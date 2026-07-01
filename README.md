# EO Structural Weight Score

A rule-based, pre-registered measure of how much governance-architecture machinery a given executive order deploys.

---

## What this is

Existing political science measures of executive order significance — most notably Mayer (1999), Mayer & Price (2002), Howell (2003), and Chiou & Rothenberg (2017) — classify orders by political importance or policy significance. Those classifications require subjective judgment, which limits reproducibility and auditability.

This project replaces the importance judgment with a structural audit. Eleven standing governance-architecture flags are applied to each order's text. Each flag either fires or doesn't, and fires at one of two severity levels. The result is a continuous structural-weight score per order: how much governance machinery does this EO deploy, regardless of its political salience?

The measure is designed for a specific purpose: testing whether EO structural weight rises as legislative gridlock rises — the "exhaust gauge" prediction of the engine model of legislative dysfunction developed in *Why Do You Think the Government Doesn't Work?* (Statecraft Blueprint). When the legislative cylinder misfires and gridlock rises, unilateral executive action rises to fill the vacuum. The signal is in the structural weight of the orders, not the raw count — raw EO counts trend downward since the mid-20th century even as gridlock rises, which is why a weighted measure is necessary.

This is the methodological home for that measure. Results, once produced, will be published through [Church Bells](https://ringthebells.org), the Statecraft Blueprint's nonpartisan legislation analysis project.

---

## What makes this different from existing measures

**Rule application, not judgment.** "Does the Bundling flag fire?" is answerable by reading the text against a written definition. "Is this order significant?" is not. The structural-weight score is designed so two coders reading the same order should reach substantially the same score.

**Pre-registered.** The scoring scheme — which flags count, how severity maps to points, how scores aggregate — is committed to this repository before any executive order is coded and before the scores are compared to gridlock data. The scheme cannot be adjusted after coding begins without creating a new version with documented reasoning and a gap in the coding timeline.

**Governance-architecture specific.** The eleven flags measure what an order does to the structural fabric of governance: whether it concentrates power, creates accountability gaps, preempts oversight, establishes perverse incentives, cannibalizes existing agency mandates, and so on. This is a different question from political significance, and it produces a different and complementary measure.

**Validates against, then extends, the established literature.** The scoring scheme is applied to EOs already coded by Howell and/or Chiou & Rothenberg before it is extended into the modern period. If the structural-weight score cannot reproduce the established significance rankings within a defined margin (AUC ≥ 0.70), the scheme is reviewed before extension proceeds. Validation earns the right to extend.

---

## The eleven flags

Defined in full in [`church-bells-flags-canonical.md`](church-bells-flags-canonical.md).

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

Each flag is scored ABSENT (0), PRESENT (1), or CRITICAL (2) per order. NOT APPLICABLE flags are excluded from the score. The normalized structural-weight score is raw points divided by maximum possible points across applicable flags, producing a 0–1 scale.

---

## Repository contents

### Pre-registration documents *(committed before any EO is coded)*

| File | Description |
|------|-------------|
| [`church-bells-flags-canonical.md`](church-bells-flags-canonical.md) | Authoritative definitions for all eleven flags — operational tests, key distinctions, applicability notes |
| [`eo-structural-weight-scoring-scheme.md`](eo-structural-weight-scoring-scheme.md) | Complete scoring scheme — status vocabulary, score mapping, aggregation formula, validation design, inter-coder reliability protocol |

### Data *(added as project progresses)*

| Path | Description |
|------|-------------|
| `data/eo-corpus/` | Executive order texts downloaded from the American Presidency Project |
| `data/eo-index.csv` | Master index of all EOs in the corpus (EO number, title, date, president, Congress) |
| `data/binder-gridlock-1947-2022.csv` | Binder gridlock series, 80th–117th Congress |
| `data/eo-counts-app.csv` | Raw EO counts by president and term from the American Presidency Project |
| `data/coding/` | Per-EO coding records (flag statuses, justifications, scores) |

### Analysis *(added as project progresses)*

| Path | Description |
|------|-------------|
| `analysis/scrape-app-eos.py` | Scraper for bulk EO text download from the American Presidency Project |
| `analysis/score-eos.py` | Applies scoring scheme to coded EOs, produces score dataset |
| `analysis/validation.py` | Reproduces established significance codings, computes AUC |
| `analysis/gridlock-comparison.py` | Aggregates scores to Congress level, compares to Binder series |

---

## Order of operations (non-negotiable)

```
1. Freeze scoring scheme  ←  you are here
         ↓
2. Code validation sample (EOs already coded by Howell / Chiou & Rothenberg) [datasets requested]
         ↓
3. Run AUC validation — confirm structural weight reproduces established rankings
         ↓
4. Extend coding to full corpus (1949–present)
         ↓
5. Aggregate to Congress level
         ↓
6. Compare to Binder gridlock series
```

Steps 5 and 6 do not begin before step 3 produces an AUC ≥ 0.70. The scoring scheme is not adjusted between steps 3 and 6.

---

## Data sources

| Source | Use |
|--------|-----|
| [American Presidency Project](https://www.presidency.ucsb.edu) | EO full text, 1826–present |
| [Comparative Agendas Project](https://www.comparativeagendas.net) | EO policy topic coding, 1945–2025 |
| Binder (2003; updated 2025) | Gridlock series, 80th–117th Congress (1947–2022) |
| Howell (2003) | Significance coding, validation sample |
| Chiou & Rothenberg (2017) | Significance coding, validation sample |

---

## Relationship to other projects

This repository is a standalone methodological project. It is connected to two larger efforts:

**Church Bells** ([ringthebells.org](https://ringthebells.org)) — the nonpartisan governance monitoring project that publishes structural analysis of executive orders and legislation using the eleven-flag methodology. The EO Structural Weight Score formalizes and quantifies what Church Bells briefs do qualitatively.

**The Statecraft Blueprint** ([statecraftblueprint.org](https://statecraftblueprint.org)) — the broader governance reform project within which the engine model of legislative dysfunction was developed. The structural-weight vs. gridlock hypothesis tests one of that model's empirical predictions.

The flag definitions in this repository are authoritative for both Church Bells brief work and this scoring project. Changes to the flags require a new version of `church-bells-flags-canonical.md` with documented reasoning, and a corresponding update to the scoring scheme.

---

## Citation

If you use the flag definitions, scoring scheme, or data produced by this project, please cite:

> Tanium, Jason. *EO Structural Weight Score* (v1.0). Church Bells / The Statecraft Blueprint, June 2026. https://github.com/jtanium/eo-structural-weight

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — You are free to use, adapt, and build on this work with attribution, under the same license.

---

## Contact

Jason Tanium · [ringthebells.org](https://ringthebells.org) · [statecraftblueprint.org](https://statecraftblueprint.org)
