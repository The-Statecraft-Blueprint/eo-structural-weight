# Blind Coding Package — EO Structural Weight Score

Prepared 2026-07-05, per the independence requirement specified in `eo-structural-weight-scoring-scheme.md` v1.4, Step 2 Amendment.

## Revision history

**v2** — Two fixes from Cowork's first pilot: (1) `flags-canonical.md` narrowed to v1.2.2, requiring the Zombie Emergency Trap sub-flag to have an explicit, acknowledged statutory lapse rather than firing on any authority derived from an active emergency or wartime statute; (2) `scoring-instructions.md`'s vague NA-boundary paraphrase removed in favor of pointing directly at the more precise mechanical test already in `flags-canonical.md`.

**v3** — Added `referenced-predecessors/`, 252 reference-only files (one citation hop deep) named by real EO number, after Gemini's pilot showed that scoring an amending order with no way to see what it actually changed can produce a very different, usually understated, score. Same one-record-per-numbered-order design as always — this doesn't change what gets scored, only what the coder can consult.

**v4 (current)** — `referenced-predecessors/` rebuilt recursively: starting from all 297 scored orders, following each predecessor's own citations backward until nothing new turns up (as far as 8 links back in a few cases, mostly the export-control continuation chain). Grew from 252 files to 561. All 561 passed the same leak check as before — clean.

**Be clear-eyed about what the recursive version does and doesn't fix.** It strengthens genuine multi-hop backward chains — order A cites B, B cites C, and C matters for reading A even though A never names C directly. It does *not* solve the specific gap Cowork's second pilot flagged for order-017 (EO 11098): that order names its original 1948 ancestor (EO 10001) without naming the more recent intermediate amendment (through EO 10984) that's actually its immediate baseline. Backward citation-following can only discover *older* material a text actually names — it structurally cannot discover a *more recent* intermediate link the text doesn't mention, no matter how many hops deep it goes. `coder-instructions.md` now says this explicitly, so a coder hitting it knows to disclose the gap rather than suspect they're missing something findable.

**On sequencing:** since the reference material available to coders changed meaningfully between the 20-order pilot and this version, a fresh full run across all 297 (not just the remaining 277) keeps the dataset internally consistent — every order coded against the same reference set, rather than 20 against a shallower folder and 277 against a deeper one.

## What this is

Everything a blind coder (Gemini, Claude Cowork, or another independent coder) needs to score the Mayer & Price validation corpus, with nothing that could leak which orders are positive-class (in the published M&P appendix) or negative-class (drawn from the general population), and with a fixed, disclosed randomization applied to presentation order.

## Package contents (give ALL of this to the coder)

```
coder-instructions.md          <- the task prompt; give this to the coder first
scoring-instructions.md        <- redacted scoring rules (see "What was left out" below)
flags-canonical.md             <- full flag definitions, unredacted (see exception below)
eo-batch/                      <- 297 files, order-001.md through order-297.md, the scored units
referenced-predecessors/       <- 561 reference-only files, named by real EO number, not scored
```

**Do not include anything beyond these five items.** In particular, do not give the coder the primary scoring-scheme.md (unredacted), the notable-findings log, the eo_coding.db database, or any of my own prior coding JSON files. Any of these would leak either class labels or specific orders' known scores.

## What's NOT in this package, and why

**`validation-queue.csv`, `negative-sample-v1.csv`, `mayer-price-2002-appendix-resolved.csv`** — these are the class-membership source files. Obviously withheld.

**The primary `eo-structural-weight-scoring-scheme.md`** — withheld in full; `scoring-instructions.md` is a purpose-built redaction of it. The full document's Validation Design and Known Limitations sections name specific EO numbers alongside their known class or exact scoring outcome:
- The "Validation Design" section states that EO 9981 and EO 10924 are appendix (positive-class) EOs by name.
- The "Known Limitations" section names EO 8451 with its exact flag-correction history.
- The "What This Scheme Does Not Do" section (v1.4 addition) names EO 9467 and EO 10143 as specific low-scoring examples.

None of that is in `scoring-instructions.md`. The general principles those examples illustrated are preserved in generic form; the specific EO numbers and their known outcomes are not.

**The notable-findings log** — withheld entirely. It's organized around "here's what's interesting," which correlates with class membership more than chance would predict, and would function as a partial answer key even without stating labels outright.

**One EO excluded from the batch: EO 9981.** `flags-canonical.md` uses EO 9981 as a named, repeated calibration anchor — its exact flag tally (5 PRESENT, 0 CRITICAL) is stated explicitly, more than once, to teach the CRITICAL threshold. Redacting those examples out of `flags-canonical.md` would degrade a genuinely useful piece of the training material for no good reason, so instead EO 9981 itself is simply not in the blind batch. My original label-aware coding of EO 9981 carries forward into the combined dataset as a documented exception — see `answer-key-DO-NOT-DISTRIBUTE.csv` (kept separately, see below). This is why the batch is 297, not 298.

## The answer key

`answer-key-DO-NOT-DISTRIBUTE.csv` (delivered as a separate file, not inside this package) maps each `order-NNN` back to its real EO number and true class (positive/negative). **Do not show this to the coder at any point before or during coding.** Keep it until the blind pass is complete, then use it to compute AUC and inter-coder agreement.

## How to run this

**With Gemini:** paste `coder-instructions.md`, `scoring-instructions.md`, and `flags-canonical.md` into the context, then work through `eo-batch/` — either pasting files in batches of 20–30, or uploading the whole folder if the interface supports it. If Gemini has web search or browsing enabled, turn it off for this task, or add an explicit reminder before each batch that searching is off-limits — the "What Not To Do" section in `coder-instructions.md` says this, but a model with live search access is worth a second, session-level safeguard.

**With Claude Cowork:** hand it the whole `blind-package` folder (with the answer key kept out of it, on a different path Cowork isn't pointed at) and `coder-instructions.md` as the task description. Cowork's lack of this conversation's context is a feature here, not a limitation — it has never seen any of my prior codings or the findings log, so there's nothing to accidentally leak from that direction. Same caution on search/browsing tools as above.

**Recommended: pilot first.** Before committing either coder to all 297, consider running just the first 15–20 files in `eo-batch/` (they're already randomly ordered, so the first N is a valid random subsample) and spot-checking the output format and reasoning quality before turning them loose on the rest. This mirrors the project's own ICR-pilot-before-full-commitment precedent.

## After coding is complete

1. Match each returned record back to its true EO number and class using the answer key.
2. Compute AUC for that coder's scores against the true class labels — this is the number that actually answers the pre-registered ≥0.70 question.
3. If more than one coder ran the full batch, compute inter-coder agreement between them across all 297 — this is a far stronger reliability estimate than the original 30-EO ICR pilot could support.
4. EO 9981 is not part of this AUC computation (it's not in the blind batch). If you want it included in a combined final number, my original coding is the only one available for it, and that should be disclosed as a label-aware carryover rather than blind data, consistent with the v1.4 amendment.

## One honest caveat this package can't fully solve

Positive-class EOs are, by construction, the ones Mayer & Price published in an appendix. If a coder has live web search enabled and searches for an order by its own number and title (both of which appear in the order's text, unavoidably), a sufficiently motivated search could surface that it's discussed in the Mayer & Price literature. This package can instruct against it and disable tool access where possible, but it can't force a coder not to search. This is worth being aware of as a residual risk when interpreting results, not something to treat as fully closed off.
