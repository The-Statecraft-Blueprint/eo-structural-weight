#!/usr/bin/env python3
"""
compute_icr_summary.py
EO Structural Weight Score — Inter-Coder Reliability Aggregation

Populates icr_summary from flag_codings for every EO that has been coded by
2+ coders. Complements import_coding.py's --icr (which prints a single-EO
report to stdout but doesn't persist anything). This is the piece referenced
but not yet built as of the v1.1 pre-registration amendment.

Usage:
    python3 compute_icr_summary.py --db eo_coding.db
    python3 compute_icr_summary.py --db eo_coding.db --sample icr-sample-v1.csv  # restrict to a named sample, and print the aggregate rollup
"""

import argparse
import csv
import json
import sqlite3
from datetime import datetime, timezone


def compute_for_eo(con: sqlite3.Connection, eo_number: str) -> dict | None:
    cur = con.cursor()
    cur.execute("SELECT DISTINCT coder_id FROM flag_codings WHERE eo_number=?", (eo_number,))
    coders = sorted(row[0] for row in cur.fetchall())
    if len(coders) < 2:
        return None

    cur.execute(
        """SELECT flag_number, coder_id, status FROM flag_codings
           WHERE eo_number=? ORDER BY flag_number""",
        (eo_number,),
    )
    by_flag: dict[int, dict[str, str]] = {}
    for fn, coder, status in cur.fetchall():
        by_flag.setdefault(fn, {})[coder] = status

    agree, total, disputes = 0, 0, []
    for fn, statuses in by_flag.items():
        vals = list(statuses.values())
        if len(vals) < 2:
            continue
        total += 1
        if len(set(vals)) == 1:
            agree += 1
        else:
            disputes.append(fn)

    agreement_rate = round(agree / total * 100, 1) if total else None

    cur.execute(
        "SELECT coder_id, structural_weight_pct FROM eo_scores WHERE eo_number=?",
        (eo_number,),
    )
    scores = {c: p for c, p in cur.fetchall()}
    numeric = [p for p in scores.values() if p is not None]
    max_delta = round(max(numeric) - min(numeric), 1) if len(numeric) >= 2 else None

    THRESHOLD = 0.35
    cur.execute(
        "SELECT coder_id, normalized_score FROM eo_scores WHERE eo_number=?", (eo_number,)
    )
    classes = {
        c: ("SIGNIFICANT" if s is not None and s >= THRESHOLD else "NOT SIGNIFICANT")
        for c, s in cur.fetchall()
    }
    binary_agreement = 1 if len(set(classes.values())) == 1 else 0

    return {
        "eo_number": eo_number,
        "coder_ids": ",".join(coders),
        "agreement_rate": agreement_rate,
        "binary_agreement": binary_agreement,
        "max_score_delta": max_delta,
        "flags_in_dispute": json.dumps(disputes),
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--sample", help="CSV with an eo_number column to restrict/report on")
    args = ap.parse_args()

    con = sqlite3.connect(args.db)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT eo_number FROM flag_codings")
    all_eos = [r[0] for r in cur.fetchall()]

    written = []
    for eo in all_eos:
        row = compute_for_eo(con, eo)
        if row is None:
            continue
        con.execute(
            """INSERT INTO icr_summary
               (eo_number, coder_ids, agreement_rate, binary_agreement, max_score_delta, flags_in_dispute, computed_at)
               VALUES (:eo_number, :coder_ids, :agreement_rate, :binary_agreement, :max_score_delta, :flags_in_dispute, :computed_at)
               ON CONFLICT(eo_number) DO UPDATE SET
                 coder_ids=excluded.coder_ids, agreement_rate=excluded.agreement_rate,
                 binary_agreement=excluded.binary_agreement, max_score_delta=excluded.max_score_delta,
                 flags_in_dispute=excluded.flags_in_dispute, computed_at=excluded.computed_at""",
            row,
        )
        written.append(row)
    con.commit()
    print(f"icr_summary updated for {len(written)} EO(s) with 2+ coders.")

    target_eos = None
    if args.sample:
        target_eos = {r["eo_number"] for r in csv.DictReader(open(args.sample))}
        rollup = [r for r in written if r["eo_number"] in target_eos]
    else:
        rollup = written

    if rollup:
        n = len(rollup)
        avg_agree = sum(r["agreement_rate"] for r in rollup if r["agreement_rate"] is not None) / n
        binary_agree_rate = sum(r["binary_agreement"] for r in rollup) / n * 100
        print(f"\nRollup over {n} EO(s):")
        print(f"  Mean per-flag agreement rate: {avg_agree:.1f}%")
        print(f"  Binary classification agreement: {binary_agree_rate:.1f}% "
              f"(pre-registered target: \u226580%)")
        print(f"  NOTE: n={n} — this is a partial sample. Pre-registered target sample "
              f"size is 10% of the validation batch, min 20 EOs with 2+ coders.")


if __name__ == "__main__":
    main()
