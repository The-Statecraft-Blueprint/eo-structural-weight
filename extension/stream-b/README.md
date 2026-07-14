# Stream B — Eisenhower to Present (1953–2026)

One of two independent, non-overlapping coding streams that make up the full-corpus extension (see `../README.md` for the combined picture). This stream covers every administration from Eisenhower through the present — 3,812 orders, coded independently of Stream A and cross-checked against it for overlap (none found).

## Files

| File | Description |
|---|---|
| `batch-01-eisenhower.json` through `batch-14-trump2.json` | One batch per administration. Trump's second term (`batch-14-trump2.json`) is the only one still accumulating new orders as of this writing. |
| `notable-patterns-log.md` | Batch 1 (Eisenhower) findings. |
| `notable-patterns-log-batch{02–14}-{admin}.md` | One log per subsequent batch, same conventions — cross-order patterns, template identifications, diff-aware findings, and coding-convention decisions, each cross-referencing earlier logs where a pattern extends or echoes something already named. |

## Record format

Each batch file is a JSON array of coding records. Each record has `eo_number`, `title`, `date_signed`, `president`, `flags` (array of 11), plus the aggregated score fields. A small number of records store `flags` as an object keyed by flag number rather than an array — both are valid and were normalized during consolidation into `../../database/eo_coding.db`; if you're parsing these files directly, handle both shapes.

## Provenance

Coded by an independent Claude Cowork instance working from `../../methodology/` (unredacted — no blinding concern applies to extension coding) and `../../database/corpus-texts/` for source text and predecessor lookups. Full justification depth throughout. The per-batch logs document real self-caught and corrected errors as coding progressed (denominator miscounts, a template-transfer error, a database journal-mode infrastructure issue) — worth reading as evidence of active quality control, not just narrative color.
