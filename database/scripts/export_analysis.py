#!/usr/bin/env python3
"""
export_analysis.py
EO Structural Weight Score — Analysis Export

Exports EO structural-weight scores aggregated to the Congress level,
aligned with the Binder gridlock series for the EO-weight vs. gridlock
hypothesis test (Claim 3 of the scoring scheme).

Also exports a flat per-EO score table for all other analyses.

Usage:
    # Export everything (requires codings to exist in database)
    python3 export_analysis.py --db eo_coding.db --gridlock binder_gridlock_1947-2022.csv

    # Primary coder only (default: most recent coding per EO)
    python3 export_analysis.py --db eo_coding.db --coder claude-church-bells-v1

    # Export per-EO scores only (no Binder alignment)
    python3 export_analysis.py --db eo_coding.db --per-eo-only

Outputs:
    scores_per_eo.csv          — one row per EO with score and metadata
    scores_by_congress.csv     — one row per Congress with aggregated scores
    gridlock_comparison.csv    — Congress-level join with Binder grid4 (if --gridlock)
"""

import argparse
import csv
import sqlite3
from pathlib import Path


# ---------------------------------------------------------------------------
# Per-EO export
# ---------------------------------------------------------------------------

def export_per_eo(con: sqlite3.Connection, coder_id: str | None,
                  output_path: Path) -> int:
    """
    Export one row per EO (selecting one coding per EO based on coder_id or
    latest coded_date if coder_id not specified).
    """
    cur = con.cursor()

    if coder_id:
        query = """
            SELECT
                s.eo_number,
                e.title,
                e.date_iso,
                e.president,
                e.congress_number,
                s.coder_id,
                s.applicable_count,
                s.raw_score,
                s.max_possible,
                s.normalized_score,
                s.structural_weight_pct,
                s.critical_count,
                s.present_count,
                s.absent_count,
                s.na_count,
                s.dominant_flag,
                s.computed_at
            FROM eo_scores s
            JOIN eos e ON e.eo_number = s.eo_number
            WHERE s.coder_id = ?
            ORDER BY e.date_iso
        """
        cur.execute(query, (coder_id,))
    else:
        # Latest coding per EO
        query = """
            SELECT
                s.eo_number,
                e.title,
                e.date_iso,
                e.president,
                e.congress_number,
                s.coder_id,
                s.applicable_count,
                s.raw_score,
                s.max_possible,
                s.normalized_score,
                s.structural_weight_pct,
                s.critical_count,
                s.present_count,
                s.absent_count,
                s.na_count,
                s.dominant_flag,
                s.computed_at
            FROM eo_scores s
            JOIN eos e ON e.eo_number = s.eo_number
            WHERE s.computed_at = (
                SELECT MAX(computed_at) FROM eo_scores
                WHERE eo_number = s.eo_number
            )
            ORDER BY e.date_iso
        """
        cur.execute(query)

    rows = cur.fetchall()
    headers = [
        "eo_number", "title", "date_iso", "president", "congress_number",
        "coder_id", "applicable_count", "raw_score", "max_possible",
        "normalized_score", "structural_weight_pct",
        "critical_count", "present_count", "absent_count", "na_count",
        "dominant_flag", "computed_at",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return len(rows)


# ---------------------------------------------------------------------------
# Congress-level aggregation
# ---------------------------------------------------------------------------

def export_by_congress(con: sqlite3.Connection, coder_id: str | None,
                       output_path: Path) -> dict[int, dict]:
    """
    Aggregate EO scores by Congress. Returns dict keyed by congress_number.
    Two aggregation methods:
      - mean_structural_weight: mean normalized score (0–100) across all EOs
      - sum_raw_score: sum of raw scores (captures total structural machinery volume)
      - count_eos: number of EOs signed in this Congress
      - count_significant: EOs with normalized_score ≥ 0.35 (interim threshold)
    """
    cur = con.cursor()

    base_filter = f"AND s.coder_id = '{coder_id}'" if coder_id else ""

    query = f"""
        SELECT
            e.congress_number,
            COUNT(s.eo_number)              AS count_eos,
            AVG(s.structural_weight_pct)    AS mean_structural_weight,
            SUM(s.raw_score)                AS sum_raw_score,
            SUM(CASE WHEN s.normalized_score >= 0.35 THEN 1 ELSE 0 END)
                                            AS count_significant,
            AVG(s.critical_count)           AS avg_critical_flags,
            SUM(s.critical_count)           AS sum_critical_flags
        FROM eo_scores s
        JOIN eos e ON e.eo_number = s.eo_number
        WHERE e.congress_number IS NOT NULL
          {base_filter}
        GROUP BY e.congress_number
        ORDER BY e.congress_number
    """
    cur.execute(query)
    rows = cur.fetchall()

    headers = [
        "congress_number", "count_eos", "mean_structural_weight",
        "sum_raw_score", "count_significant",
        "avg_critical_flags", "sum_critical_flags",
    ]
    congress_data = {}
    for row in rows:
        congress_data[row[0]] = dict(zip(headers, row))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return congress_data


# ---------------------------------------------------------------------------
# Gridlock comparison join
# ---------------------------------------------------------------------------

def export_gridlock_comparison(congress_data: dict[int, dict],
                                gridlock_path: Path,
                                output_path: Path) -> int:
    """
    Join Congress-level EO scores with Binder gridlock series.
    The canonical gridlock measure is grid4 (NYT salience threshold ≥4).
    """
    # Load Binder data
    binder = {}
    with open(gridlock_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                congress = int(row["congress"])
                binder[congress] = {
                    "years": row.get("years", ""),
                    "start_year": row.get("start_year", ""),
                    "grid1": _float_or_none(row.get("grid1")),
                    "grid2": _float_or_none(row.get("grid2")),
                    "grid3": _float_or_none(row.get("grid3")),
                    "grid4": _float_or_none(row.get("grid4")),  # canonical
                    "grid5": _float_or_none(row.get("grid5")),
                    "agenda4": _float_or_none(row.get("agenda4")),
                    "fail4":   _float_or_none(row.get("fail4")),
                }
            except (ValueError, KeyError):
                continue

    # Find overlap
    eo_congresses = set(congress_data.keys())
    binder_congresses = set(binder.keys())
    overlap = sorted(eo_congresses & binder_congresses)
    eo_only = sorted(eo_congresses - binder_congresses)
    binder_only = sorted(binder_congresses - eo_congresses)

    headers = [
        "congress_number", "years", "start_year",
        # Binder
        "grid4", "grid1", "grid2", "grid3", "grid5", "agenda4", "fail4",
        # EO scores
        "count_eos", "mean_structural_weight", "sum_raw_score",
        "count_significant", "avg_critical_flags", "sum_critical_flags",
    ]

    rows = []
    for congress in overlap:
        b = binder[congress]
        e = congress_data[congress]
        rows.append([
            congress,
            b["years"], b["start_year"],
            b["grid4"], b["grid1"], b["grid2"], b["grid3"], b["grid5"],
            b["agenda4"], b["fail4"],
            e["count_eos"], e["mean_structural_weight"], e["sum_raw_score"],
            e["count_significant"], e["avg_critical_flags"], e["sum_critical_flags"],
        ])

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"\nGridlock comparison:")
    print(f"  Overlap: {len(overlap)} Congresses")
    print(f"  EO data only (no Binder): {eo_only}")
    print(f"  Binder only (no EO data): {binder_only}")
    print(f"  Primary measure: grid4 (NYT salience ≥4)")
    print(f"\n  Note: run Spearman correlation between mean_structural_weight")
    print(f"  and grid4 to test the engine-model exhaust-gauge prediction.")

    return len(overlap)


def _float_or_none(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Export EO structural-weight scores for analysis."
    )
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument(
        "--coder",
        default=None,
        help="Restrict to a specific coder_id (default: latest per EO)",
    )
    parser.add_argument(
        "--gridlock",
        default=None,
        help="Path to binder_gridlock_1947-2022.csv for hypothesis test export",
    )
    parser.add_argument(
        "--per-eo-only",
        action="store_true",
        help="Export per-EO scores only; skip Congress aggregation",
    )
    parser.add_argument(
        "--output-dir",
        default="analysis_output",
        help="Directory for output files (default: analysis_output/)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(args.db)

    # Check that scores exist
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM eo_scores")
    score_count = cur.fetchone()[0]
    if score_count == 0:
        print("No scores found in database. Import codings first.")
        print("  python3 import_coding.py --db eo_coding.db --coding <file>")
        con.close()
        return

    print(f"Database has {score_count} scored EOs.")

    # Per-EO export
    per_eo_path = output_dir / "scores_per_eo.csv"
    n = export_per_eo(con, args.coder, per_eo_path)
    print(f"Per-EO scores: {n} rows → {per_eo_path}")

    if args.per_eo_only:
        con.close()
        return

    # Congress-level aggregation
    congress_path = output_dir / "scores_by_congress.csv"
    congress_data = export_by_congress(con, args.coder, congress_path)
    print(f"Congress scores: {len(congress_data)} Congresses → {congress_path}")

    # Gridlock comparison
    if args.gridlock:
        gridlock_path = Path(args.gridlock)
        if not gridlock_path.exists():
            print(f"Warning: Binder gridlock file not found: {gridlock_path}")
        else:
            comparison_path = output_dir / "gridlock_comparison.csv"
            n = export_gridlock_comparison(
                congress_data, gridlock_path, comparison_path
            )
            print(f"Gridlock comparison: {n} Congresses → {comparison_path}")
    else:
        print("\nNote: run with --gridlock binder_gridlock_1947-2022.csv to generate "
              "the gridlock comparison table once sufficient EOs are coded.")

    con.close()
    print(f"\nOutput directory: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
