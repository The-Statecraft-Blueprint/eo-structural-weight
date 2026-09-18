# Masked Re-coding Test and Human Hand-Coding Packet

This folder tests whether the project's AI codings depend on the coder knowing *which* order it is scoring. It also supplies the project's first human codings. Read `ANALYSIS-PLAN.md` first. It fixes the hypotheses and decision rules before any data exists.

| Path | Who sees it |
|---|---|
| `coder-packet-masked/` (INSTRUCTIONS, rubric, `items/item-001…210.md`) | Masked-arm AI coders and human coders |
| `coder-packet-unmasked/` (INSTRUCTIONS, rubric, `items/order-001…210.md`) | Unmasked-arm AI coders only |
| `human-coding/` (protocol and the 80-item sheet) | Human coders |
| `_sealed/key.csv`, `_sealed/redaction-log.csv` | **No coder.** Only `analyze.py` reads them. |
| `results/arm-M/`, `results/arm-U/` | Coder outputs go here, one JSON file per coder per arm |
| `build_package.py` | Regenerates everything deterministically (seed 20260918) |
| `analyze.py` | Computes every statistic in the plan. Tested on simulated data before any real data existed. |

## Running an AI coder

1. Start a fresh session with no project context, memory or connected folders. Upload the contents of `coder-packet-masked/` and paste in `INSTRUCTIONS.md`.
2. Collect the JSON, validate that it parses, and save it as `results/arm-M/<coder-name>.json`.
3. In a separate fresh session with the same model, do the same with `coder-packet-unmasked/` and save it as `results/arm-U/<coder-name>.json`.
4. Record the model name and version string, run date and any problems in `results/RUN-LOG.md`.
5. Once all coders and the human sheet are in, run `python3 analyze.py > results/REPORT.txt`.

At 210 items, expect to need batches of 20–30 per response.

## Known limits of the masking

- Content itself can reveal era. Agency names (e.g. "Department of Homeland Security", "Department of War"), modern boilerplate ("This order is not intended to, and does not, create any right…"), and named people or events in the text all leak. The `after_coding` guesses measure how much leaks (H5), and the analysis reports AUC on unrecognized items separately.
- U.S. Code section numbers are left in place, since they're needed to judge authority.
- Neither arm gets predecessor texts. Masked-vs-unmasked comparisons are therefore clean, but comparisons with the existing blind-v2 scores (which had predecessors) mix masking with predecessor access. That's why the primary test is M vs U, not M vs blind-v2.
