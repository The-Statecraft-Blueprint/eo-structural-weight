# Methodology

The instrument itself — frozen, pre-registered, and shared across every other part of this project. Both the Mayer & Price validation and the full-corpus extension apply exactly what's defined here; nothing about the scoring rules changes between them.

## Files

| File | Description |
|---|---|
| [`flags-canonical.md`](flags-canonical.md) | The authoritative definition of all eleven structural flags — what each one tests, the operational test for firing it, key distinctions (e.g., what does and doesn't count as a sunset provision), and the NOT_APPLICABLE decision-structure rule. Currently **v1.2.2**. |
| [`scoring-scheme.md`](scoring-scheme.md) | The full scoring scheme: status vocabulary (ABSENT/PRESENT/CRITICAL/NOT_APPLICABLE), how status maps to points, the aggregation formula, coding conventions (diff-aware amendment comparison, incorporation-by-reference), and the validation design that governs how independence from label-awareness is tested. Currently **v1.4**. |

## Why these are frozen

Both documents carry full version histories inside them. Flag definitions and the confidence taxonomy were frozen once pre-registration was complete, specifically to prevent the instrument from being tuned to whatever corpus it's currently being tested against. Process and procedural clarifications are added as dated amendments — visible in each document's own changelog — rather than quietly edited in place. If a flag definition ever needs to substantively change, that's a new version number and a stated reason, not a silent edit.

## Reading order

`flags-canonical.md` first — it's the thing being applied. `scoring-scheme.md` second — it's how individual flag calls become a single structural-weight percentage, plus the rules for edge cases (amendments, incorporation, missing text).
