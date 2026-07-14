# Database

The shared foundational data underneath everything else in this project: the raw source text every coding decision was made from, the tooling that builds and maintains the coding database, and the consolidated record of every coding decision itself.

## Files

| Path | Description |
|---|---|
| `corpus-texts/` | Full text of all 7,151 executive orders from 1936–present, one JSON file per order (`EO-{number}.json`, containing title, date, president, and full text). This is the primary-source material behind every score in this project — anyone can independently verify a coding decision by reading the same text the coder read. |
| `eo_coding.db` | SQLite database with every coding record ever produced for this project, across every coder. See below. |
| `scripts/` | The actual tooling that builds and maintains `eo_coding.db` from JSON coding files — `init_db.py` (creates the schema, including Congress-number mapping), `import_coding.py` (validates and imports a completed coding file, computing the score on import), `create_coding_template.py`, `import_corpus_index.py`, `export_analysis.py`. Run these, don't hand-edit the database. |
| `eo_index.csv` | Master index of the full corpus (all years, not just 1936-present). |
| `errors.log` | Log from the original corpus-scraping process. |
| `find_tier1_candidates.py` | Corpus-building utility script. |

## `eo_coding.db` is a derived artifact — read this before editing anything

**The JSON coding files are the source of truth. The database is rebuilt from them, not maintained independently.** Every batch of coded orders — the Mayer & Price validation runs in `mayer-price-validation/`, the extension batches in `extension/stream-a/` and `extension/stream-b/` — exists first as JSON. The database is a convenience layer built by importing all of those JSON files into one queryable place.

This matters in practice: if you ever need to fix, extend, or merge coding data, **edit the JSON files and rebuild the database from scratch**, rather than hand-editing the database directly. Two independent processes writing to the same SQLite file at once caused real problems earlier in this project (see the git history around the two-stream extension effort) — treating JSON as authoritative and the database as disposable/reproducible is what avoided that becoming a permanent mess.

### Table structure

- **`eos`** — one row per executive order: `eo_number`, `title`, `date_iso`, `president`, `corpus_file`.
- **`flag_codings`** — one row per (order, coder, flag): status, points, justification, whether the Zombie Emergency Trap sub-flag fired.
- **`eo_scores`** — one row per (order, coder): the aggregated score (`applicable_count`, `raw_score`, `max_possible`, `normalized_score`, `structural_weight_pct`) plus status counts.

### `coder_id` values, in the order they were produced

| `coder_id` | What it is |
|---|---|
| `gemini-2.5-collaborator`, `gemini-2.5-flash`, `gpt-5.5-thinking-v1`, `gpt-5.5-thinking-v2` | An early 30-order inter-coder reliability pilot, predating the full validation sample. Kept for completeness, not used as validation evidence. |
| `claude-church-bells-v1` | Primary coding — the original label-aware pass over the Mayer & Price validation census (298 orders) plus the calibration set. |
| `cowork-blind-v1` | First independent blind validation run (superseded — see `mayer-price-validation/archive/`). |
| `cowork-blind-v2` | Final independent blind validation run — this is what the published AUC (0.7836) is computed from. |
| `cowork-extension-stream-a` | Full-corpus extension, FDR and Truman (1936–1953). |
| `cowork-extension-stream-b` | Full-corpus extension, Eisenhower through the present. |

For a single "what's the current best score for this order" view, prefer `claude-church-bells-v1` where it exists (richest justification, part of the validated sample), and one of the two extension coders otherwise — the two extension streams never overlap with each other or with the primary coding, so there's no real conflict to resolve.
