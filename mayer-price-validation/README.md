# Mayer & Price Validation

*Everything related to validating the EO Structural Weight Score against Mayer & Price's (2002) executive order significance classification — the data it was built from, how the blind test was run, what the result means, and how to reproduce all of it.*

## Who Mayer & Price are, and why we validate against them

Mayer, K. R., & Price, K. (2002), "Unilateral Presidential Powers: Significant Executive Orders, 1949–99," *Presidential Studies Quarterly*, is the field's standard reference classification of which executive orders mattered. It's built on expert judgment: political scientists read the historical record and flagged 149 orders as "significant." That's a real, valuable measure — and a fundamentally different kind of measure than a structural audit.

The EO Structural Weight Score asks a different question: not *was this order politically consequential*, but *how much unreviewed discretion, unaccountable authority, or structurally risky machinery does this order's text deploy*, independent of how much attention it got. Those two questions are related — architecture and consequence often travel together — but they're not the same question, and an instrument that only measures one of them can't tell you when they come apart.

Validating against Mayer & Price answers a specific, falsifiable question: **does a rule-based structural reading of the text reconstruct expert judgment about significance, well enough to trust it as a signal on its own?** The answer is yes (AUC = 0.7836), and the 22% it doesn't reconstruct is where the two measures are actually telling you different things — see `comparison-to-mayer-price.md` for exactly where and why.

## The validation sample

298 orders: **149 positive-class** (Mayer & Price's published appendix, resolved into a clean CSV — see `source-data/mayer-price-2002-appendix-provenance.md` for exactly how) plus **149 negative-class** (a random draw from the general population of executive orders, seed `20260703`, disclosed for reproducibility). Full detail in `source-data/README.md`.

## How the validation actually worked

**Two coding passes, only one of which counts as validation evidence.**

1. **Primary coding** — the full 298-order sample coded with full context, including which orders were Mayer & Price-positive. Rich, useful for finding qualitative patterns (see `../findings/`), but *not* valid as a test of the instrument's discriminative power, since the coder knew the labels while coding.

2. **Independent blind coding** — a separate coder, with no access to class labels, no access to the primary coder's prior work, working through the 297 orders (EO 9981 excluded — it's a named calibration example in the flag definitions themselves, so including it would leak the answer) in randomized presentation order, from a redacted methodology extract. **This is what the AUC is computed from.** The complete package given to that coder — task instructions, redacted rules, the randomized text batch, reference material for predecessor orders — is preserved in full in `blind-coding-package/`, so the exact conditions of the test are reproducible, not just described.

The blind package went through four real revisions, each driven by a specific pilot finding rather than a hypothetical concern (a sub-flag firing too broadly; an amending order that couldn't be scored correctly without seeing what it amended; a bug in how that reference material was built). The full trajectory — including a full run that was later superseded after a bug was found — is documented in `auc-results.md`.

## The result

**AUC = 0.7836**, verified two independent ways (manual rank-sum calculation and `sklearn.metrics.roc_auc_score`, matching to four decimal places). Full computation, every integrity check run against it, the complete revision trajectory, and known limitations: **[`auc-results.md`](auc-results.md)**.

**Where this stands relative to Mayer & Price specifically — what matches, what diverges, and why the divergences are legible rather than noise**, with supporting charts: **[`comparison-to-mayer-price.md`](comparison-to-mayer-price.md)**.

## Reproducing this

Everything needed is in this folder:

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

To reproduce the *coding itself* rather than just the statistic — i.e., run a fresh independent blind pass — everything a new coder needs is in `blind-coding-package/`: task instructions, the redacted scoring rules, the 297-order text batch, and 612 reference-only predecessor texts. `source-data/` and `../database/corpus-texts/` together contain the full text and provenance for every order in the sample, in case the source needs independent verification against the primary record.

## Files in this folder

| Path | Description |
|---|---|
| `source-data/` | The Mayer & Price appendix, the negative sample, provenance, the pre-validation calibration set, and Policy Agendas Project background data. |
| `primary-coding/` | The original 307 raw per-EO JSON coding files produced by the primary coder — `eo_coding.db`'s `claude-church-bells-v1` rows are built from these. |
| `icr-pilot/` | An earlier, smaller-scale inter-coder reliability pilot (30 orders, Gemini and GPT-5.5 variants) that predates the full 298-order validation sample — a precursor check, not validation evidence in its own right. |
| `auc-results.md` | The full computation, integrity checks, and revision trajectory. |
| `comparison-to-mayer-price.md` | Where structural weight agrees and diverges with Mayer & Price, with charts. |
| `validation-key.csv` | Maps each blind-batch position to its real EO number and true class. Confidential during coding; public now that coding is complete. |
| `blind-coding-results.json` / `.csv` | The independent blind coder's raw, complete output — current run. |
| `blind-coding-package/` | Exactly what was given to the blind coder, preserved in full. |
| `archive/` | The superseded first blind run, kept for the record. |
