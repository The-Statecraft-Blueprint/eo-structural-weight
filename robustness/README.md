# Robustness

Checks on how far the project's claims hold up, and the tests still needed.

| File | What it is |
|---|---|
| [`AUDIT.md`](AUDIT.md) | What holds, what doesn't, and what is untested, across validation, divergence examples, reliability and the long-run trend. **Start here.** |
| `audit.py` | Reproduces every number in `AUDIT.md` from `../database/eo_coding.db` (numpy only). |
| `audit-output.json` | Full output of `audit.py`, including complete lists of robust and unstable examples. |
| `annual-series-rebuilt.csv` | Annual series built from extension and blind-v2 codings only (no label-aware scores), with zero-share, mean-if-nonzero and long-order columns. |
| [`masked-recode/`](masked-recode/) | Pre-registered masked re-coding test (recognition, administration-knowledge bias, reliability, coder seam) and the 80-item human hand-coding packet. |
| [`data-fixes.md`](data-fixes.md) | Log of corrections made to source data. |
