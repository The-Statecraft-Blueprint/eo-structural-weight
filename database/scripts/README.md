# Scripts

The tooling that builds and maintains `../eo_coding.db`. Run these to rebuild or extend the database — don't hand-edit it directly, per the source-of-truth principle in `../README.md`.

| Script | Purpose |
|---|---|
| `init_db.py` | Creates the database schema, including Congress-number mapping (`date_to_congress()`) for rolling scores up to Congress sessions. Run once before any other script, against a fresh database. |
| `import_coding.py` | Validates a completed JSON coding file and imports it, computing the structural-weight score on import. Supports single-file, batch (whole directory), and `--icr` (inter-coder report) modes. |
| `create_coding_template.py` | Generates a blank coding template for a given EO — the JSON shape `import_coding.py` expects. |
| `import_corpus_index.py` | Imports corpus metadata (title, date, president) independent of coding data. |
| `export_analysis.py` | Exports aggregated views from the database (e.g., the annual structural-weight series in `../../extension/annual-structural-weight.csv`). |
