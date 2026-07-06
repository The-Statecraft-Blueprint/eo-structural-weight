# Task: Score 297 Executive Orders Against a Governance-Architecture Rubric

## Your task

You are one of two (or more) independent coders scoring a batch of executive orders for a research project on presidential governance architecture. You will score 297 executive orders, one at a time, against an eleven-flag rubric described in the accompanying documents.

You have not been told anything about how these 297 orders were selected, what hypothesis they are testing, or whether any prior coder has already scored them. That is intentional. Your value to this project comes specifically from arriving at a score without that context. Please do not attempt to reconstruct it, infer it, or look it up.

## What you have

1. **`scoring-instructions.md`** — the scoring rules: status vocabulary, point values, the aggregation formula, and the exact record format to report for each order.
2. **`flags-canonical.md`** — the full definition of each of the eleven flags, including the operational test for each one, illustrative language, and the boundary between adjacent flags. This is the authoritative document for what each flag means.
3. **`eo-batch/`** — a folder of 297 files, named `order-001.md` through `order-297.md`. Each file contains one executive order's title and full text, and nothing else. The numbering in the filenames reflects the order in which you should work through them; it carries no other meaning (it is not chronological and is not grouped by any property of the orders — please preserve the given sequence rather than re-sorting by date, subject, or apparent length).
4. **`referenced-predecessors/`** — a folder of reference-only files, named by their real EO number (e.g., `EO-10651.md`), containing the full text of any order connected by citation to something in `eo-batch/` — not just direct citations, but citations-of-citations, followed backward as far as the chain goes (up to 8 links deep in a few cases). `INDEX.csv` maps each predecessor number to its hop depth and which order(s) cite it directly. **These are not part of what you score.** They exist purely so that when an order in your batch says "EO 10651 is hereby amended" or "EO 10651 is revoked," you can see what EO 10651 said — and if EO 10651 itself was amending something earlier, that's in here too. If you need to trace back further than the order's immediate citation, check whether the predecessor's own file also cites something earlier; if it does, that further-back order is in this same folder. If an order cites a predecessor by number and that number isn't in `referenced-predecessors/` either, it genuinely wasn't recoverable — note that as a limitation per the coding conventions in `scoring-instructions.md`, rather than treating the order as if no predecessor existed.

    **One real limit worth knowing about:** this only follows citations *backward* in time — toward what an order's text actually names as its own ancestor. It cannot discover a *more recent* intermediate amendment that isn't named. If an order says "amending the regulations established by EO 10001" without also naming a closer, more recent amendment that's actually the operative baseline, that closer amendment may not be in this folder even though it exists somewhere in the broader historical record. If you hit this, treat it the same way as any other unrecoverable predecessor: assess what you can from the text and reference material available, and say plainly that a more immediate baseline may exist but wasn't reachable — don't guess at its contents.

## What to do

Read `scoring-instructions.md` and `flags-canonical.md` in full before starting. Then, for each file in `eo-batch/`, in the given sequence:

1. Read the order's text.
2. **If the order references a prior EO by number as something it amends, extends, revokes, or supersedes, check `referenced-predecessors/` for that number before proceeding.** This is not optional background reading — several orders in this batch score very differently depending on whether the comparison the diff-aware convention calls for is actually made. A short order that quietly replaces a detailed predecessor with a one-sentence blank delegation looks unremarkable on its own four sentences; it only reads correctly against what it replaced.
3. Score all eleven flags per the rubric, incorporating that comparison where relevant.
4. Compute the aggregation fields.
5. Produce the structured record specified in "What You Should Report" in `scoring-instructions.md`.

Please complete all 297 before reporting results — a partial batch is much less useful than a complete one, since the project needs the full set to compute how well the scores as a whole separate two groups it has not disclosed to you.

## Output format

Please return one record per order, in the same sequence as the input files, clearly labeled by the file's order number (e.g., "order-001," "order-014"). A structured format (JSON array, or one clearly delimited block per order) is preferred over free-flowing prose, since these results will be parsed programmatically. If you're working within a single conversation and the full 297 records would be unwieldy in one response, batches of 20–30 at a time are fine — just keep the order-number labeling consistent so the batches can be reassembled correctly.

## A few things worth saying directly

- There is no "expected" number of orders that should score high or low, no target average, and no reason to expect any particular distribution. Score what's in front of you.
- Some orders are one paragraph; others are several pages. Length is not itself informative about the score — some very short orders score high, and some very long ones score at or near zero. Judge the architecture, not the word count.
- Some orders reference other executive orders by number as amendments or extensions. The coding conventions in `scoring-instructions.md` explain how to handle this. If a referenced predecessor order's text isn't in your batch, say so in your notes rather than guessing at its contents.
- If anything in the rubric is genuinely ambiguous for a specific order, make your best judgment, note the ambiguity briefly, and move on — don't get stuck on any single order at the expense of finishing the batch.
