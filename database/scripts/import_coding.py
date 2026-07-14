#!/usr/bin/env python3
"""
import_coding.py
EO Structural Weight Score — Coding Import and Score Computation

Validates a completed JSON coding file and imports it into the database.
Automatically computes the structural-weight score on import.

Usage:
    python3 import_coding.py --db eo_coding.db --coding codings/13769-claude-v1.json
    python3 import_coding.py --db eo_coding.db --coding codings/ --batch
    python3 import_coding.py --db eo_coding.db --icr 13769   # inter-coder report

The JSON format is defined by create_coding_template.py.
Fields that begin with _ (like _instructions, _eo_text, _definition) are ignored.
"""

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

VALID_STATUSES = {"ABSENT", "PRESENT", "CRITICAL", "NOT_APPLICABLE"}
STATUS_TO_POINTS = {"ABSENT": 0, "PRESENT": 1, "CRITICAL": 2, "NOT_APPLICABLE": None}
FLAG_NAMES = {
    1: "Power Concentration",       2: "Accountability Gaps",
    3: "Bundling",                  4: "Vague Enforcement",
    5: "Perverse Incentives",       6: "Sunset Provisions",
    7: "Preemption of Oversight",   8: "Third-Party Incentive Gaps",
    9: "Second/Third-Order Effects", 10: "Inter-Agency Cannibalization",
    11: "Exemptions Architecture",
}


def validate_coding(data: dict) -> list[str]:
    """Return list of validation errors (empty = valid)."""
    errors = []

    if not data.get("eo_number"):
        errors.append("Missing eo_number")
    if not data.get("coder_id"):
        errors.append("Missing coder_id")
    if not data.get("coded_date"):
        errors.append("Missing coded_date")

    flags = data.get("flags", [])
    if len(flags) != 11:
        errors.append(f"Expected 11 flags, got {len(flags)}")
        return errors  # can't validate further

    seen_flag_nums = set()
    for flag in flags:
        fn = flag.get("flag_number")
        if fn not in range(1, 12):
            errors.append(f"Invalid flag_number: {fn}")
            continue
        if fn in seen_flag_nums:
            errors.append(f"Duplicate flag_number: {fn}")
        seen_flag_nums.add(fn)

        status = flag.get("status", "").upper()
        if status not in VALID_STATUSES:
            errors.append(f"Flag {fn}: invalid status '{flag.get('status')}'")
            continue

        points = flag.get("points")
        expected_points = STATUS_TO_POINTS[status]
        if points != expected_points:
            errors.append(
                f"Flag {fn}: status={status} expects points={expected_points}, "
                f"got {points}"
            )

        if not flag.get("justification"):
            errors.append(f"Flag {fn}: missing justification")

    missing = set(range(1, 12)) - seen_flag_nums
    if missing:
        errors.append(f"Missing flags: {sorted(missing)}")

    return errors


# ---------------------------------------------------------------------------
# Score computation
# ---------------------------------------------------------------------------

def compute_score(flags: list[dict]) -> dict:
    """Compute structural-weight score from a list of flag dicts."""
    applicable_count = 0
    raw_score = 0
    critical_count = 0
    present_count = 0
    absent_count = 0
    na_count = 0
    flag_scores = {}

    for flag in flags:
        fn = flag["flag_number"]
        status = flag["status"].upper()
        points = flag.get("points")

        if status == "NOT_APPLICABLE":
            na_count += 1
        elif status == "ABSENT":
            applicable_count += 1
            absent_count += 1
            flag_scores[fn] = 0
        elif status == "PRESENT":
            applicable_count += 1
            present_count += 1
            raw_score += 1
            flag_scores[fn] = 1
        elif status == "CRITICAL":
            applicable_count += 1
            critical_count += 1
            raw_score += 2
            flag_scores[fn] = 2

    max_possible = 2 * applicable_count
    normalized = (raw_score / max_possible) if max_possible > 0 else None
    structural_weight_pct = normalized * 100 if normalized is not None else None

    # Dominant flag: highest-scoring; if tied, lowest flag number
    dominant_flag = None
    if flag_scores:
        max_pts = max(flag_scores.values())
        dominant_flag = min(fn for fn, pts in flag_scores.items() if pts == max_pts)

    return {
        "applicable_count": applicable_count,
        "raw_score": raw_score,
        "max_possible": max_possible,
        "normalized_score": round(normalized, 4) if normalized is not None else None,
        "structural_weight_pct": round(structural_weight_pct, 2)
                                 if structural_weight_pct is not None else None,
        "critical_count": critical_count,
        "present_count": present_count,
        "absent_count": absent_count,
        "na_count": na_count,
        "dominant_flag": dominant_flag,
    }


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def import_coding(con: sqlite3.Connection, data: dict, overwrite: bool = False) -> bool:
    """
    Insert one coding into the database. Returns True on success.
    If overwrite=True, deletes existing coding first.
    """
    cur = con.cursor()
    eo_number = data["eo_number"]
    coder_id = data["coder_id"]
    coded_date = data["coded_date"]
    flags = data["flags"]

    if overwrite:
        cur.execute(
            "DELETE FROM flag_codings WHERE eo_number=? AND coder_id=?",
            (eo_number, coder_id),
        )
        cur.execute(
            "DELETE FROM eo_scores WHERE eo_number=? AND coder_id=?",
            (eo_number, coder_id),
        )

    # Ensure EO exists in eos table (insert stub if not)
    cur.execute("SELECT eo_number FROM eos WHERE eo_number=?", (eo_number,))
    if not cur.fetchone():
        cur.execute(
            "INSERT OR IGNORE INTO eos (eo_number, title, date_iso, president, "
            "source_url) VALUES (?, ?, ?, ?, ?)",
            (
                eo_number,
                data.get("title", ""),
                data.get("date_iso", ""),
                data.get("president", ""),
                data.get("source_url", ""),
            ),
        )

    # Insert flag codings
    for flag in flags:
        fn = flag["flag_number"]
        status = flag["status"].upper()
        points = flag.get("points")
        sub_flag = 1 if (fn == 5 and flag.get("sub_flag_fired")) else 0
        try:
            cur.execute(
                """
                INSERT INTO flag_codings
                    (eo_number, coder_id, coded_date, flag_number, flag_name,
                     status, points, justification, sub_flag_fired)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    eo_number,
                    coder_id,
                    coded_date,
                    fn,
                    FLAG_NAMES.get(fn, ""),
                    status,
                    points,
                    flag.get("justification", ""),
                    sub_flag,
                ),
            )
        except sqlite3.IntegrityError:
            print(f"  Warning: flag {fn} for EO {eo_number} by {coder_id} already exists. "
                  "Use --overwrite to replace.")
            return False

    # Compute and insert score
    score = compute_score(flags)
    score["eo_number"] = eo_number
    score["coder_id"] = coder_id
    score["computed_at"] = datetime.now().isoformat()

    cur.execute(
        """
        INSERT OR REPLACE INTO eo_scores
            (eo_number, coder_id, applicable_count, raw_score, max_possible,
             normalized_score, structural_weight_pct, critical_count, present_count,
             absent_count, na_count, dominant_flag, computed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            score["eo_number"],
            score["coder_id"],
            score["applicable_count"],
            score["raw_score"],
            score["max_possible"],
            score["normalized_score"],
            score["structural_weight_pct"],
            score["critical_count"],
            score["present_count"],
            score["absent_count"],
            score["na_count"],
            score["dominant_flag"],
            score["computed_at"],
        ),
    )

    con.commit()
    return True


# ---------------------------------------------------------------------------
# Inter-coder reliability report
# ---------------------------------------------------------------------------

def icr_report(con: sqlite3.Connection, eo_number: str) -> None:
    """Print an inter-coder reliability report for a given EO."""
    cur = con.cursor()

    cur.execute(
        "SELECT DISTINCT coder_id FROM flag_codings WHERE eo_number=?",
        (eo_number,),
    )
    coders = [row[0] for row in cur.fetchall()]

    if len(coders) < 2:
        print(f"Only {len(coders)} coder(s) found for EO {eo_number}. "
              "Need ≥2 for ICR.")
        return

    print(f"\nInter-Coder Reliability Report — EO {eo_number}")
    print(f"Coders: {', '.join(coders)}")
    print()

    # Per-flag comparison
    agree_count = 0
    disagree_count = 0
    disputes = []

    cur.execute("""
        SELECT flag_number, flag_name, coder_id, status, points
        FROM flag_codings
        WHERE eo_number=?
        ORDER BY flag_number, coder_id
    """, (eo_number,))

    by_flag: dict[int, dict] = {}
    for fn, fname, coder, status, points in cur.fetchall():
        if fn not in by_flag:
            by_flag[fn] = {"name": fname, "codings": {}}
        by_flag[fn]["codings"][coder] = {"status": status, "points": points}

    print(f"{'Flag':<5} {'Name':<35} ", end="")
    for c in coders:
        print(f"{c:<20}", end="")
    print("Agreement")
    print("-" * (45 + 20 * len(coders) + 10))

    for fn in sorted(by_flag.keys()):
        fdata = by_flag[fn]
        codings = fdata["codings"]
        statuses = [codings.get(c, {}).get("status", "MISSING") for c in coders]
        agree = len(set(statuses)) == 1

        if agree:
            agree_count += 1
            marker = "✓"
        else:
            disagree_count += 1
            disputes.append(fn)
            marker = "✗"

        print(f"{fn:<5} {fdata['name']:<35} ", end="")
        for c in coders:
            s = codings.get(c, {}).get("status", "MISSING")
            print(f"{s:<20}", end="")
        print(marker)

    total_flags = agree_count + disagree_count
    agreement_rate = agree_count / total_flags * 100 if total_flags > 0 else 0

    print(f"\nAgreement: {agree_count}/{total_flags} flags ({agreement_rate:.1f}%)")
    if disputes:
        print(f"Flags in dispute: {disputes}")

    # Score comparison
    print("\nScores by coder:")
    cur.execute(
        "SELECT coder_id, structural_weight_pct, critical_count, present_count "
        "FROM eo_scores WHERE eo_number=? ORDER BY coder_id",
        (eo_number,),
    )
    for row in cur.fetchall():
        coder, pct, crit, pres = row
        pct_str = f"{pct:>6.1f}%" if pct is not None else "   N/A "
        print(f"  {coder:<25} {pct_str}  "
              f"(CRITICAL: {crit}, PRESENT: {pres})")

    # Binary classification (significant threshold = 35%)
    THRESHOLD = 0.35
    cur.execute(
        "SELECT coder_id, normalized_score FROM eo_scores WHERE eo_number=?",
        (eo_number,),
    )
    classifications = {row[0]: ("SIGNIFICANT" if row[1] and row[1] >= THRESHOLD
                                else "NOT SIGNIFICANT")
                       for row in cur.fetchall()}
    class_values = set(classifications.values())
    binary_agree = len(class_values) == 1
    print(f"\nBinary classification (threshold ≥{THRESHOLD:.0%}):")
    for coder, cls in classifications.items():
        print(f"  {coder:<25} {cls}")
    print(f"Binary agreement: {'YES' if binary_agree else 'NO'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Import EO codings into the database and compute scores."
    )
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument(
        "--coding",
        help="Path to completed coding JSON file, or directory for --batch",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Import all *.json files in the --coding directory",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing coding if present",
    )
    parser.add_argument(
        "--icr",
        metavar="EO_NUMBER",
        help="Print inter-coder reliability report for this EO number",
    )
    args = parser.parse_args()

    con = sqlite3.connect(args.db)

    if args.icr:
        icr_report(con, args.icr)
        con.close()
        return

    if not args.coding:
        parser.error("--coding is required unless --icr is used")

    coding_path = Path(args.coding)

    if args.batch:
        if not coding_path.is_dir():
            print(f"Error: {coding_path} is not a directory")
            return
        files = list(coding_path.glob("*.json"))
        # Skip templates (files starting with "template-")
        files = [f for f in files if not f.name.startswith("template-")]
        print(f"Batch import: {len(files)} coding files found.")
        success = 0
        for fpath in sorted(files):
            with open(fpath) as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"  {fpath.name}: JSON error — {e}")
                    continue
            # Strip underscore-prefixed keys
            data = {k: v for k, v in data.items() if not k.startswith("_")}
            if "flags" in data:
                for flag in data["flags"]:
                    flag.pop("_definition", None)
            errors = validate_coding(data)
            if errors:
                print(f"  {fpath.name}: INVALID — {errors[0]}")
                continue
            ok = import_coding(con, data, overwrite=args.overwrite)
            if ok:
                score = compute_score(data["flags"])
                pct = score["structural_weight_pct"]
                pct_str = f"{pct:.1f}%" if pct is not None else "N/A (0 applicable flags)"
                print(f"  {fpath.name}: OK — EO {data['eo_number']} "
                      f"score={pct_str}")
                success += 1
        print(f"\nBatch complete: {success}/{len(files)} imported.")

    else:
        if not coding_path.exists():
            print(f"Error: {coding_path} not found")
            return

        with open(coding_path) as f:
            data = json.load(f)

        # Strip underscore-prefixed keys
        data = {k: v for k, v in data.items() if not k.startswith("_")}
        if "flags" in data:
            for flag in data["flags"]:
                flag.pop("_definition", None)

        errors = validate_coding(data)
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
            return

        ok = import_coding(con, data, overwrite=args.overwrite)
        if ok:
            score = compute_score(data["flags"])
            print(f"Imported: EO {data['eo_number']} by {data['coder_id']}")
            print(f"  Structural weight: {score['structural_weight_pct']:.1f}%")
            print(f"  Raw: {score['raw_score']}/{score['max_possible']} "
                  f"({score['applicable_count']} applicable flags)")
            print(f"  CRITICAL: {score['critical_count']} | "
                  f"PRESENT: {score['present_count']} | "
                  f"ABSENT: {score['absent_count']} | "
                  f"N/A: {score['na_count']}")

    con.close()


if __name__ == "__main__":
    main()
