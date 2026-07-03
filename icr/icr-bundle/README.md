# Inter-Coder Reliability Bundle v1

*30 EOs, 10% of the 298-EO validation batch, per the pre-registered ICR protocol (scoring scheme, "Inter-Coder Reliability Protocol" section). Sample drawn 2026-07-04, seed 20260704 for the 23 new draws; 7 EOs already primary-coded by Claude carry forward as a head start. Full membership in `icr-sample-v1.csv`.*

## What to do with this

For **each** of ChatGPT and Gemini, separately:

1. Give it `00-CODING-PROMPT.txt` as the instruction.
2. Give it each `icr-template-{eo}.json` file one at a time (or in a batch, if the interface handles multi-file well) and ask it to return the completed JSON.
3. Set its `coder_id` to something identifying: e.g. `chatgpt-icr-v1` / `gemini-icr-v1`.
4. Save each returned JSON as `{eo_number}-{coder_id}.json` (matching the existing repo naming convention in `codings/`).

## Important — preserving blindness

Don't show either model the other's output, and don't show either model any of Claude's existing codings for the 7 head-start EOs (7856, 8233, 7329, 7344, 7392, 9981, 10924) before it codes them. The templates in this bundle are blank — they don't leak that information — so as long as you're pasting from this bundle rather than from the repo's `codings/` folder, you're fine.

## When you bring results back

Send me the completed JSONs (all 30 from each model, or however many you get back — partial is fine, we don't need all 60 to start looking at agreement). I'll:

- Code my own primary-coder version of the 23 EOs I haven't scored yet (without looking at ChatGPT's or Gemini's answers first)
- Import all codings under their respective `coder_id`s
- Run `import_coding.py --icr {eo_number}` per EO for the per-flag comparison
- Write the aggregation script to roll all 30 into an overall agreement rate against the pre-registered 80% threshold, and populate `icr_summary`
- Flag any EOs where disagreement exceeds "one level" (e.g. ABSENT vs. CRITICAL) for reconciliation by reference to the flag definitions, per protocol — not by averaging

## Files in this bundle

- `00-CODING-PROMPT.txt` — the standard prompt
- `icr-template-{eo}.json` × 30 — blank templates, full EO text embedded
- `icr-sample-v1.csv` — sample membership and provenance
