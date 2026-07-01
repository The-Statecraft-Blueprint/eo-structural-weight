#!/usr/bin/env python3
"""
init_db.py
EO Structural Weight Score — Database Initialization

Creates the SQLite database for storing EO codings, scores, and metadata.
Run once before any other coding scripts.

Usage:
    python3 init_db.py [--db PATH]

Default DB path: eo_coding.db (in current directory)
"""

import argparse
import sqlite3
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Congress number computation
# ---------------------------------------------------------------------------

def date_to_congress(date_iso: str) -> int | None:
    """
    Map an ISO date string to the U.S. Congress number in session on that date.
    Congresses start January 3 of odd-numbered years (since 1934).
    Returns None if date is unparseable.
    """
    if not date_iso or len(date_iso) < 4:
        return None
    try:
        from datetime import date
        d = date.fromisoformat(date_iso)
        year = d.year
        # Determine which odd year the current Congress started in
        if year % 2 == 1:
            # Odd year: new Congress starts Jan 3
            congress_start_year = year if (d.month > 1 or d.day >= 3) else year - 2
        else:
            # Even year: Congress started the prior odd year
            congress_start_year = year - 1
        # 1st Congress started in 1789
        congress = (congress_start_year - 1789) // 2 + 1
        return congress if congress > 0 else None
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA = """
-- Master EO table (metadata from corpus index)
CREATE TABLE IF NOT EXISTS eos (
    eo_number       TEXT PRIMARY KEY,
    title           TEXT,
    date_iso        TEXT,
    president       TEXT,
    congress_number INTEGER,   -- computed from date_iso
    source_url      TEXT,
    word_count      INTEGER,
    corpus_file     TEXT,      -- filename in eo_corpus/texts/
    UNIQUE(eo_number)
);

-- One row per flag per EO per coder
-- Supports multiple codings (primary + inter-coder reliability)
CREATE TABLE IF NOT EXISTS flag_codings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eo_number       TEXT NOT NULL,
    coder_id        TEXT NOT NULL,   -- e.g. 'claude-v1', 'gemini-v1', 'human-jt'
    coded_date      TEXT NOT NULL,   -- ISO date string
    flag_number     INTEGER NOT NULL CHECK(flag_number BETWEEN 1 AND 11),
    flag_name       TEXT NOT NULL,
    status          TEXT NOT NULL CHECK(status IN (
                        'ABSENT', 'PRESENT', 'CRITICAL', 'NOT_APPLICABLE'
                    )),
    points          INTEGER CHECK(points IN (0, 1, 2) OR points IS NULL),
    justification   TEXT,            -- specific text cited from EO
    sub_flag_fired  INTEGER DEFAULT 0 CHECK(sub_flag_fired IN (0, 1)),
                                     -- 1 = Zombie Emergency Trap fired (flag 5 only)
    FOREIGN KEY(eo_number) REFERENCES eos(eo_number),
    UNIQUE(eo_number, coder_id, flag_number)
);

-- Computed score per EO per coder (populated by compute_scores.py)
CREATE TABLE IF NOT EXISTS eo_scores (
    eo_number               TEXT NOT NULL,
    coder_id                TEXT NOT NULL,
    applicable_count        INTEGER,   -- flags scored ABSENT/PRESENT/CRITICAL
    raw_score               INTEGER,   -- sum of points
    max_possible            INTEGER,   -- 2 × applicable_count
    normalized_score        REAL,      -- raw / max_possible (0.0–1.0)
    structural_weight_pct   REAL,      -- normalized × 100
    critical_count          INTEGER,
    present_count           INTEGER,
    absent_count            INTEGER,
    na_count                INTEGER,
    dominant_flag           INTEGER,   -- flag_number with highest score; lowest if tied
    computed_at             TEXT,      -- ISO datetime
    PRIMARY KEY(eo_number, coder_id),
    FOREIGN KEY(eo_number) REFERENCES eos(eo_number)
);

-- Inter-coder reliability summary (populated by compute_scores.py --icr)
-- One row per EO where ≥2 codings exist
CREATE TABLE IF NOT EXISTS icr_summary (
    eo_number               TEXT PRIMARY KEY,
    coder_ids               TEXT,      -- JSON array of coder_ids
    agreement_rate          REAL,      -- % of flags where all coders agree
    binary_agreement        INTEGER,   -- 1 if all coders agree on significant/not
    max_score_delta         REAL,      -- largest gap between coder normalized scores
    flags_in_dispute        TEXT,      -- JSON array of flag_numbers with disagreement
    computed_at             TEXT,
    FOREIGN KEY(eo_number) REFERENCES eos(eo_number)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_fc_eo      ON flag_codings(eo_number);
CREATE INDEX IF NOT EXISTS idx_fc_coder   ON flag_codings(coder_id);
CREATE INDEX IF NOT EXISTS idx_scores_pct ON eo_scores(structural_weight_pct);
CREATE INDEX IF NOT EXISTS idx_eos_date   ON eos(date_iso);
CREATE INDEX IF NOT EXISTS idx_eos_cong   ON eos(congress_number);
"""


# ---------------------------------------------------------------------------
# Seed the flag name lookup (for validation and display)
# ---------------------------------------------------------------------------

FLAG_NAMES = {
    1:  "Power Concentration",
    2:  "Accountability Gaps",
    3:  "Bundling",
    4:  "Vague Enforcement",
    5:  "Perverse Incentives",
    6:  "Sunset Provisions",
    7:  "Preemption of Oversight",
    8:  "Third-Party Incentive Gaps",
    9:  "Second/Third-Order Effects",
    10: "Inter-Agency Cannibalization",
    11: "Exemptions Architecture",
}

FLAG_SEED = """
CREATE TABLE IF NOT EXISTS flags (
    flag_number INTEGER PRIMARY KEY,
    flag_name   TEXT NOT NULL,
    sub_flag    TEXT  -- description of sub-flag if any (null for most)
);
"""

FLAG_ROWS = [
    (1,  "Power Concentration",         None),
    (2,  "Accountability Gaps",         None),
    (3,  "Bundling",                    None),
    (4,  "Vague Enforcement",           None),
    (5,  "Perverse Incentives",         "Zombie Emergency Trap"),
    (6,  "Sunset Provisions",           None),
    (7,  "Preemption of Oversight",     None),
    (8,  "Third-Party Incentive Gaps",  None),
    (9,  "Second/Third-Order Effects",  None),
    (10, "Inter-Agency Cannibalization",None),
    (11, "Exemptions Architecture",     None),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Initialize the EO Structural Weight Score SQLite database."
    )
    parser.add_argument(
        "--db",
        default="eo_coding.db",
        help="Path to the SQLite database file (default: eo_coding.db)",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if db_path.exists():
        print(f"Database already exists at {db_path}. Adding any missing tables/indexes.")
    else:
        print(f"Creating new database at {db_path}.")

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Create tables
    cur.executescript(SCHEMA)
    cur.executescript(FLAG_SEED)

    # Seed flag reference table (ignore if already present)
    cur.executemany(
        "INSERT OR IGNORE INTO flags (flag_number, flag_name, sub_flag) VALUES (?, ?, ?)",
        FLAG_ROWS,
    )
    con.commit()

    # Report
    cur.execute("SELECT COUNT(*) FROM eos")
    eo_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM flag_codings")
    coding_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM eo_scores")
    score_count = cur.fetchone()[0]

    print(f"\nDatabase ready: {db_path}")
    print(f"  EOs indexed:       {eo_count}")
    print(f"  Flag codings:      {coding_count}")
    print(f"  Computed scores:   {score_count}")
    print(f"  Flag reference:    11 flags seeded")
    print(
        "\nNext steps:"
        "\n  python3 import_corpus_index.py --db eo_coding.db --index eo_corpus/eo_index.csv"
        "\n  python3 create_coding_template.py --db eo_coding.db --eo 13769"
    )

    con.close()


if __name__ == "__main__":
    main()
