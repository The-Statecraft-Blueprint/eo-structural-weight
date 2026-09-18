# Human Hand-Coding Protocol (80 masked items)

This is the project's first human coding. It's the reliability anchor that the AI-to-AI agreement figures can't provide.

## Before you start

- **Don't open** `../_sealed/`, `../../../database/eo_coding.db`, any blind-run or extension results, or the notable-findings log until your sheet is finished. They show which order each item is and how it was scored before.
- Read `../coder-packet-masked/scoring-instructions.md` and `flags-canonical.md` in full, exactly as an AI coder would.
- If a second human coder is available (a student or colleague who didn't design the rubric), they're more valuable than a second pass by you. Have them code the same 80 items independently on a copy of the sheet named `human-coding-sheet-<initials>.csv`.

## Coding

- The items to code are the `item_id`s in `human-coding-sheet.csv`, in the order listed. Their texts are in `../coder-packet-masked/items/`.
- For each flag, enter `ABSENT`, `PRESENT`, `CRITICAL` or `NOT_APPLICABLE` in `fN_status`, and a short note citing the text in `fN_note`. A note is required for every `NOT_APPLICABLE`.
- Don't compute the score. `analyze.py` computes it from the statuses.
- Record `minutes_spent` for each item.
- Fill in the `AFTER_CODING_*` columns only after all 11 flags are done. If you recognized the order partway through reading it, say so. That still counts as recognized.
- Don't go back and change earlier items after you've seen later ones, except to fix a clear clerical error. If you make such a fix, note it in `general_notes`.

## Pace

At 10–20 minutes per item, 80 items take roughly 15–25 hours. A good split is about 10 items per sitting. Code the first 10, then re-read `flags-canonical.md` before continuing. Early items tend to drift the most.

## When you're done

Save the sheet, commit it, and only then run `python3 ../analyze.py`.
