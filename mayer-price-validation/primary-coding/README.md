# Primary Coding

The original, raw per-EO coding files produced by the primary coder (`claude-church-bells-v1`) — 307 files, one per order, named `{eo_number}-claude-church-bells-v1.json`. This is source data: `../../database/eo_coding.db`'s primary-coder rows are built from these files via `../../database/scripts/import_coding.py`, not the other way around.

This is the coding pass that had full context — including which orders were Mayer & Price-positive — while coding. It's rich and useful for qualitative pattern-finding (see `../../findings/`), but it is **not** validation evidence on its own, since label-awareness while coding is exactly what the independent blind pass (`../blind-coding-results.json`) was built to test for. See `../README.md` and `../auc-results.md` for that distinction in full.
