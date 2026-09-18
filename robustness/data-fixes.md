# Data Fixes Log

## 2026-09-18: garbled president field (EO 14412, EO 14413)

The scraper had concatenated the page's byline and title into the `president` field. Example: `Donald J. Trump (2nd Term)47th President of the United States: 2025—presentExecutive Order 14412—Securing the Nation…`. These orders were grouped as a separate "president" in any aggregation by president.

Changed to `Donald J. Trump (2nd Term)` in:

- `database/corpus-texts/EO-14412.json`, `EO-14413.json` (`president` key only; text untouched)
- `database/eo_index.csv` (president column only; 3 rows, including the unnumbered regenerative-agriculture order)
- `database/eo_coding.db`, table `eos` (2 rows). The update ran on a copy outside the mounted folder and was copied back. `pragma integrity_check` returned ok before and after, and row counts in `flag_codings` (86,504) and `eo_scores` (7,864) are unchanged.

No scores, flags or justifications changed.

A first attempt to update the database in place on the mounted folder failed with a disk I/O error partway through. It left a hot `-journal` file. The database was restored byte-for-byte from git HEAD before the fix above was applied. The stale journal was moved to `_to_delete/eo_coding.db-journal.stale` at the repo root. Delete that folder; don't restore the file next to the database.
