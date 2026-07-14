# ICR Pilot

An early, small-scale inter-coder reliability check — 30 orders (`icr-sample-v1.csv`), independently coded by two additional models (Gemini and an early GPT-5.5 variant, two runs each) before the full 298-order Mayer & Price validation sample existed. Corresponds to the `gemini-2.5-collaborator`, `gemini-2.5-flash`, `gpt-5.5-thinking-v1`, and `gpt-5.5-thinking-v2` coder IDs in `../../database/eo_coding.db`.

## Files

| Path | Description |
|---|---|
| `icr-bundle/` | The task package given to the pilot coders — instructions, the 30-order sample, coding templates. |
| `icr-sample-v1.csv` | The 30-order sample itself. |
| `chatgpt_*.json`, `gemini_*.json` | Raw per-coder outputs. |
| `compute_icr_summary.py` | The agreement-statistics script. |
| `*.zip` | Zipped bundles of the same content above — check before assuming these add anything not already present unzipped. |

## What this is and isn't

This predates the frozen methodology's final form and the full validation sample — it's a precursor calibration check, useful for understanding how the rubric was pressure-tested early on, but it is not part of the AUC validation claim. That claim rests entirely on the independent blind pass documented in `../auc-results.md`.
