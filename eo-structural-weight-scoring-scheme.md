# EO Structural Weight Score: Scoring Scheme
*Version 1.0 — June 2026*
*Pre-registration document. This scheme is frozen before any executive order is coded.*
*Flag definitions: church-bells-flags-canonical.md v1.2.1*
*Repository: [the-statecraft-blueprint/eo-structural-weight*](https://github.com/The-Statecraft-Blueprint/eo-structural-weight)

---

## Purpose

This document specifies the complete scoring scheme for the EO Structural Weight Score — a quantified, rule-based measure of how much governance-architecture machinery a given executive order deploys. It is a pre-registration artifact: the scheme is committed in writing before it is applied to any EO, before the EO corpus is coded, and before the structural-weight scores are compared against any external measure (Binder gridlock series, Mayer/Howell/Rothenberg significance codings).

The order of operations is a non-negotiable guardrail:

1. **Freeze the scoring scheme** (this document)
2. **Validate against established significance codings** (Howell, Rothenberg, or equivalent) on EOs those scholars already coded — confirm the structural-weight score reproduces their significance rankings within a defined margin before extending
3. **Extend to the full corpus** (1949–present, or the period available)
4. **Compare to Binder gridlock series** — only after steps 1–3 are complete

No EO is coded before this document is committed to the repository. No gridlock comparison is run before the validation in step 2 is complete. The scheme is not adjusted between steps 2 and 4.

---

## What This Measures

The EO Structural Weight Score measures the structural presence of governance-architecture machinery in an executive order — how many of the eleven standing structural flags fire, and at what severity. It is a descriptive measure, not a significance judgment.

**What it is:** A rule-applied structural audit. The score captures what the EO does to governance architecture — whether it concentrates power, creates accountability gaps, preempts oversight, establishes perverse incentives, and so on. Two coders reading the same EO text against the same flag definitions should reach substantially the same score.

**What it is not:** A measure of political importance, policy impact, public salience, or historical significance. An EO that concentrates power in an unaccountable official over a narrow regulatory domain scores higher than a politically prominent EO that does so cleanly and with full oversight mechanisms — even if the latter is more historically significant by conventional judgment. That divergence is not a flaw; it is the methodological contribution.

**The comparison claim:** The structural-weight score is more objective and more auditable than existing significance measures (Mayer 1999; Mayer & Price 2002; Howell 2003; Chiou & Rothenberg 2017), which rely on subjective importance judgments. It is more theoretically grounded for governance-architecture purposes — measuring the machinery deployed, not the political salience of the subject. Validation against existing measures tests convergent validity: the score should correlate with established significance rankings, while diverging in theoretically explicable ways.

---

## The Eleven Flags

The flag set is defined in full in `church-bells-flags-canonical.md` v1.2.1. That document is authoritative; this section summarizes for reference only.

| # | Flag | Track emphasis |
|---|------|----------------|
| 1 | Power Concentration | Both |
| 2 | Accountability Gaps | Both |
| 3 | Bundling (remedy / frame) | Both |
| 4 | Vague Enforcement | Both |
| 5 | Perverse Incentives (sub-flag: Zombie Emergency Trap) | Both / EO emphasis |
| 6 | Sunset Provisions (absence of) | Both |
| 7 | Preemption of Oversight | Both |
| 8 | Third-Party Incentive Gaps | Both |
| 9 | Second/Third-Order Effects | Both |
| 10 | Inter-Agency Cannibalization | Both / EO emphasis |
| 11 | Exemptions Architecture | Both / EO emphasis |

---

## Status Vocabulary

Every flag is assigned exactly one status per EO:

| Status | Definition |
|--------|------------|
| **ABSENT** | Flag does not fire. Clean design on this dimension. |
| **PRESENT** | Flag fires. The structural failure mode is identifiable from the text. |
| **CRITICAL** | Flag fires and represents a core design collapse that directly undermines the EO's stated purpose. CRITICAL implies PRESENT; not every PRESENT rises to CRITICAL. |
| **NOT APPLICABLE** | Flag does not apply to this EO's type, scope, or subject matter. Requires brief written justification. |

---

## Score Mapping

### Status-to-points

| Status | Points |
|--------|--------|
| NOT APPLICABLE | Excluded (see below) |
| ABSENT | 0 |
| PRESENT | 1 |
| CRITICAL | 2 |

**Rationale for 0/1/2:** The simplest scale that captures the PRESENT/CRITICAL distinction. Maximum theoretical raw score is 22 (eleven flags × 2 points). The scale is auditable, has no hidden parameters, and produces no incentive to assign CRITICAL over PRESENT for scoring reasons — the difference is one point.

### NOT APPLICABLE handling

Flags scored NOT APPLICABLE are excluded from both numerator and denominator. They do not contribute zero points to the score — they are absent from the calculation entirely. This ensures that narrow administrative orders (pay-rate adjustments, committee continuances, scheduling changes) are not artificially deflated relative to major policy orders by the presence of flags that genuinely do not apply.

**Documentation requirement:** Every NOT APPLICABLE scoring must include a one-sentence written justification in the coding record. "Not applicable — order is a narrow administrative action with no enforcement mechanism" is sufficient. Undocumented NOT APPLICABLE scores are treated as coding errors on audit.

### Sub-flag handling

The Zombie Emergency Trap (sub-flag under Flag 5, Perverse Incentives) does not score independently. It is a diagnostic label that can elevate a PRESENT to CRITICAL on the parent flag when its operational test is met. No additional points are awarded beyond what the parent flag's CRITICAL status already contributes. This prevents an asymmetry between Flag 5 and the other ten flags, which have no sub-flags.

---

## Aggregation Formula

For each executive order, the following quantities are computed:

**applicable\_count** = number of flags scored ABSENT, PRESENT, or CRITICAL
*(i.e., total flags minus NOT APPLICABLE flags; range 0–11)*

**raw\_score** = sum of points across all applicable flags
*(range 0 to 2 × applicable\_count)*

**max\_possible** = 2 × applicable\_count
*(the score an EO would receive if every applicable flag fired at CRITICAL)*

**normalized\_score** = raw\_score / max\_possible
*(range 0.00–1.00; undefined if applicable\_count = 0)*

**structural\_weight\_pct** = normalized\_score × 100
*(range 0–100; the primary reported measure)*

### Edge case: fully administrative EOs

If applicable\_count = 0 (every flag scored NOT APPLICABLE), the normalized score is undefined and the EO is coded as administrative-only. These EOs are retained in the dataset with a flag indicating their status but are excluded from the main analysis. A post-office renaming is the canonical example.

---

## Per-EO Coding Record

Each coded EO produces one structured record containing:

**Identification fields:**
- EO number
- Title
- Date signed
- President
- Congress number (derived from date — the Congress in session when the EO was signed)
- Source URL (American Presidency Project)

**Flag fields (one per flag, repeated × 11):**
- Flag number (1–11)
- Flag name
- Status (ABSENT / PRESENT / CRITICAL / NOT APPLICABLE)
- Points awarded (0, 1, or 2)
- Justification (1–3 sentences citing specific EO text that triggers or clears the flag)
- Sub-flag fired (yes/no — Zombie Emergency Trap only, under Flag 5)

**Score fields:**
- applicable\_count
- raw\_score
- max\_possible
- normalized\_score
- structural\_weight\_pct

**Qualitative fields:**
- Dominant flag (the highest-scoring flag; if tied, the lower-numbered flag)
- Critical\_count (number of flags scored CRITICAL)
- Present\_count (number of flags scored PRESENT)
- Absent\_count (number of flags scored ABSENT)
- NA\_count (number of flags scored NOT APPLICABLE)
- Coder ID
- Coding date
- Source text version (URL + date accessed, to handle APP updates)

---

## Weighting Decisions (Frozen)

**Flag weights: uniform.** All eleven flags contribute equally to the score. No flag is weighted more heavily than another in the aggregation formula. This is a deliberate and frozen design choice, not a default.

Differential weights are the highest-risk tuning surface in the scoring scheme. The correlation between structural-weight scores and the Binder gridlock series is the hypothesis being tested. Applying differential weights before that test is run creates the possibility — however unintentional — of weighting flags until the correlation improves. Pre-registration forecloses that path. If differential weighting is explored, it is a post-hoc sensitivity analysis with explicitly disclosed motivation, not an adjustment to the primary measure.

**PRESENT/CRITICAL split: 1/2.** The two-to-one ratio between CRITICAL and PRESENT is the simplest ratio that distinguishes them. Any other ratio (e.g., 1/3, 2/3) would require a principled justification that the distinction is more than binary — that severity varies continuously within CRITICAL. The flag definitions do not support that claim; CRITICAL is a threshold judgment, not a continuous one.

**Normalization: yes.** The normalized score is the primary measure because it is comparable across EOs with different applicability profiles. Raw scores are reported as a secondary measure for transparency.

---

## Validation Design

### Step 2: Reproduce established significance codings

Before extending into the modern period, the frozen scoring scheme is applied to EOs already coded by Howell (*Power Without Persuasion*, 2003) and/or Chiou & Rothenberg (*The Enigma of Presidential Power*, 2017). The structural-weight scores for those EOs are compared against the existing significance classifications.

**Validation measure:** Area Under the ROC Curve (AUC). Howell's and Rothenberg's significance codings are binary or near-binary (significant / not significant, or a small number of tiers). AUC measures how well the continuous structural-weight score separates the "significant" from "not significant" classifications across all possible thresholds — without requiring us to commit to a specific threshold before seeing the data.

**Success criterion (frozen):** AUC ≥ 0.70 against at least one of the established codings constitutes sufficient convergent validity to proceed to step 3. AUC between 0.60 and 0.70 constitutes partial convergent validity and requires a published explanation before extension. AUC < 0.60 requires the flag definitions or scoring scheme to be reviewed before extension — with any changes documented as a revision to this pre-registration, with a new version number and a gap in the coding timeline.

**Rationale for 0.70:** An AUC of 0.70 is a conventional threshold for "acceptable discrimination" in diagnostic testing. It is not a high bar — it means the structural-weight score does notably better than random chance at recovering existing significance judgments. The claim is not that the structural-weight score perfectly reproduces Mayer/Howell/Rothenberg; it is that it correlates with them sufficiently to establish that they are measuring related (though distinct) phenomena. AUC < 0.70 would suggest the measures are largely orthogonal, which would require explanation before the structural-weight score can be used as an extension of or improvement upon the established literature.

**Divergence analysis:** EOs where the structural-weight score and the established coding most strongly disagree are identified and examined qualitatively. These divergences are the methodological contribution: cases where a structural-feature measure produces a different classification than an importance-judgment measure, for explicable reasons, are evidence that the two measures are genuinely distinct and that the structural-weight score adds information beyond what the established codings capture.

### Step 2 Amendment (v1.1, 2026-07-03): Mayer & Price (2002) substituted as primary validation source

**Trigger.** Kenneth Mayer confirmed by email that the original dataset underlying Mayer (1999) and Mayer & Price (2002) is lost. Outreach to Howell and Rothenberg for their independent codings is in progress but has not yet produced data. Rather than block Step 2 on external response times, the published appendix of Mayer & Price (2002) — 149 EOs classified as significant, drawn from a pooled random sample of 1,028 orders sampled from all orders issued March 1936–December 1999 — is substituted as the Step 2 validation source. If and when Howell or Rothenberg data arrives, it is treated as an additional, independent cross-validation rather than a prerequisite for this step.

**The data gap.** Mayer & Price publish only the 149 orders their coding classified as significant. The remaining ~879 sampled orders classified as not-significant are not published, and the underlying dataset is lost — sample membership for the negative class is unrecoverable. AUC requires both classes, so the negative class for this validation run is constructed rather than reproduced from their actual sample.

**Positive class.** All 149 EOs in the published appendix — a census of the published positives, not a subsample. (Transcription and corpus-join details, including nine date-transcription errors in the original PSQ appendix identified and resolved against corpus signing dates, are documented separately in `mayer-price-2002-appendix-provenance.md`.)

**Negative class.** A random sample, N=149 (matching the positive class 1:1), drawn from EOs issued between 1936-03-01 and 1999-12-31 (Mayer & Price's stated sampling window — note this is date-bounded, not EO-number-bounded; their footnote-3 population count of 7,471 orders, EO 5674–13144, describes the Federal Register's retrospective numbering series and includes some orders actually signed before 1936, retroactively indexed when the Register began publication in 1936), excluding the 149 appendix EOs. Simple random sample, no stratification. Frozen random seed: `20260703`. Draw is reproducible from `eo_coding.db` and recorded in `negative-sample-v1.csv`.

**Contamination and its direction.** Because the negative class is drawn from the general population rather than reproducing Mayer & Price's actual sampled-and-rejected pool, it will contain some EOs that Mayer & Price would have classified significant had they sampled them — implied base rate 149/1,028 ≈ 14.5%. Any such order sitting in the negative class is mislabeled relative to what Mayer & Price would have found. This can only ever suppress the measured AUC, never inflate it: a structurally heavy EO wrongly placed in the "insignificant" bin is a labeling error the score gets no credit for resolving correctly. Clearing the pre-registered AUC ≥ 0.70 threshold under this contamination is therefore a *harder*, more conservative test than the originally envisioned design against a clean external negative class — not an easier one. This is a one-directional bound, not a full correction; it is disclosed as a limitation, not treated as eliminated.

**Exclusion of calibration-set EOs from the negative draw.** Six of the ten already-coded calibration EOs fall within the 1936–1999 window (9066, 9981, 10924, 11069, 12291, 12717). Two of these (9981, 10924) are themselves appendix EOs and their existing codings carry forward directly as already-completed positives — no re-coding needed, since the positive class is a census and coding-order doesn't matter. The other four (9066, 11069, 12291, 12717) were purposively selected to test specific expected-score tiers during calibration, not randomly drawn, and are excluded from consideration as negatives even though they are already coded and technically available: including purposively-selected cases in a nominally random negative sample would bias the AUC test. Confirmed no overlap between these four and the drawn negative-sample-v1.

**Scope and pacing.** Full census of 149 positives (147 remaining to code; 2 already complete) plus 149 negatives (149 remaining) — 296 total codings, executed incrementally across sessions via the existing `create_coding_template.py` / `import_coding.py` pipeline, given per-conversation constraints. Progress is tracked in `eo_scores`; AUC is not computed until the full batch is coded, per the pre-registration's ban on peeking at the comparison before extension.

### Step 4: Compare to Binder gridlock series

After extension to the full corpus, EO structural-weight scores are aggregated to the Congress level (mean normalized score per Congress, or total raw score per Congress — both reported). The resulting series is compared to the Binder grid4 score (the canonical gridlock measure at the NYT ≥4 salience threshold) for the matching Congresses.

**The hypothesis:** EO structural weight rises as legislative gridlock rises. The engine model predicts that when the legislative cylinder misfires (gridlock rises), unilateral executive action rises to fill the vacuum — and that this signal is in the structural weight of the orders, not the raw count.

**Comparison measure:** Spearman rank correlation between mean-structural-weight-per-Congress and grid4, for all Congresses where both measures are available. Spearman is appropriate because both measures are bounded and the relationship may not be linear.

**The raw-count control:** Raw EO counts per Congress (from the APP dataset) are entered as a comparison. The hypothesis predicts that structural weight correlates with gridlock more strongly than raw counts do. If raw counts outperform structural weight, the methodological contribution is weakened.

---

## Inter-Coder Reliability Protocol

A random sample of EOs is independently coded by a second coder (Gemini or ChatGPT, using the same flag definitions and scoring scheme, without access to the primary coder's scores). Divergences are recorded and resolved by reference to the flag definitions — not by averaging.

**Target sample size:** 10% of the validation set (EOs also coded by Howell/Rothenberg), minimum 20 EOs.

**Acceptable divergence:** Coders are expected to agree on flag status within one level (e.g., PRESENT vs. CRITICAL disagreements are acceptable; ABSENT vs. CRITICAL disagreements require reconciliation). Overall inter-coder agreement on the binary significant/not-significant classification (using a structural-weight threshold of 0.35 as the interim cutoff, subject to revision after validation) should exceed 80%.

The interim threshold of 0.35 is used only for the inter-coder reliability binary classification. The threshold used in the final AUC analysis is not fixed — AUC evaluates discrimination across all thresholds.

---

## What This Scheme Does Not Do

**Does not predict litigation outcomes.** A high structural-weight score does not mean an EO will be struck down in court. Legal vulnerability is a separate analysis (the Church Bells Legal Impact Assessment). Structural weight is an architecture measure.

**Does not assess political significance.** An EO transferring enormous regulatory authority cleanly — with clear accountability, meaningful oversight, defined enforcement, and a sunset provision — could score very low structural weight while being politically significant. That outcome is correct, not a flaw.

**Does not impute motive.** A CRITICAL flag finding means the structural failure mode is present in the text. It says nothing about whether the failure was deliberate or inadvertent.

**Does not capture non-EO executive actions.** Presidential memoranda, proclamations, national security directives, and similar instruments are outside this dataset. The score applies to numbered executive orders only.

---

## Known Limitations (Coding Process)

**Scope of scrutiny to date.** The ICR pilot (Claude, Gemini, ChatGPT; see Inter-Coder Reliability Protocol) has closely examined roughly 38 of the corpus's 10,537 EOs — the calibration set plus the 30-EO ICR sample. Every fix in this document's version history (v1.1, v1.2, v1.2.1) was discovered through that narrow window, not through a systematic audit of the full corpus. It is not known how many similar coding-process issues exist in the ~10,500 EOs that have not received this level of scrutiny.

**A specific mechanism, found by example.** Coding EO 8451 (a 90-word individual Civil Service Rules waiver), two flags were incorrectly scored NOT_APPLICABLE — not because the operational test was ambiguous, but because the order's surface simplicity led to a pattern-matched "this is obviously trivial" judgment instead of an independent check of each flag's own test against the text. Both flags (Perverse Incentives, Preemption of Oversight) were in fact answerable and PRESENT once actually checked — the order's "without compliance with the requirements of the Civil Service Rules" language is a direct textual trigger for both. Caught only because Jason independently researched the order and pushed back on the coding.

**This mechanism is not a rare edge case.** A corpus-wide scan (2026-07-04) found:
- 42.0% of all 10,537 EOs are under 200 words — squarely in the length range where the triviality-pattern-match shortcut operates.
- 11.5% of all EOs contain at least one of the bypass-language patterns ("notwithstanding," "without regard to," "without compliance with," "without complying with") that specifically warrant deliberate Flag 5/Flag 7 scrutiny before defaulting to NOT_APPLICABLE.

**A confound worth naming directly: EO length correlates strongly with era.** Median EO word count rises roughly 12-fold across the corpus's history — from 87 words in the 1900s to 1,099 words in the 2020s — and the share of short (under-200-word) orders falls from ~80% in the earliest decades to under 1% by the 2010s–2020s. If the pattern-matching-to-triviality shortcut causes systematic under-scoring on short orders, that error is not randomly distributed across the corpus — it concentrates almost entirely in early decades. Because this project's central hypothesis (the "exhaust gauge" prediction) is itself a claim about structural weight *rising over time* as gridlock rises, a bias that depresses old-EO scores relative to modern ones would inflate the appearance of that trend for reasons unrelated to actual governance-architecture change. This is a plausible mechanism connecting a demonstrated error type to a known corpus-composition fact — not a demonstrated bias in the results, since only one instance has been confirmed. It is disclosed here because it bears directly on the interpretability of whatever trend the full-corpus analysis eventually shows: a strong, clear trend is not obviously an artifact of this mechanism, but a marginal or borderline one should be treated with this specific risk in mind, not just generic measurement-error caution.

**Scoping decision.** This project's purpose is to support the analysis in Jason's book, not to produce an exhaustively validated, publication-grade academic instrument immune to this class of criticism. Full-corpus re-auditing for this and similar issues is not planned. This section exists so the limitation is disclosed rather than discovered later — by a reviewer, a reader, or a future pass — without having been named as a known, accepted trade-off.

---

## Version History

- v1.0 — June 2026 — Initial pre-registration document. Eleven flags, uniform weights, 0/1/2 status mapping, AUC ≥ 0.70 validation threshold. Committed before any EO is coded.
- v1.1 — 2026-07-03 — Step 2 amendment: Mayer & Price (2002) published appendix substituted as primary Step 2 validation source pending Howell/Rothenberg response (treated as future cross-validation, not a prerequisite). Documents the data gap (negative class unpublished, dataset lost), the constructed negative-sample design (N=149, random, seed 20260703, date-bounded 1936-03-01–1999-12-31), the one-directional contamination bound, and the exclusion of purposively-selected calibration EOs from the negative draw. Committed before any validation-batch EO is coded.
- v1.2 — 2026-07-04 — Added "Known Limitations (Coding Process)" section documenting the pattern-matching-to-triviality error mechanism found in EO 8451's reconciliation, the corpus-wide scan bounding its potential scope (42% of corpus under 200 words, 11.5% containing bypass-language patterns), and the EO-length-vs-era confound directly relevant to the project's core time-trend hypothesis. Explicit scoping decision recorded: accepted as a disclosed trade-off given the project's purpose, not pursued via full-corpus re-audit.
