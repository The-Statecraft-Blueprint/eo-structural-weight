# Task: Score 210 Executive-Branch Orders Against a Governance-Architecture Rubric

You are an independent coder for a research project on governance architecture. Score each item in `items/` against the eleven-flag rubric.

## What you have

1. `scoring-instructions.md`: status vocabulary, scoring math and record format.
2. `flags-canonical.md`: the authoritative definition of each flag. Read both documents in full before starting.
3. `items/item-001.md` to `items/item-210.md`: one order per file.

## About the texts

Identifying details have been removed on purpose: the order's number, title, date, signer, signature block and filing notes. Inside the text, years, dates, and citations to other numbered orders, proclamations, Public Laws, the Statutes at Large, the Federal Register and numbered Congresses have also been replaced with placeholders such as `[YEAR]`, `[DATE]`, `[EO-A]` and `[STAT]`. Placeholders are consistent within one item, so `[EO-A]` refers to the same order everywhere in that file, but not across items.

Please score what the text does. Don't try to work out which order it is, when it was issued or who issued it.

## Differences from the scoring instructions

- **No predecessor texts are provided.** `scoring-instructions.md` mentions a `referenced-predecessors/` folder, but this exercise doesn't have one. When an item amends, revokes or extends another order, score from the item's own text. In the justification for each affected flag, say that the predecessor wasn't available. Don't guess at what the predecessor contained.
- Work through the items in numerical order and don't re-sort them.

## Record format

Return a JSON array with one object per item:

```json
{
  "item_id": "item-001",
  "flags": [
    {"flag_number": 1, "flag_name": "Power Concentration", "status": "ABSENT|PRESENT|CRITICAL|NOT_APPLICABLE",
     "points": 0, "justification": "one or two sentences citing the text", "sub_flag_fired": false}
    // ... all 11 flags
  ],
  "applicable_count": 0, "raw_score": 0, "max_possible": 0, "structural_weight_pct": 0.0,
  "after_coding": {
    "guess_decade": "e.g. 1950s, or unknown",
    "guess_president": "name, or unknown",
    "recognized_specific_order": false,
    "recognized_as": "",
    "confidence_in_guess": "low|medium|high"
  }
}
```

**Fill in `after_coding` only after all eleven flags for that item are scored.** It's a check on how well the masking worked, and it isn't part of the score. An honest "unknown" is the most useful answer when you don't know.

Batches of 20–30 items per response are fine. Keep the `item_id` labels exact.

## Scoring notes

- There's no expected distribution and no target average. Score what's in front of you.
- Length doesn't tell you the score. Judge the architecture, not the word count.
- If the rubric is ambiguous for an item, make your best call, note the ambiguity briefly and move on.
