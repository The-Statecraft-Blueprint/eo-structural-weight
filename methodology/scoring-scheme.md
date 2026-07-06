# EO Structural Weight Score: Scoring Scheme
*Version 1.4 — 2026-07-05*
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

## Coding Conventions (Process Additions, v1.4)

These are procedural instructions for applying the frozen flag definitions consistently — not changes to what any flag means, and not a reopening of the flag set or the confidence taxonomy. They were identified while coding the Mayer & Price validation corpus and are documented here so any future coding pass, including a recode, applies them from the start rather than discovering them ad hoc partway through.

### Diff-aware amendment coding

When an EO amends, supersedes, or is explicitly amended by a named predecessor or successor order, the coder must first identify the specific mechanism the amendment touches (a reporting requirement, a review process, an eligibility criterion, a termination trigger, and so on) before scoring the amending order's own text. The question is not only "what does this order say" but "relative to what existed immediately before, did this specific mechanism get preserved, strengthened, or weakened."

This matters because an amendment can look clean read in isolation while actually removing a safeguard its predecessor had, or look unremarkable while actually adding one the predecessor lacked. Both patterns were found in the validation corpus and were only caught by explicitly making this comparison; scoring the amending text alone would have missed them.

**Procedure:** For any order presented as an amendment, the coder should locate and read the specific provision(s) being amended in the predecessor order before finalizing flag scores, and should state explicitly in the justification field whether the amendment preserves, strengthens, or weakens the relevant mechanism relative to that baseline.

### Incorporation-by-reference: two distinct rules

An order can relate to a prior order in two structurally different ways, and they are scored differently.

**Full incorporation.** When an order extends, adopts, or applies "all provisions" (or substantively equivalent language) of a named prior order to a new subject — a new country, a new agency, a new department — the extending order inherits the parent order's flag findings. A one-paragraph order stating that "the provisions of EO X shall apply to Y" carries the same structural weight as EO X itself with respect to the extended subject, even though its own text is short. Scoring such an order as clean merely because it is brief understates its actual architecture.

**Partial amendment.** When an order amends one specific provision of a prior order — a reporting clause, a membership rule, a single definition — without incorporating the whole framework, only that specific provision is assessed, evaluated against its own prior-text baseline per the diff-aware convention above. Full inheritance does not apply; the amendment is scored on its own narrower terms.

**The distinguishing test:** does the order's text incorporate the predecessor wholesale for a new application, or does it modify one identified piece of an existing framework that otherwise continues to operate under its own terms? The former inherits; the latter is assessed independently.

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

**Completion note (2026-07-05).** The full census described above is now complete: all 149 positive-class and all 149 negative-class EOs are coded in `eo_coding.db` under coder ID `claude-church-bells-v1`. See the following amendment before treating this as the Step 2 AUC dataset.

### Step 2 Amendment (v1.4, 2026-07-05): Independence requirement for AUC test coding

**Trigger.** The primary coding pass across the full 298-EO validation set was conducted with the coder aware of each EO's class label throughout, and in block order — the entire positive class was coded to completion before the negative class was begun. This is a validity problem for the AUC test specifically: a coder who knows the answer while grading cannot produce an independent measurement of whether the score discriminates the two classes, no matter how careful the underlying flag-level reasoning was. The problem is visible directly in the coding record itself, where high scores on negative-class EOs and low scores on positive-class EOs were repeatedly flagged and explained as they were encountered — the kind of thing a coder without the label in view would not have had reason to single out in the same way.

**Consequence.** The existing primary-coded dataset does not satisfy the independence requirement for the Step 2 AUC test as designed. It is retained and repurposed as (a) the source of the qualitative divergence analysis and the named recurring patterns documented in the project's notable-findings log, and (b) pilot material for calibrating instructions given to independent coders. It is not treated as the Step 2 validation data, and no AUC computed from it is reported as confirmatory evidence of the scheme's discriminative validity.

**Requirement for the AUC test itself.** The Step 2 AUC computation is valid only when produced from a coding pass meeting all of the following:

1. **Label-blind.** The coder performing the pass has no access to any EO's Mayer & Price class (positive or negative) before or during coding.
2. **Order-randomized.** EOs are presented in an order carrying no information about class membership — not chronological, not grouped by class, not otherwise correlated with the label. A fixed, disclosed random seed governs the presentation order, the same discipline already applied to the negative-sample draw itself.
3. **Isolated from prior coding artifacts.** The blind coder has no access to the primary coder's flag-level codings, notes, or the notable-findings log. These could leak class information indirectly, since "noteworthy enough to write up" and "historically significant" are correlated more often than chance.
4. **Documented coder identity and independence.** Whether the blind pass uses a different model, a different vendor's model entirely, or a separated instance of the same model with no access to this project's conversational history, the choice and its rationale are recorded, since the strength of the independence claim differs across these options.

**On coder choice.** A blind pass using the same model family that helped originate the scoring scheme carries some residual risk that model-family-specific reading tendencies shape both the scheme's design and its application, even with labels stripped. A cross-vendor blind pass does not carry this risk and is the stronger form of independence. Where feasible, this project uses at least one cross-vendor blind coder for the Step 2 AUC test. A same-family blind pass, if used in addition, is reported as a weaker but still meaningful form of independence — it controls for label-awareness and order effects even where it does not fully control for model-family effects.

**Multiple independent coders.** Where more than one blind coder completes the full corpus, each coder's AUC is reported individually, and the inter-coder agreement between them across the full 298-EO set is reported as a substantially stronger reliability estimate than the original 30-EO ICR pilot (see Inter-Coder Reliability Protocol) could support on its own.

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

**Does not assess substantive fairness or policy wisdom.** The score measures governance architecture — how power is concentrated, checked, and made accountable — not whether the policy that architecture serves is just, wise, or fair. A precisely drafted, stably administered, substantively discriminatory or otherwise troubling policy can score low if its architecture is clean by the flags' own tests: clear criteria, defined authority, no vague enforcement, a working oversight mechanism. This is not a gap to be fixed. Distinguishing "well-built machine" from "machine built for a good purpose" is what the instrument is for. But it means a low score should never be read, on its own, as a verdict that the underlying policy was fair or good — only that its architecture met the tests this instrument applies. This surfaced concretely, not just hypothetically, while coding EO 9467 (a Panama Canal Zone wage-tier system with a documented history of employment discrimination) and EO 10143 (a patronage-flavored civil-service exemption): both scored low because their architectural form was narrow and precise, and both are flagged in their own coding records as instances where this boundary was doing real work rather than providing purely theoretical cover.

---

## Known Limitations (Coding Process)

**Scope of scrutiny to date.** The ICR pilot (Claude, Gemini, ChatGPT; see Inter-Coder Reliability Protocol) has closely examined roughly 38 of the corpus's 10,537 EOs — the calibration set plus the 30-EO ICR sample. Every fix in this document's version history (v1.1, v1.2, v1.2.1) was discovered through that narrow window, not through a systematic audit of the full corpus. It is not known how many similar coding-process issues exist in the ~10,500 EOs that have not received this level of scrutiny.

**A specific mechanism, found by example.** Coding EO 8451 (a 90-word individual Civil Service Rules waiver), two flags were incorrectly scored NOT_APPLICABLE — not because the operational test was ambiguous, but because the order's surface simplicity led to a pattern-matched "this is obviously trivial" judgment instead of an independent check of each flag's own test against the text. Both flags (Perverse Incentives, Preemption of Oversight) were in fact answerable and PRESENT once actually checked — the order's "without compliance with the requirements of the Civil Service Rules" language is a direct textual trigger for both. Caught only because Jason independently researched the order and pushed back on the coding.

**This mechanism is not a rare edge case.** A corpus-wide scan (2026-07-04) found:
- 42.0% of all 10,537 EOs are under 200 words — squarely in the length range where the triviality-pattern-match shortcut operates.
- 11.5% of all EOs contain at least one of the bypass-language patterns ("notwithstanding," "without regard to," "without compliance with," "without complying with") that specifically warrant deliberate Flag 5/Flag 7 scrutiny before defaulting to NOT_APPLICABLE.

**Scoping decision.** This coding process is not being exhaustively re-audited for this or similar issues across the full corpus; the ICR pilot and ad hoc catches like this one are the level of scrutiny in place. This section exists so that limitation is disclosed as a known, accepted property of the coding process, rather than something a later pass discovers without it having been named. What any of this implies for the interpretation of downstream analyses of the resulting scores is out of scope for this document — that's a separate question for whatever context does that analysis, not for the instrument-building process recorded here. Reasoning about hypothesis-level implications while producing the individual codings that feed such an analysis risks biasing those codings toward a preferred outcome, the same risk this project already guards against by keeping external ICR coders blind to the validation design (see Inter-Coder Reliability Protocol).

---

## Version History

- v1.0 — June 2026 — Initial pre-registration document. Eleven flags, uniform weights, 0/1/2 status mapping, AUC ≥ 0.70 validation threshold. Committed before any EO is coded.
- v1.1 — 2026-07-03 — Step 2 amendment: Mayer & Price (2002) published appendix substituted as primary Step 2 validation source pending Howell/Rothenberg response (treated as future cross-validation, not a prerequisite). Documents the data gap (negative class unpublished, dataset lost), the constructed negative-sample design (N=149, random, seed 20260703, date-bounded 1936-03-01–1999-12-31), the one-directional contamination bound, and the exclusion of purposively-selected calibration EOs from the negative draw. Committed before any validation-batch EO is coded.
- v1.2 — 2026-07-04 — Added "Known Limitations (Coding Process)" section documenting the pattern-matching-to-triviality error mechanism found in EO 8451's reconciliation and the corpus-wide scan bounding its potential scope (42% of corpus under 200 words, 11.5% containing bypass-language patterns).
- v1.3 — 2026-07-04 — Removed Binder/gridlock-comparison content added earlier the same day to the Known Limitations section and to Step 4. That analysis belongs to the TSB-side thesis-testing work, not this instrument-building document, and reasoning about hypothesis-level implications (does a coding-process risk help or hurt the appearance of the book's core trend) while producing the codings that feed such an analysis risks biasing those codings — the same blinding principle this document already applies to external ICR coders, misapplied here by not extending it to the primary coding process itself. Step 4 reverted to its pre-2026-07-04 text. Known Limitations retained only the coding-process disclosure (the mechanism, the 8451 example, the corpus-wide scan), with no reference to gridlock, Binder, or the book's hypothesis.
- v1.4 — 2026-07-05 — Three additions. Flag definitions and the confidence taxonomy are unchanged and remain frozen; none of the following alters what any flag measures. (1) Added "Coding Conventions" section: diff-aware amendment coding (compare an amending order's specific mechanism against its immediate predecessor before scoring, rather than scoring the amending text in isolation) and a two-part incorporation-by-reference rule (full incorporation of "all provisions" of a prior order inherits that order's flag findings; a partial amendment to one specific provision is assessed on its own terms against its own baseline). Both derived from patterns identified while coding the Mayer & Price corpus. (2) Added Step 2 Amendment (v1.4) documenting that the completed 298-EO primary coding pass was conducted with the coder aware of class labels throughout and in block order (positive class completed before negative class began), disqualifying it as Step 2 AUC test data notwithstanding its completion; the dataset is retained for qualitative findings and pilot calibration only. Specifies a formal independence requirement — label-blind, order-randomized, isolated from prior coding artifacts, documented coder choice, cross-vendor coder preferred — for any coding pass whose AUC is reported as confirmatory evidence. (3) Added a fifth item to "What This Scheme Does Not Do": the instrument does not assess substantive fairness or policy wisdom, only governance architecture. A low score on a substantively troubling policy is not a verdict that the policy was fair, only that its architecture was precise by the flags' own tests. Motivated by EO 9467 and EO 10143 in the primary coding pass, where this distinction did real interpretive work rather than remaining a theoretical caveat.
