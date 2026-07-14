# EO Structural Weight Score

A rule-based, pre-registered measure of how much governance-architecture machinery a given executive order deploys — validated by independent blind coding against Mayer & Price's (2002) significance classification, **AUC = 0.7836** — and applied to the full 1936–present corpus, **7,149 of 7,151 executive orders scored**.

**→ [How this compares to Mayer & Price's classification, and why we think it's a better tool for this specific question](mayer-price-validation/comparison-to-mayer-price.md)**

---

## What this is, and why it exists

Existing measures of executive order significance — Mayer & Price's being the field's standard reference — classify orders by political importance through expert judgment. That's a real and valuable measure. It's also fundamentally subjective: it can't be independently re-derived by someone else reading the same text, and it doesn't distinguish *how an order achieves what it does* from *how much it mattered that it did*.

This project replaces the importance judgment with a structural audit. Eleven standing governance-architecture flags — power concentration, accountability gaps, oversight preemption, and so on — are applied to each order's actual text. Each flag either fires or doesn't, at one of two severity levels. The result is a continuous structural-weight score per order, answering a different question than significance: *how much unreviewed discretion or unaccountable authority does this order deploy*, independent of how much attention it got.

The two questions are related but not identical, and that's the point. A landmark order can be architecturally clean (FISA implementation, EO 12139, scores 0%); a routine wartime order can be architecturally heavy (EO 9250, 45.5%, entirely outside Mayer & Price's sampling window). Measuring both separately is more informative than either alone — see the comparison link above for the full case, with specific examples in both directions.

This repository is the methodological home for that measure: the frozen scoring rules, every coded record, the validation evidence, and the full-corpus results. Findings, as they accumulate, are published through [Church Bells](https://ringthebells.org), the Statecraft Blueprint's nonpartisan legislation and executive-action analysis project.

---

## Status

**Validation complete.** The full 298-order Mayer & Price (2002) validation sample has been coded twice — once with full context, once by an independent coder blind to every order's class. The blind pass is what the AUC claim rests on. Start at [`mayer-price-validation/README.md`](mayer-price-validation/README.md).

**Full-corpus extension complete.** The validated methodology has been applied to the entire 1936–present corpus by two independent, non-overlapping coding streams, at full justification depth. Start at [`extension/README.md`](extension/README.md).

---

## What makes this different — and why we think it's better suited to this question

**Rule application, not judgment.** "Does the Bundling flag fire?" is answerable by reading the text against a written definition. "Is this order significant?" is not. Two coders applying the same eleven rules to the same order should converge — and now there's a full-corpus independent test of exactly that.

**Reproducible by construction.** Every score in this repository traces back to a specific coder, a specific piece of source text (preserved in [`database/corpus-texts/`](database/corpus-texts/)), and a specific written justification against a specific version of a frozen rule. Significance classification by expert panel can't be re-derived by someone outside the panel; this can.

**Pre-registered.** The scoring scheme was committed before any order was coded. Changes after coding began are dated amendments with stated reasons, not silent edits — see the version histories inside [`methodology/scoring-scheme.md`](methodology/scoring-scheme.md) and [`methodology/flags-canonical.md`](methodology/flags-canonical.md).

**Validated before extended.** The scoring scheme was applied to the full Mayer & Price census, then re-coded from scratch by an independent, label-blind coder, *before* any claim about discriminative validity was made or the methodology was applied beyond that sample. Validation earned the right to extend, not the other way around.

**Explicit about its own scope boundary.** The instrument measures architecture, not substantive fairness or policy wisdom. A precisely drafted, substantively troubling policy can score low — that's a feature of what's being measured, not a flaw. See "What This Scheme Does Not Do" in `scoring-scheme.md`.

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

Each flag is scored ABSENT (0), PRESENT (1), or CRITICAL (2) per order. NOT_APPLICABLE flags are excluded from both the numerator and denominator. The normalized structural-weight score is raw points divided by maximum possible points across applicable flags.

---

## Repository contents

Every folder below, including nested ones, has its own README explaining exactly what's in it. This section is a map, not the full explanation.

### [`methodology/`](methodology/) — the instrument itself, frozen before coding

`scoring-scheme.md` (v1.4) and `flags-canonical.md` (v1.2.2). Shared and unchanged across both the validation and the extension — nothing here is specific to Mayer & Price or to any one time period.

### [`mayer-price-validation/`](mayer-price-validation/) — the full validation story, start to finish

**Start here for the AUC claim and the comparison to Mayer & Price.** Who Mayer & Price are and why we validate against them, the 298-order sample and its provenance, the independent blind coding process (with the complete package given to the blind coder preserved in full), the AUC computation and its revision trajectory, and the comparison analysis. Everything needed to reproduce this specific result lives here.

### [`extension/`](extension/) — the full-corpus application (Step 4)

**Start here for the full-corpus claim.** The validated methodology applied to all of 1936–present: 7,149 of 7,151 orders scored, by two independent coding streams (FDR/Truman; Eisenhower–present), each with full per-order justification and a running log of cross-order patterns discovered along the way. The annual structural-weight trend and its chart data live here.

### [`database/`](database/) — the shared foundational data

The full text of every in-scope executive order (`corpus-texts/`, one file per order, primary source for every coding decision in this project), and `eo_coding.db`, the consolidated database of every coding record from every coder. **The database is a derived artifact, rebuilt from the JSON coding files — read `database/README.md` before editing it directly.**

### [`findings/`](findings/)

Named cross-order patterns and structural phenomena — separate from the validation claim itself, and expected to keep growing as more of the full-corpus extension's material gets synthesized.

---

## Order of operations

```
1. Freeze scoring scheme                                                     ✓ complete
         ↓
2. Code the full Mayer & Price (2002) validation sample (298 orders)         ✓ complete
         ↓
3. Re-code independently, blind to class label — run AUC validation          ✓ complete — AUC = 0.7836
         ↓
4. Extend coding to the full corpus (1936–present)                          ✓ complete — 7,149 / 7,151 orders
```

The scoring scheme (flag definitions and confidence taxonomy) remained frozen through the extension, to avoid fitting the instrument to the corpus it was validated on rather than the one it's meant to generalize to.

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
