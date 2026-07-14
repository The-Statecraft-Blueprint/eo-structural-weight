# Stream A — FDR & Truman (1936–1953)

One of two independent, non-overlapping coding streams that make up the full-corpus extension (see `../README.md` for the combined picture). This stream covers Franklin D. Roosevelt (1936–1945, the in-scope portion of his presidency) and Harry S Truman (1945–1953) — 3,032 orders, coded independently of Stream B and cross-checked against it for overlap (none found).

## Files

| File | Description |
|---|---|
| `batch-01-fdr-1936.json` through `batch-08-fdr-1943-1945.json` | FDR, one batch per year (1943–1945 combined, since order volume drops sharply as the war winds down and his term ends). |
| `batch-09-truman-1945-1946.json` through `batch-11-truman-1950-1953.json` | Truman, three batches spanning his presidency. |
| `notable-patterns-log.md` | Cross-order patterns, template identifications, and diff-aware findings surfaced while coding this stream — coding-convention decisions are also logged here for auditability (e.g., how Taylor Grazing Act land-designation orders were treated for Flag 6). |

## Record format

Each batch file is a JSON array of coding records. Each record has `eo_number`, `title`, `date_signed`, `president`, `flags` (array of 11, each with flag number, name, status, points, justification, and whether the Zombie Emergency Trap sub-flag fired), plus the aggregated `applicable_count` / `raw_score` / `max_possible` / `normalized_score` / `structural_weight_pct`.

## Provenance

Coded by an independent Claude Cowork instance working from `../../methodology/` (unredacted — no blinding concern applies to extension coding) and `../../database/corpus-texts/` for source text and predecessor lookups. Full justification depth throughout, not a rapid-throughput pass — see `../README.md` for why that choice was made.
