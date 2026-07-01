# Church Bells: Brief Methodology
*Bootstrapping document — March 2026. Updated April 2026.*

---

## The Pipeline

Church Bells operates a four-phase governance analysis pipeline:

**Detect → Analyze → Distribute → Mobilize**

Phase 1 covers Detect, Analyze, and Distribute. Mobilization is a later phase and a separate design problem.

**Sources monitored:**
- Federal Register (executive orders, presidential directives)
- Congressional activity (introduced legislation, markup, floor votes)

Both tracks are intentional. Monitoring executive *and* legislative action is what makes Church Bells nonpartisan by design, not by rhetoric. The methodology is the constant — not the political target. Bad structural design is flagged regardless of which branch produces it or which party sponsors it.

---

## The Two Tracks

**Executive Track** — Reactive, time-sensitive. An order is signed; analysis is published before the news cycle moves on. Value: speed and clarity.

**Legislative Track** — Proactive, slower, more durable. A bill is introduced; analysis is published while there is still time to amend it. Value: giving legislators, advocates, and citizens something to cite *during* the process, not after.

The legislative track also builds longitudinal authority: if TSB flagged structural problems in a bill, that bill passed, and those problems materialized — that is a track record. That is how credibility is earned without institutional credentials.

**Hybrid cases** — Some legislation is designed specifically to constrain or respond to executive action; some executive orders implement existing statutory authority in contested ways. These don't sit cleanly in either track. When a hybrid case arises, apply both analytical postures where relevant: treat the executive action as reactive and time-sensitive for publication purposes, and treat the statutory interaction as a legislative track question requiring longitudinal analysis. The methodology is the same — the framing and urgency differ.

---

## The Brief Format

Every Church Bells brief follows this structure. Length varies by subject; structure does not.

---

### Header Block
- Identifier (EO number, bill number, etc.)
- Full title
- Date signed or introduced
- Sponsoring authority

**Plain-language summary:** One paragraph. What does this do, in plain language. No editorializing. This is the "what happened" layer.

**Verdict line:** Two sentences, immediately following the summary. Sentence one states the core finding in its most compressed form. Sentence two states the primary structural reason the finding holds. The entire brief earns these two sentences. They should be quotable, briefable, and shareable on their own. Example: *"This order has significant constitutional vulnerabilities and predictable structural failures. Power over eligibility determinations is concentrated in unelected agency heads with no meaningful appeal mechanism and no sunset review."*

---

### Legal Impact Assessment

This is not litigation prediction. It is a **legal vulnerability audit** — analogous to a security audit of source code. We are not predicting whether someone will exploit a vulnerability. We are identifying that the vulnerability exists and what it exposes.

**Questions this section answers:**
- What existing rights, protections, or legal constraints does this touch?
- Does this concentrate or distribute power — and in whom?
- What does this make easier or harder to challenge in the future?
- What legal precedent does this set if it stands, and what does that precedent enable next?
- Where does this weaken democratic accountability specifically?
- What are the legal implications to people — not courts?

**Confidence ratings are required on all legal findings, using the two-axis taxonomy below.** This is both intellectually honest and central to the nonpartisan case. Where a finding splits across multiple legal theories, each theory gets its own rating.

Note: LegesGPT or equivalent legal AI tools should be used to ground citations and precedent. Assertions require support.

---

### Structural Analysis

This is TSB's primary value-add. No other outlet is doing this layer systematically.

**Questions this section answers:**
- What incentives does this create, and who is incentivized?
- Who bears the cost, and how is that cost distributed?
- What are the second and third-order effects predictable from the design?
- What failure modes are baked into the structure?
- What accountability gaps exist — who is responsible when this fails?

**Standing structural flags** — every brief checks for these known failure patterns:
- **Bundling:** Does this legislation bundle unrelated provisions, obscuring accountability and forcing false choices?
- **Vague enforcement:** Are enforcement mechanisms clearly defined?
- **Accountability gaps:** Is it clear who is responsible when this fails?
- **Perverse incentives:** Does the design reward the wrong behavior?
- **Third-party incentive gaps:** Do regulated entities, intermediaries, or platform operators have obligations and incentives aligned with the bill's stated purpose — or does enforcement depend entirely on the regulated party to surface violations?
- **Power concentration:** Does this shift power in ways that reduce future correction capacity?
- **Sunset provisions:** Is there a mechanism for review, or is this designed to be permanent by default?
- **Preemption of oversight:** Does this reduce or eliminate existing oversight mechanisms?
- **Second and third-order effects:** What does this enable, legitimize, or foreclose that wouldn't otherwise be possible? Does the bill create conditions that make the underlying problem harder to address on a future pass?

Not every flag will apply to every brief. Those that apply should be named explicitly, even if not analyzed at depth. This makes the structural section scannable and consistent across briefs over time.

**Confidence ratings are required on all structural findings,** using Textual Finding and Structural Significance from the two-axis taxonomy below. Positive findings (absence of a flag, clean design) should be rated explicitly — the absence of a collapse is itself a data point.

---

### Abstraction Layer Analysis

This section applies a systems engineering lens to the bill's or order's implementation design. It is distinct from the structural flags, which ask *what* a piece of legislation does. This section asks *how well it knows what it's doing* — whether the design separates policy goals cleanly from implementation specifics, and whether the interfaces between those layers are well-defined.

Well-architected legislation defines policy goals at the statutory layer and delegates implementation specifics to rulemaking and administration — layers that can be updated without returning to Congress. When a bill collapses those layers, the result is brittleness: implementation details that cannot be corrected without new legislation, undefined interfaces that produce inconsistent administration, and enforcement mechanisms pinned to standards that don't yet exist.

The analogy to software architecture is exact. A statute is an API contract. Rulemaking is the implementation. Administration is the runtime. Abstraction layer collapses in legislation produce the same failure modes as in software: hardcoded values that break when the environment changes, undefined function contracts that produce inconsistent behavior across callers, and SLAs baked into the interface layer that fail silently when the underlying system is unavailable.

**Checklist questions for every brief:**

- Are document or technical specifications written into statute that belong in regulation — things that will need to be updated as standards evolve?
- Are operational commitments (response deadlines, implementation windows, SLAs) hardcoded without exception handling or fallback mechanisms?
- Are there fixed historical dates or anchors that create permanent one-way doors — conditions that cannot be met retroactively regardless of future compliance?
- Are critical terms at enforcement triggers, removal triggers, or eligibility thresholds left undefined or delegated without minimum standards?
- Is liability or criminal exposure imposed at points where the underlying standard those penalties enforce is still unspecified or delegated?
- Does the bill reference organizational structures, agencies, or technology that may be outdated or in flux?
- Does the bill bypass standard administrative oversight mechanisms (notice-and-comment, Paperwork Reduction Act, etc.) that exist to catch implementation defects before deployment?
- Does the bill import definitional frameworks from other statutes or contexts without auditing whether those frameworks' scope matches the covered population of this bill? (Coverage audit — watch for definitions that carry a broader or narrower population than the bill intends.)
- Does the bill define key terms by cross-referencing other statutes, where amendments to those statutes for unrelated purposes could inadvertently alter coverage or enforcement under this bill? (Amendment drift — watch for policy couplings to implementation details in statutes the bill doesn't control.)
- Are the bill's operative layers — prohibition, enforcement, procedure, reporting — temporally and functionally synchronized? Does one layer depend on another that won't exist when the first takes effect?

Not every flag will apply to every brief. A bill with clean abstraction layering should say so explicitly — the absence of collapses is itself a data point.

**Confidence ratings are required on all abstraction layer findings,** using Textual Finding and Structural Significance from the two-axis taxonomy below.

**Note on sourcing:** Abstraction layer analysis requires reading the actual bill or order text. It cannot be performed from summaries or news coverage. The bill text should be obtained from Congress.gov or the Federal Register and reviewed directly before this section is written.

---

### What This Brief Gets Right

This section is required. Every brief must name what works — provisions that are architecturally sound, coverage choices that are well-constructed, design decisions that should be preserved in any revision. Rate these findings using the confidence taxonomy.

This section reinforces the non-opposition framing. Church Bells is not a criticism pipeline. A brief that contains only problems is either missing something or approaching its subject as an adversary rather than an analyst. Positive findings also anchor the Recommendations section: they define what should be kept when the structural problems are corrected.

Position: immediately before Recommendations.

---

### Recommendations

This section is what distinguishes TSB from opposition. We are not opposing — we are engineering.

**What this section does:**
- Identifies what functional design would look like instead
- Names alternatives that should have been considered
- Makes the kind of recommendations the Governance Design Agency would ultimately make

The framing is always: *here is the structural problem, here is what addressing it would require.* Not "this is bad" — "here is what better looks like."

---

## Confidence Taxonomy

Every finding in a Church Bells brief — legal, structural, or abstraction layer — carries explicit confidence ratings on two axes. Ratings are High / Medium / Low on each axis.

**Axis 1 — Textual Finding**
How clearly the finding is grounded in the primary source text (bill, executive order, statute).

- **High** — Unambiguous from the statutory text. Any reader of the source document would reach the same conclusion.
- **Medium** — Reasonable inference requiring interpretive judgment. The text supports the finding but does not compel it.
- **Low** — Speculative or heavily context-dependent. The finding relies on extrinsic evidence, analogy, or prediction rather than text.

**Axis 2 — varies by section**

*For legal findings:* **Litigation Risk** — how likely this finding generates a viable legal challenge.
- **High** — Strong basis for challenge; favorable precedent exists; courts have ruled this way in analogous contexts.
- **Medium** — Contested; outcome depends on jurisdiction, implementation, or how courts interpret ambiguous doctrine.
- **Low** — Weak or no basis for challenge; constitutionally sound even if structurally problematic.

*For structural and abstraction layer findings:* **Structural Significance** — how significantly this undermines the legislation's stated purpose.
- **High** — Core evasion path, enforcement failure, or design collapse that directly undermines the stated purpose.
- **Medium** — Real problem that degrades effectiveness without defeating the bill's purpose entirely.
- **Low** — Marginal or technical issue; unlikely to determine outcomes at scale.

**Required display format:** Every finding must display both axes explicitly, on a single line, immediately following the finding's prose. Use this format:

> **Textual Finding: High | Litigation Risk: Medium**

or for structural and abstraction layer findings:

> **Textual Finding: High | Structural Significance: High**

Where a finding splits across theories, each theory gets its own labeled rating block. Do not collapse multiple findings into a single shared rating. Do not substitute narrative language ("this is legally contested") for the structured format — narrative may accompany the rating but does not replace it. Consistent formatting is what makes ratings comparable across briefs over time.

**Usage notes:**
- Where a finding splits across multiple theories, each theory gets its own rating pair.
- Positive findings (architecturally sound provisions, absence of a flag) should be rated explicitly. Clean design is a data point, not a default.
- A finding can have High Textual Finding and Low Litigation Risk simultaneously — this is common for drafting artifacts and coverage gaps that are clear from the text but don't generate constitutional exposure.
- Confidence ratings apply to the *finding*, not to the political significance of the subject matter.

---

## What Makes This Different

Most legal analysis focuses on court cases — how courts have ruled or might rule. Most policy analysis focuses on political implications — who wins, who loses politically.

Church Bells does neither of those things as its primary function.

**The legal impact assessment is a vulnerability audit, not a litigation forecast.** We are reading the source code of governance and identifying where the exploits are — before anyone uses them.

**The structural analysis is incentive and failure-mode mapping.** We are asking what the system will do when this input is applied to it — not what the authors intended.

Together, these two layers answer a question that is not being answered systematically anywhere: *what does this do to the architecture of governance, rights, and accountability?*

---

## Track Record as Credential

Church Bells has no institutional credential. The field of governance architecture does not yet exist as a recognized discipline.

The credential is built through track record:
- Analyses that prove accurate over time
- Structural failures that were predicted and materialized
- A consistent, nonpartisan methodology applied regardless of political context

Every brief contributes to that record. The longitudinal body of work is the credential.

---

*See also: Church Bells Project Context, TSB Context for Church Bells*
*Analog model: [Watch Duty](https://www.watchduty.org/)*
*Long-term framework: Governance Design Agency*
