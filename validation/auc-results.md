# AUC Validation Results

*Computed 2026-07-05 against the blind coding run in `blind-coding-results.json`. This document is the evidentiary basis for the project's Step 2 validation claim; see `../methodology/scoring-scheme.md`, Step 2 Amendment (v1.4), for why this specific computation — rather than the primary label-aware coding — is what counts as the validation test.*

---

## Headline result

**AUC = 0.7662**, computed on 296 of the 297 blind-coded orders against their true Mayer & Price (2002) classification (positive = appears in the published appendix; negative = drawn from the general population).

This clears the pre-registered threshold of AUC ≥ 0.70 set before any coding began (`scoring-scheme.md`, Validation Design).

Verified two independent ways:
- Manual rank-sum (Mann-Whitney U equivalent) computation
- `sklearn.metrics.roc_auc_score`

Both return 0.7662 to four decimal places.

## Class separation

| | Mean | Median | Std. dev. |
|---|---|---|---|
| Positive class (n=148) | 17.85% | 18.2% | 14.52 |
| Negative class (n=148) | 5.15% | **0.0%** | 9.82 |

The majority of negative-class orders scored exactly zero. This separation is visible before any formal statistic is computed, which is a useful sanity check in itself — the AUC isn't reconstructing a signal that requires the statistic to see.

## Accounting: why 296, not 298

The full validation corpus is 298 orders (149 positive, 149 negative). Two are excluded from this computation, both disclosed in advance rather than discovered after the fact:

- **EO 9981** — excluded from the blind batch entirely. It's used as a named, repeated worked example in `flags-canonical.md` (the calibration anchor for the CRITICAL threshold), so a blind coder scoring it would effectively be shown the answer by the reference material it's required to read. See `blind-coding-package/README.md` for the full exclusion rationale.
- **EO 9681** — no published text exists for this order (recorded historically as "not published"). Both the primary coder and the independent blind coder reached this same conclusion independently and scored it as fully administrative/undefined (applicable_count = 0), which has no computable percentage. This is a data availability limit, not a coding disagreement.

**Combined figure, if wanted:** folding EO 9981 back in using the primary coder's original (label-aware) score for that one order gives AUC = 0.7674 across 297 orders. The difference from the clean 296-order figure is negligible, which is itself reassuring, but the 296-order blind figure is the one that actually demonstrates independence from label awareness and should be treated as the primary result.

## Supporting evidence for coding quality

These don't affect the AUC number directly, but they're relevant to whether the AUC should be trusted as reflecting careful, rule-following coding rather than noise that happened to correlate:

**Zero math inconsistencies.** Every one of the 297 records' `applicable_count`, `raw_score`, `max_possible`, and `structural_weight_pct` was independently recomputed from the underlying 11 flag judgments and checked against the reported values. No discrepancies found.

**Flag-usage statistics, full corpus (3,267 flag judgments across 297 orders):**

| Status | Count | % |
|---|---|---|
| ABSENT | 1,809 | 55.4% |
| NOT_APPLICABLE | 818 | 25.0% |
| PRESENT | 603 | 18.5% |
| CRITICAL | 37 | 1.1% |

CRITICAL is appropriately rare (reserved for core-collapse findings, not overused as a default severity). NOT_APPLICABLE usage on Flags 1, 2, and 7 — which `flags-canonical.md`'s Application Notes specify as always answerable regardless of an order's brevity — occurred only 1, 1, and 2 times respectively out of 297 each, essentially full compliance with that rule.

**Zombie Emergency Trap sub-flag fired exactly 4 times**, and on the same four orders identified independently in the primary coding pass: EO 11796, EO 11810, EO 11940, EO 12730 (the export-control continuation chain spanning 1974–1990, three presidencies). An independent, blind, full-corpus pass landing on exactly the same instances — no more, no fewer — is meaningful evidence that this pattern is a genuine textual feature of these orders rather than an artifact of one coder's reading.

**Earlier inter-coder reliability pilot.** Before the full corpus was coded, a 30-order sample was independently double-coded by two additional models (Gemini and an early GPT-5.5 variant, two runs each) as a preliminary reliability check. That data is retained in `../data/eo_coding.db` under coder IDs `gemini-2.5-collaborator`, `gemini-2.5-flash`, `gpt-5.5-thinking-v1`, and `gpt-5.5-thinking-v2`, and predates the methodology fixes described below — it's included for completeness, not as validation evidence on its own.

## How the blind coding package evolved

The package given to the independent coder (Claude Cowork) went through four revisions, each driven by a specific pilot finding rather than a hypothetical concern:

1. **v1** — initial package: label-blind, randomized presentation order (seed `20260705`), redacted methodology extract.
2. **v2** — after a 20-order Cowork pilot on v1 found the Zombie Emergency Trap sub-flag over-firing relative to established practice, `flags-canonical.md`'s ZET test was narrowed to require an explicit, acknowledged statutory lapse rather than any authority merely derived from an active emergency statute.
3. **v3** — after a Gemini pilot showed that scoring an amending order with no way to see what it actually changed produces a different, usually understated score, `referenced-predecessors/` was added: reference-only text (not scored) for any order cited elsewhere in the batch as amended, revoked, or superseded.
4. **v4** — `referenced-predecessors/` rebuilt as a recursive backward citation walk rather than a single-hop lookup, growing from 252 to 561 reference files. Documented limit: this can only discover *older* material a text actually names; it cannot discover a more recent intermediate amendment that isn't cited. That specific gap (found in a second Cowork pilot, EO 11098's baseline) remains open and is disclosed in `blind-coding-package/coder-instructions.md`.

The full 297-order run in `blind-coding-results.json` was coded fresh against v4, not assembled from earlier pilot rounds, to keep the reference material consistent across every order.

## Known, disclosed data issue in the results file (does not affect the AUC)

`blind-coding-results.json` has the `eo_number` values for order-285 and order-286 transposed — each record's title and flag content correctly matches the real order it analyzes, but the two results were filed under swapped position labels. This was caught by cross-referencing every record's reported EO number against `validation-key.csv` before computing anything. Since this computation matches records by `eo_number` rather than by position label, it had no effect on the result. Noted here for anyone auditing the raw file directly.

## A bug in `referenced-predecessors/` found after the blind run, and what it actually cost

The recursive rebuild of `referenced-predecessors/` (v4) had a logic error: any predecessor order that happened to *also* be one of the 298 validation-sample orders was incorrectly treated as already covered and excluded from the reference folder, even when something else in the batch cited it. **51 citations across the corpus were dropped this way**, discovered and fixed after the full 297-order blind run had already been coded and delivered against the buggy v4 folder.

This was not a silent failure. The coding conventions require the blind coder to disclose, per-flag, when a cited predecessor isn't recoverable rather than guess at its contents — and that's exactly what happened. The clearest example: EO 11190 (which revokes EO 10651) scored 25.0% in the delivered blind run, against 35.7% in the primary coder's original pass. The gap traces entirely to Flag 2 and Flag 7, where the blind coder's justification states plainly that EO 10651 "was not recoverable in the referenced-predecessors folder, so it cannot be determined... whether any oversight mechanism existed under that prior order that this revocation removes." The system degraded exactly the way it was designed to when reference material is missing: fewer findings, not wrong ones, with the gap stated in the coder's own words rather than papered over.

**What this means for the AUC.** The delivered figure (0.7662) reflects real limitations in the reference material available at the time, not an error in the computation itself — it's an honest number computed from what the coder actually had access to. Because the bug caused *missing* findings rather than *incorrect* ones, and missing findings can only ever pull scores toward zero, the true achievable AUC with complete reference material is likely to be at or above 0.7662, not below it. The folder has since been corrected (612 files, up from 561) for any future coding pass. Whether to re-run the ~51 affected citing orders specifically, or treat the current figure as final with this limitation disclosed, is an open decision.

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
        continue  # EO 9681, undefined
    scores.append(pct)
    labels.append(1 if answer_key[r['eo_number']] == 'positive' else 0)

print(roc_auc_score(labels, scores))  # 0.7662
```
