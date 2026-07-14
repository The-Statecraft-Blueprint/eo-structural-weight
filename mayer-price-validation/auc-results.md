# AUC Validation Results

*Computed 2026-07-06 against the blind coding run in `blind-coding-results.json`. This document is the evidentiary basis for the project's Step 2 validation claim; see `../methodology/scoring-scheme.md`, Step 2 Amendment (v1.4), for why this specific computation — rather than the primary label-aware coding — is what counts as the validation test.*

---

## Headline result

**AUC = 0.7836**, computed on all 297 blind-coded orders against their true Mayer & Price (2002) classification (positive = appears in the published appendix; negative = drawn from the general population).

This clears the pre-registered threshold of AUC ≥ 0.70 set before any coding began (`scoring-scheme.md`, Validation Design), and improves on an earlier full-corpus run (AUC = 0.7662) after a bug in the blind-coding package's reference material was found and fixed — see "How this number was reached" below for the full trajectory.

Verified two independent ways:
- Manual rank-sum (Mann-Whitney U equivalent) computation
- `sklearn.metrics.roc_auc_score`

Both return 0.7836 to four decimal places.

## Class separation

| | Mean | Median |
|---|---|---|
| Positive class (n=148) | 19.19% | 18.2% |
| Negative class (n=149) | 6.03% | **0.0%** |

All 297 orders received a defined score in this run — including EO 9681, which has no published text and was undefined in the prior run. The blind coder handled the missing text explicitly, scoring only the three decision-structure flags (which remain answerable from the title alone) and marking the rest NOT_APPLICABLE with that limitation stated, rather than leaving the order unscored.

## Accounting: why 297, not 298

The full validation corpus is 298 orders (149 positive, 149 negative). One is excluded from this computation, disclosed in advance:

- **EO 9981** — excluded from the blind batch entirely. It's used as a named, repeated worked example in `flags-canonical.md` (the calibration anchor for the CRITICAL threshold), so a blind coder scoring it would effectively be shown the answer by the reference material it's required to read. See `blind-coding-package/README.md` for the full exclusion rationale.

**Combined figure, if wanted:** folding EO 9981 back in using the primary coder's original (label-aware) score for that one order gives AUC = 0.7846 across 298 orders. The difference from the clean 297-order figure is negligible, which is reassuring in itself, but the 297-order blind figure is the one that demonstrates independence from label awareness and should be treated as the primary result.

---

## How this number was reached

The AUC did not arrive in one pass. Documenting the trajectory here rather than only reporting the final figure, because the process is itself part of the evidence that this result reflects careful, independently-verified work rather than a number that happened to clear a threshold.

### Step 1: First full-corpus blind run — AUC = 0.7662

The independent coder (Claude Cowork) completed all 297 orders against the v4 blind-coding package. Full structural and math audit at the time found the run clean: no duplicates, all 297 records with 11 flags each, zero arithmetic inconsistencies on independent recomputation. One data-labeling issue was found and disclosed (order-285 and order-286 had transposed `eo_number` values — content was correct, position labels were swapped; had no effect on the AUC since scoring was matched by EO number, not position). Zombie Emergency Trap fired on exactly the four orders identified independently in the primary coding (EO 11796, 11810, 11940, 12730). This run and its full audit trail are preserved in `archive/blind-coding-results-v1-20260705.json` for the record.

### Step 2: A bug found after the fact, in the reference material — not the scoring

Auditing the v4 `referenced-predecessors/` folder (built by a recursive backward citation walk) turned up a logic error: any predecessor order that happened to *also* be one of the 298 validation-sample orders was incorrectly treated as already covered and excluded from the reference folder, even when something else in the batch cited it as an amendment target. **51 citations were dropped this way.**

This was not a silent failure in the delivered scoring. The coding conventions require the blind coder to disclose, per flag, when a cited predecessor isn't recoverable rather than guess at its contents — and that's exactly what happened. The clearest example: EO 11190 (which revokes EO 10651) scored 25.0% in the v1 blind run, against 35.7% in the primary coder's original pass, entirely because Flags 2 and 7 could not be assessed — the coder's own justification stated plainly that EO 10651 "was not recoverable in the referenced-predecessors folder."

The folder was corrected (561 → 612 reference files) and the full corpus re-coded fresh against it.

### Step 3: Second full-corpus blind run — AUC = 0.7836

Same coder, same package apart from the corrected reference folder, full 297 orders coded again from scratch (not just the affected subset, to keep every order coded against consistent reference material). Same structural and math audit run again: clean, 297/297, zero arithmetic inconsistencies, and this time no position-label swap either. Zombie Emergency Trap again fired on exactly the same four orders (11796, 11810, 11940, 12730) — the third independent confirmation of that specific pattern across two blind runs and the original primary coding.

**What actually changed, checked directly rather than assumed:**

Of the 23 orders in the batch that cite one of the 51 previously-unavailable predecessors, 12 increased, 5 decreased, 6 were unchanged (average change: +3.2 percentage points). Spot-checking individual cases against their flag-level justifications shows the changes are a mix of two distinct things, worth telling apart:

- **Genuine fix effects.** EO 9296 moved from 10.0% to 35.0%. Its new Flag 7 justification: *"EO 9001 Title II Para 1 required 'all contracts... shall be reported to the President... at least quarterly'; this order replaces that mandatory presidential reporting with mere[ly discretionary disclosure].*" That is the same finding logged independently in the primary coding's notable-findings log (the "quiet regression" pattern) — rediscovered here with no access to that log, purely because EO 9001's text became available for the comparison the diff-aware convention calls for. EO 11190 moved only modestly (25.0% → 27.3%), but the reasoning underneath changed substantially: Flags 2, 4, and 7 now explicitly cite the diff against EO 10651, while Flags 5, 8, and 11 — previously NOT_APPLICABLE for lack of the comparison — resolved to definitive ABSENT rather than PRESENT. The fix made the finding possible; it didn't guarantee the finding would be large.
- **Ordinary re-coding variance, unrelated to the fix.** EO 9279 moved from 59.1% to 40.9%, the largest decrease in the batch. None of its four changed flags reference a predecessor comparison — every one is the coder revising its own read of the order's own text (for instance, reversing an earlier judgment that tying an order's duration to "termination of Title I of the First War Powers Act" doesn't count as a real sunset mechanism). This is the kind of variance that would show up in any two independent codings of the same order, fix or no fix, and shouldn't be attributed to the reference-folder correction.

The direction of the aggregate change (net positive) is consistent with the theoretical expectation that a bug causing *missing* findings can only pull scores toward zero, never away from it — but the specific size of any individual order's movement reflects both the fix and ordinary independent judgment, and the two shouldn't be conflated order by order.

---

## Supporting evidence for coding quality (current run)

**Zero math inconsistencies** across all 297 records, independently recomputed from the underlying 11 flag judgments.

**Flag-usage statistics, full corpus (3,267 flag judgments across 297 orders):**

| Status | Count | % |
|---|---|---|
| ABSENT | 1,893 | 57.9% |
| NOT_APPLICABLE | 633 | 19.4% |
| PRESENT | 706 | 21.6% |
| CRITICAL | 35 | 1.1% |

CRITICAL remains appropriately rare. NOT_APPLICABLE usage dropped from 25.0% to 19.4% relative to the v1 run — consistent with fewer flags being defaulted to NA for lack of comparison material, now that more of it is available.

**Zombie Emergency Trap fired exactly 4 times**, on EO 11796, EO 11810, EO 11940, and EO 12730 — identical to both the v1 blind run and the original primary coding. Three independent codings (one label-aware, two blind, on different reference material) landing on exactly the same four orders is strong evidence this is a genuine textual feature of the export-control continuation chain, not an artifact of any single reading.

**Earlier inter-coder reliability pilot.** A 30-order sample was independently double-coded by two additional models (Gemini and an early GPT-5.5 variant, two runs each) before the full corpus was coded. Retained in `../database/eo_coding.db` under coder IDs `gemini-2.5-collaborator`, `gemini-2.5-flash`, `gpt-5.5-thinking-v1`, and `gpt-5.5-thinking-v2` — included for completeness, not as validation evidence on its own.

## How the blind coding package evolved

1. **v1** — initial package: label-blind, randomized presentation order (seed `20260705`), redacted methodology extract.
2. **v2** — after a 20-order pilot found the Zombie Emergency Trap sub-flag over-firing relative to established practice, `flags-canonical.md`'s ZET test was narrowed to require an explicit, acknowledged statutory lapse rather than any authority merely derived from an active emergency statute.
3. **v3** — after a pilot showed that scoring an amending order with no way to see what it actually changed produces a different, usually understated score, `referenced-predecessors/` was added: reference-only text (not scored) for orders cited elsewhere in the batch as amended, revoked, or superseded.
4. **v4** — `referenced-predecessors/` rebuilt as a recursive backward citation walk, growing from 252 to 561 reference files. Documented limit, unresolved by design: this can only discover *older* material a text actually names, not a more recent intermediate amendment that isn't cited (found via a separate pilot on EO 11098).
5. **v4 (corrected)** — the 51-citation exclusion bug described above fixed; folder grew to 612 files. This is what the current 0.7836 result was coded against.

## Reproducing this result

```python
import json, csv
from sklearn.metrics import roc_auc_score

with open('blind-coding-results.json') as f:
    records = json.load(f)

answer_key = {}
with open('validation-key.csv') as f:
    for row in csv.DictReader(f):
        answer_key[row['eo_number']] = row['validation_class']

scores, labels = [], []
for r in records:
    pct = r.get('structural_weight_pct')
    if pct is None:
        continue
    scores.append(pct)
    labels.append(1 if answer_key[r['eo_number']] == 'positive' else 0)

print(roc_auc_score(labels, scores))  # 0.7836
```

The prior run (AUC = 0.7662) can be reproduced the same way against `archive/blind-coding-results-v1-20260705.json`.
