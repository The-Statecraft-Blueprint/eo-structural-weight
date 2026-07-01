#!/usr/bin/env python3
"""
find_tier1_candidates.py
Find shortest EOs in the corpus — likely routine administrative orders
suitable for Tier 1 calibration (expected score near zero).

Usage:
    python3 find_tier1_candidates.py --dir eo_corpus/texts --top 30
"""

import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        default="eo_corpus/texts",
        help="Directory containing EO JSON files",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=30,
        help="Number of shortest EOs to show",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=1949,
        help="Only show EOs from this year onward (default: 1949)",
    )
    args = parser.parse_args()

    results = []

    for path in Path(args.dir).glob("EO-*.json"):
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            continue

        text = data.get("text", "")
        date_iso = data.get("date_iso", "")
        year = int(date_iso[:4]) if date_iso and len(date_iso) >= 4 else 0

        if year < args.min_year:
            continue

        word_count = len(text.split())
        results.append(
            {
                "file": path.name,
                "eo_number": data.get("eo_number", ""),
                "title": data.get("title", "")[:80],
                "date": date_iso,
                "president": data.get("president", "")[:30],
                "word_count": word_count,
                "char_count": len(text),
            }
        )

    results.sort(key=lambda r: r["word_count"])

    print(f"{'EO':<12} {'Date':<12} {'Words':>6}  {'Title'}")
    print("-" * 100)
    for r in results[: args.top]:
        print(
            f"{r['eo_number']:<12} {r['date']:<12} {r['word_count']:>6}  {r['title']}"
        )

    print(f"\nTotal EOs scanned: {len(results)}")
    print(
        "\nTip: Aim for EOs under 300 words for Tier 1 candidates. "
        "Check title for 'pay', 'holiday', 'closing', 'commission', 'advisory'."
    )


if __name__ == "__main__":
    main()
