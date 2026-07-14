#!/usr/bin/env python3
"""
import_corpus_index.py
EO Structural Weight Score — Corpus Index Import

Reads the eo_index.csv produced by the scraper and populates the eos table.
Also computes the Congress number for each EO from its date.

Usage:
    python3 import_corpus_index.py --db eo_coding.db --index eo_corpus/eo_index.csv

Run after init_db.py. Safe to re-run — uses INSERT OR IGNORE.
"""

import argparse
import csv
import sqlite3
from datetime import date
from pathlib import Path


def date_to_congress(date_iso: str) -> int | None:
    """Map ISO date to U.S. Congress number."""
    if not date_iso or len(date_iso) < 4:
        return None
    try:
        d = date.fromisoformat(date_iso)
        year = d.year
        if year % 2 == 1:
            congress_start_year = year if (d.month > 1 or d.day >= 3) else year - 2
        else:
            congress_start_year = year - 1
        congress = (congress_start_year - 1789) // 2 + 1
        return congress if congress > 0 else None
    except (ValueError, TypeError):
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--index", required=True, help="Path to eo_index.csv")
    parser.add_argument(
        "--corpus-dir",
        default=None,
        help="Path to eo_corpus/texts/ directory (for word counts). Optional.",
    )
    args = parser.parse_args()

    index_path = Path(args.index)
    if not index_path.exists():
        print(f"Error: index file not found: {index_path}")
        return 1

    con = sqlite3.connect(args.db)
    cur = con.cursor()

    inserted = 0
    skipped = 0
    errors = 0

    with open(index_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if row.get("status") != "ok":
                continue

            eo_number = row.get("eo_number", "").strip()
            if not eo_number:
                continue

            date_iso = row.get("date", "").strip()
            congress = date_to_congress(date_iso)

            # Word count from corpus file if directory provided
            word_count = None
            corpus_file = None
            if args.corpus_dir:
                import json
                import re
                safe = re.sub(r"[^\w-]", "_", eo_number)
                fname = f"EO-{safe}.json"
                fpath = Path(args.corpus_dir) / fname
                if fpath.exists():
                    try:
                        with open(fpath) as jf:
                            d = json.load(jf)
                        word_count = len(d.get("text", "").split())
                        corpus_file = fname
                    except Exception:
                        pass

            rows.append((
                eo_number,
                row.get("title", "").strip(),
                date_iso,
                row.get("president", "").strip(),
                congress,
                row.get("url", "").strip(),
                word_count,
                corpus_file,
            ))

        # Batch insert
        for row in rows:
            try:
                cur.execute(
                    """
                    INSERT OR IGNORE INTO eos
                        (eo_number, title, date_iso, president, congress_number,
                         source_url, word_count, corpus_file)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )
                if cur.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except sqlite3.Error as e:
                print(f"  Error inserting {row[0]}: {e}")
                errors += 1

    con.commit()

    cur.execute("SELECT COUNT(*) FROM eos")
    total = cur.fetchone()[0]

    print(f"Import complete.")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (already present): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total EOs in database: {total}")

    # Congress distribution summary
    cur.execute("""
        SELECT congress_number, COUNT(*) as cnt
        FROM eos
        WHERE congress_number IS NOT NULL
        GROUP BY congress_number
        ORDER BY congress_number
        LIMIT 5
    """)
    print("\nFirst 5 Congresses in index:")
    for row in cur.fetchall():
        print(f"  {row[0]}th Congress: {row[1]} EOs")

    cur.execute("""
        SELECT congress_number, COUNT(*) as cnt
        FROM eos
        WHERE congress_number IS NOT NULL
        GROUP BY congress_number
        ORDER BY congress_number DESC
        LIMIT 5
    """)
    print("Last 5 Congresses in index:")
    for row in cur.fetchall():
        print(f"  {row[0]}th Congress: {row[1]} EOs")

    con.close()


if __name__ == "__main__":
    main()
