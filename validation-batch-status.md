# Validation Batch Status — Mayer & Price (2002) Cross-Validation

*As of 2026-07-03. Batch ID: `mayer-price-2002-v1`. See `eo-structural-weight-scoring-scheme.md` v1.1, Step 2 Amendment, for full design.*

## Progress

| Class | Total | Coded | Remaining |
|---|---|---|---|
| Positive (Mayer & Price appendix) | 149 | 4 | 145 |
| Negative (random draw, seed 20260703) | 149 | 3 | 146 |
| **Total** | **298** | **7** | **291** |

Of the 4 positives coded, 2 (9981, 10924) were completed earlier as part of the calibration set and carry forward directly — no re-coding needed, since the positive class is a census, not a fresh draw. 2 (7856, 8233) plus all 3 negatives (7329, 7344, 7392) were coded fresh this session to confirm the pipeline end-to-end: template generation → text retrieval → 11-flag coding with justifications → import → score computation.

## Scores so far

| EO | Class | Structural weight | Notes |
|---|---|---|---|
| 9981 | positive | 25.0% | Calibration Tier 2 |
| 10924 | positive | 12.5% | Calibration |
| 7856 | positive | 20.0% | Passport rules — moderate weight, driven by undefined Secretary discretion |
| 8233 | positive | 0.0% | Wartime interagency neutrality enforcement — clean jurisdictional division |
| 7329 | negative | 0.0% | Land acquisition (Petersburg NMP) |
| 7344 | negative | 0.0% | Land withdrawal revocation (Colorado) |
| 7392 | negative | 0.0% | Land withdrawal revocation (Oregon) |

Early and not indicative of anything yet at n=7 — flagged here only to confirm the scoring mechanism is producing sensible, differentiated output (e.g., EO 8233 scoring 0% despite being a Mayer & Price positive is exactly the kind of divergence the pre-registration's "Divergence analysis" section anticipates and wants surfaced, not smoothed over).

## What remains

291 EOs still need the same treatment: template generation, text read, 11-flag coding with per-flag justification, import. At the pace demonstrated this session, this is realistically a multi-session undertaking — each EO in this batch takes genuine analytical work, not a mechanical pass, and EO length varies enormously (this batch alone ran from ~75 words to ~7,800 words).

**This is a pacing decision worth making explicitly rather than defaulting into:** options include (a) continuing in fixed-size batches across future Church Bells sessions, (b) splitting the batch across the multi-AI workflow (Gemini/ChatGPT already used for review — could take a coding pass on a subset, then reconciled against the inter-coder reliability protocol already in the scoring scheme), or (c) some combination, e.g. Claude codes positives (need more architectural judgment given historical/legal context) while a faster pass handles negatives (many of which, like the three coded here, are short and low-complexity).

## Files

- `validation-queue.csv` — 291 remaining EOs (eo_number, class), ready to feed into `create_coding_template.py` in order.
- `negative-sample-v1.csv` — the frozen 149-EO negative draw, full record.
- Coding JSONs for all 7 in `codings/`.
- `eo_coding.db` updated with all 7 new scores in `eo_scores`.
