# EO Structural Weight Score: Scoring Instructions for Blind Coding

*This is a redacted extract of the project's scoring-scheme document (v1.4), prepared specifically for an independent, label-blind coding pass. It contains only the operational rules needed to score an executive order. It deliberately omits sections of the source document that describe the validation study's design, sampling, or any worked examples tied to specific executive orders' known scores — because several of the orders in your batch are examples used elsewhere in this project's materials, and seeing their answers in advance would defeat the purpose of this exercise.*

*You will also receive a companion document, `flags-canonical.md`, which defines each of the eleven flags in full. That document is authoritative for what each flag means and how to apply it. This document covers everything else: status vocabulary, scoring math, and the record format for what you report back.*

---

## What This Measures

The EO Structural Weight Score measures the structural presence of governance-architecture machinery in an executive order — how many of eleven standing structural flags fire, and at what severity. It is a descriptive measure, not a significance judgment.

**What it is:** A rule-applied structural audit. The score captures what the order does to governance architecture — whether it concentrates power, creates accountability gaps, preempts oversight, establishes perverse incentives, and so on. Two coders reading the same text against the same flag definitions should reach substantially the same score.

**What it is not:** A measure of political importance, policy impact, public salience, or historical significance. An order that concentrates power in an unaccountable official over a narrow regulatory domain scores higher than a politically prominent order that does the same thing cleanly, with full oversight and a defined sunset — even if the latter is more historically significant by conventional judgment. That divergence is the point of the instrument, not a flaw in it.

**Does not assess substantive fairness or policy wisdom.** The score measures governance architecture — how power is concentrated, checked, and made accountable — not whether the policy that architecture serves is just, wise, or fair. A precisely drafted, stably administered policy that is nonetheless substantively troubling on other grounds can score low if its architecture is clean by the flags' own tests: clear criteria, defined authority, no vague enforcement, a working oversight mechanism. That is not a gap in the instrument. Distinguishing "well-built machine" from "machine built for a good purpose" is what it is for. A low score should never be read, on its own, as a verdict that the underlying policy was fair or good — only that its architecture met the tests below.

**Does not predict litigation outcomes, assess political significance, or impute motive.** A CRITICAL flag finding means the structural failure mode is present in the text; it says nothing about whether the drafter intended it.

---

## The Eleven Flags

Full definitions, operational tests, and "key distinction" guidance for each flag are in the companion document `flags-canonical.md`. Read that document in full before coding. This table is a reference summary only.

| # | Flag |
|---|------|
| 1 | Power Concentration |
| 2 | Accountability Gaps |
| 3 | Bundling (remedy / frame) |
| 4 | Vague Enforcement |
| 5 | Perverse Incentives (sub-flag: Zombie Emergency Trap) |
| 6 | Sunset Provisions (absence of) |
| 7 | Preemption of Oversight |
| 8 | Third-Party Incentive Gaps |
| 9 | Second/Third-Order Effects |
| 10 | Inter-Agency Cannibalization |
| 11 | Exemptions Architecture |

---

## Status Vocabulary

Every flag is assigned exactly one status per order:

| Status | Definition |
|--------|------------|
| **ABSENT** | Flag does not fire. Clean design on this dimension. |
| **PRESENT** | Flag fires. The structural failure mode is identifiable from the text. |
| **CRITICAL** | Flag fires and represents a core design collapse that directly undermines the order's stated purpose. CRITICAL implies PRESENT; not every PRESENT rises to CRITICAL. |
| **NOT APPLICABLE** | Flag does not apply to this order's type, scope, or subject matter. Requires a brief written justification. |

---

## Score Mapping

### Status-to-points

| Status | Points |
|--------|--------|
| NOT APPLICABLE | Excluded (see below) |
| ABSENT | 0 |
| PRESENT | 1 |
| CRITICAL | 2 |

Maximum theoretical raw score per flag is 2. The scale is intentionally simple: it has no hidden parameters and creates no incentive to inflate CRITICAL over PRESENT — the difference is one point.

### NOT APPLICABLE handling

Flags scored NOT APPLICABLE are excluded from both numerator and denominator. They do not contribute zero points — they are absent from the calculation entirely. This keeps narrow administrative orders (pay-rate adjustments, committee continuances, scheduling changes) from being artificially deflated relative to major policy orders by flags that genuinely do not apply to them.

**Documentation requirement:** every NOT APPLICABLE scoring must include a one-sentence written justification. "Not applicable — order is a narrow administrative action with no enforcement mechanism" is sufficient. Undocumented NOT APPLICABLE scores are treated as coding errors on audit.

**On the NOT APPLICABLE / ABSENT boundary — read this carefully.** `flags-canonical.md` contains a precise, mechanical rule for this in its "Application Notes" section (the paragraphs following "A concrete test for the eight flags without the narrow-order exception"). That rule, not this document, is authoritative. In short: Flags 1, 2, and 7 are always answerable — a self-executing, one-sentence order still has a clean answer to "where does decision authority rest" and "is any existing oversight removed," and that answer is ABSENT, not NOT APPLICABLE. Flags 4, 5, 8, and 11 presuppose an ongoing behavioral or compliance relationship; where no such relationship exists at all (a one-time land transfer, a fixed-sum authorization), they are genuinely NOT APPLICABLE — this is not a shortcut for brevity, it's a real difference in what the flag is asking. Flags 6 and 10 have their own narrower conditions, also specified there. Apply that test directly rather than a general instinct either toward or away from NOT APPLICABLE — the goal is matching each flag's actual question to what the order's text does, not defaulting in either direction.

### Sub-flag handling

The Zombie Emergency Trap (sub-flag under Flag 5, Perverse Incentives) does not score independently. It is a diagnostic label that can elevate a PRESENT to CRITICAL on the parent flag when its operational test — defined in `flags-canonical.md` — is met. No additional points are awarded beyond what the parent flag's CRITICAL status already contributes.

---

## Aggregation Formula

For each executive order, compute:

**applicable_count** = number of flags scored ABSENT, PRESENT, or CRITICAL (i.e., 11 minus the count scored NOT APPLICABLE; range 0–11)

**raw_score** = sum of points across all applicable flags (range 0 to 2 × applicable_count)

**max_possible** = 2 × applicable_count

**normalized_score** = raw_score / max_possible (range 0.00–1.00; undefined if applicable_count = 0)

**structural_weight_pct** = normalized_score × 100 (range 0–100; the primary reported measure)

### Edge case: fully administrative orders

If applicable_count = 0 (every flag scored NOT APPLICABLE), the normalized score is undefined. Report the order as administrative-only rather than assigning a score. A pure post-office-renaming order is the canonical example, though none should be quite that trivial in this batch.

---

## Weighting Decisions (Frozen — do not deviate)

**Flag weights: uniform.** All eleven flags contribute equally. No flag is weighted more heavily than another.

**PRESENT/CRITICAL split: 1/2.** CRITICAL is a threshold judgment (a core design collapse), not a matter of degree within PRESENT. Do not invent intermediate values.

**Normalization: yes.** Report the normalized score (structural_weight_pct) as the primary result; raw_score, applicable_count, and max_possible are also reported for transparency and auditability.

---

## Coding Conventions

### Diff-aware amendment coding

When an order amends, supersedes, or is explicitly amended by a named predecessor order, first identify the specific mechanism the amendment touches (a reporting requirement, a review process, an eligibility criterion, a termination trigger, etc.). The question is not only "what does this order say" but "relative to what existed immediately before, did this specific mechanism get preserved, strengthened, or weakened."

**Check `referenced-predecessors/EO-{number}.md` for the named predecessor's text before scoring.** This is the primary place to look — it was built specifically to make this comparison possible, and most predecessors cited anywhere in this batch are there. Only if the number isn't in that folder either should you fall back to scoring based on the amending order's own text alone, and in that case, note explicitly in your justification field that the comparison could not be made and why — don't silently treat the order as if no predecessor existed, and don't guess at what the predecessor likely said.

### Incorporation-by-reference: two distinct rules

**Full incorporation.** When an order extends, adopts, or applies "all provisions" (or substantively equivalent language) of a named prior order to a new subject — a new country, a new agency, a new department — the extending order inherits the parent order's flag findings for the extended subject, even though its own text may be very short. Do not score a one-paragraph extension order as structurally clean merely because it is brief; assess what it actually extends.

**Partial amendment.** When an order amends one specific provision of a prior order — a reporting clause, a membership rule, a single definition — without incorporating the whole framework, assess only that specific provision against its own baseline, per the diff-aware convention above. Full inheritance does not apply.

**The distinguishing test:** does the order's text incorporate the predecessor wholesale for a new application, or does it modify one identified piece of an existing framework that otherwise continues to operate under its own terms? The former inherits; the latter is assessed independently.

---

## What You Should Report

For each order, produce one structured record containing:

**Identification:** EO number (as it appears in the order's own title), title, date signed, president.

**Flag fields, one per flag (× 11):** flag number, flag name, status (ABSENT / PRESENT / CRITICAL / NOT APPLICABLE), points awarded (0/1/2), a 1–3 sentence justification citing the specific text that triggers or clears the flag, and whether the Zombie Emergency Trap sub-flag fired (yes/no — Flag 5 only).

**Score fields:** applicable_count, raw_score, max_possible, normalized_score, structural_weight_pct.

**A brief note** (1–2 sentences) on anything unusual about the order that affected your scoring — e.g., "this order is a full incorporation of EO X, whose text was not available to me" or "this order's brevity made me want to default several flags to NOT APPLICABLE, but I checked each one against the text directly per the coding conventions above."

---

## What Not To Do

- **Do not search the web, consult academic literature, or look up whether this order appears in any published index of "significant" executive orders.** Score based solely on the order's own text and the rules in this document and in `flags-canonical.md`. This instruction is not incidental — it is the reason this coding pass exists as a separate, independent check.
- Do not attempt to guess or infer whether an order is part of any particular study sample. You have not been told anything about how these orders were selected, and that is intentional.
- Do not compare orders to each other while coding, or adjust earlier scores because a later order seems "more" or "less" severe by comparison. Score each order against the flag definitions, not against the other orders in the batch.
- Do not skip an order or leave it partially coded. If an order genuinely seems unscoreable (missing text, garbled formatting), say so explicitly rather than guessing.
