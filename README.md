# EO Structural Weight Score

A rule-based, pre-registered measure of how much governance-architecture machinery a given executive order deploys — validated by independent blind coding against Mayer & Price's (2002) significance classification, **AUC = 0.7662**.

---

## What this is

Existing political science measures of executive order significance classify orders by political importance or policy significance. Those classifications require subjective judgment, which limits reproducibility and auditability.

This project replaces the importance judgment with a structural audit. Eleven standing governance-architecture flags are applied to each order's text. Each flag either fires or doesn't, and fires at one of two severity levels. The result is a continuous structural-weight score per order: how much governance machinery does this EO deploy, regardless of its political salience?

This repository is the methodological home for that measure: the frozen scoring rules, the coded data, and the validation evidence. Results, as they're produced, are published through [Church Bells](https://ringthebells.org), the Statecraft Blueprint's nonpartisan legislation and executive-action analysis project.

---

## Status

**Validation complete.** The full 298-order Mayer & Price (2002) validation sample (149 positive-class orders from their published appendix, 149 negative-class orders drawn at random from the general population, seed disclosed) has been coded twice: once by the primary coder with full context, and once by an independent coder blind to every order's class, presentation order randomized, working from a redacted methodology extract. The blind pass is what the AUC claim rests on. See [`validation/auc-results.md`](validation/auc-results.md) for the full computation and every check run against it before it was trusted.

Extension to the full corpus is the next phase.

---

## What makes this different from existing measures

**Rule application, not judgment.** "Does the Bundling flag fire?" is answerable by reading the text against a written definition. "Is this order significant?" is not. The structural-weight score is designed so two coders reading the same order should reach substantially the same score — and now there's a full-corpus independent test of exactly that.

**Pre-registered.** The scoring scheme — which flags count, how severity maps to points, how scores aggregate — was committed to this repository before any executive order was coded. Changes after coding began are documented as dated amendments rather than silent edits; see the version history inside [`methodology/scoring-scheme.md`](methodology/scoring-scheme.md) and [`methodology/flags-canonical.md`](methodology/flags-canonical.md).

**Governance-architecture specific.** The eleven flags measure what an order does to the structural fabric of governance: whether it concentrates power, creates accountability gaps, preempts oversight, establishes perverse incentives, cannibalizes existing agency mandates, and so on. This is a different question from political significance, and it produces a different and complementary measure — see [`findings/notable-findings.md`](findings/notable-findings.md) for documented cases where the two diverge in both directions.

**Validated by independent blind coding before extension.** The scoring scheme was applied to the full Mayer & Price (2002) census, then re-coded from scratch by an independent, label-blind coder before any claim about discriminative validity was made. Validation earns the right to extend, not the other way around.

**Explicit about its own scope boundary.** The instrument measures architecture, not substantive fairness or policy wisdom. A precisely drafted, substantively troubling policy can score low, and that's a feature of what's being measured, not a flaw — see "What This Scheme Does Not Do" in `scoring-scheme.md`.

---

## The eleven flags

Defined in full in [`methodology/flags-canonical.md`](methodology/flags-canonical.md).

| # | Flag |
|---|------|
| 1 | Power Concentration |
| 2 | Accountability Gaps |
| 3 | Bundling |
| 4 | Vague Enforcement |
| 5 | Perverse Incentives *(sub-flag: Zombie Emergency Trap)* |
| 6 | Sunset Provisions *(absence of)* |
| 7 | Preemption of Oversight |
| 8 | Third-Party Incentive Gaps |
| 9 | Second/Third-Order Effects |
| 10 | Inter-Agency Cannibalization |
| 11 | Exemptions Architecture |

Each flag is scored ABSENT (0), PRESENT (1), or CRITICAL (2) per order. NOT APPLICABLE flags are excluded from both the numerator and denominator. The normalized structural-weight score is raw points divided by maximum possible points across applicable flags.

---

## Repository contents

### `methodology/` — pre-registration documents, frozen before coding

| File | Description |
|------|-------------|
| [`flags-canonical.md`](methodology/flags-canonical.md) | Authoritative definitions for all eleven flags — operational tests, key distinctions, applicability rules. Currently v1.2.2. |
| [`scoring-scheme.md`](methodology/scoring-scheme.md) | Complete scoring scheme — status vocabulary, score mapping, aggregation formula, validation design, blind-coding independence requirements. Currently v1.4. |

### `data/`

| File | Description |
|------|-------------|
| `mayer-price-2002-appendix.csv` | The 149 positive-class orders, resolved from Mayer & Price's (2002) published appendix |
| `mayer-price-2002-appendix-provenance.md` | How the appendix list was reconciled into a clean, citable dataset |
| `negative-sample-v1.csv` | The 149 negative-class orders, random draw, seed `20260703` |
| `calibration-record.md` | The initial 10-order calibration set coded before the full validation batch began |
| `eo_coding.db` | SQLite database with every coding record, distinguished by `coder_id`: `claude-church-bells-v1` (primary, label-aware), `cowork-blind-v1` (independent blind validation), plus an earlier 30-order inter-coder reliability pilot under four additional coder IDs |

### `validation/` — the evidence for the AUC claim

| Path | Description |
|------|-------------|
| [`auc-results.md`](validation/auc-results.md) | **Start here for the validation claim.** The computation, every integrity check run against it, and how to reproduce it. |
| `blind-coding-results.json` / `.csv` | The independent blind coder's raw, complete output — 297 orders, unmodified |
| `validation-key.csv` | Maps each blind-batch position to its real EO number and true Mayer & Price class. Kept confidential during blind coding; published now that coding is complete, so the AUC result is independently checkable. |
| `blind-coding-package/` | Exactly what was given to the blind coder: task instructions, the redacted methodology extract, the 297-order text batch in randomized order, and 561 reference-only predecessor texts for orders that amend or revoke something earlier |

### `findings/`

| File | Description |
|------|-------------|
| [`notable-findings.md`](findings/notable-findings.md) | Qualitative results from the primary coding pass: named recurring patterns (the Zombie Emergency Trap continuation chain, quiet regression/strengthening, the no-private-right-of-action drafting convention, and others), a divergence index of orders where structural weight and historical significance diverge, and the methodological lessons that shaped `scoring-scheme.md`'s coding conventions. **This is exploratory material, not validation evidence** — see `validation/` for that. |

---

## Order of operations

```
1. Freeze scoring scheme
         ↓
2. Code the full Mayer & Price (2002) validation sample (298 orders)         ✓ complete
         ↓
3. Re-code independently, blind to class label — run AUC validation          ✓ complete — AUC = 0.7662
         ↓
4. Extend coding to the full corpus (1936–present)                          ← next
```

The scoring scheme (flag definitions and confidence taxonomy) remains frozen through the extension, to avoid fitting the instrument to a corpus it was validated on rather than the one it's meant to generalize to.

---

## Data sources

| Source | Use |
|--------|-----|
| [American Presidency Project](https://www.presidency.ucsb.edu) | EO full text, 1826–present |
| Mayer, K. R., & Price, K. (2002). "Unilateral Presidential Powers: Significant Executive Orders, 1949-99." *Presidential Studies Quarterly* | Positive-class significance classification, validation sample |
| [Comparative Agendas Project](https://www.comparativeagendas.net) | EO policy topic coding, 1945–2025 — for future extension work, not yet used |

---

## Relationship to other projects

**Church Bells** ([ringthebells.org](https://ringthebells.org)) — the nonpartisan governance monitoring project that publishes structural analysis of executive orders and legislation using the eleven-flag methodology. The EO Structural Weight Score formalizes and quantifies what Church Bells briefs do qualitatively.

**The Statecraft Blueprint** ([statecraftblueprint.org](https://statecraftblueprint.org)) — the broader governance reform project this measure supports.

The flag definitions in this repository are authoritative for both Church Bells brief work and this scoring project. Changes to the flags require a new version of `flags-canonical.md` with documented reasoning, and a corresponding update to `scoring-scheme.md`.

---

## Citation

If you use the flag definitions, scoring scheme, or data produced by this project, please cite:

> Edwards, Jason. *EO Structural Weight Score* (v1.4). Church Bells / The Statecraft Blueprint, 2026. https://github.com/The-Statecraft-Blueprint/eo-structural-weight

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — You are free to use, adapt, and build on this work with attribution, under the same license.

---

## Contact

Jason Edwards · [ringthebells.org](https://ringthebells.org) · [statecraftblueprint.org](https://statecraftblueprint.org)
