# Task: Score 210 Executive Orders Against a Governance-Architecture Rubric

You are an independent coder for a research project on governance architecture. Score each order in `items/` against the eleven-flag rubric.

## What you have

1. `scoring-instructions.md`: status vocabulary, scoring math and record format.
2. `flags-canonical.md`: the authoritative definition of each flag. Read both documents in full before starting.
3. `items/order-001.md` to `items/order-210.md`: one executive order per file, with its number, title and full published text.

## About the texts

Each file shows the order exactly as published, including its number, title and signature block.

## Differences from the scoring instructions

- **No predecessor texts are provided.** `scoring-instructions.md` mentions a `referenced-predecessors/` folder, but this exercise doesn't have one. When an item amends, revokes or extends another order, score from the item's own text. In the justification for each affected flag, say that the predecessor wasn't available. Don't guess at what the predecessor contained.
- Work through the items in numerical order and don't re-sort them.

## Record format

Return a JSON array with one object per item:

```json
{
  "order_id": "order-001",
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

**Fill in `after_coding` only after all eleven flags for that item are scored.** For this packet, the decade and president guesses are trivial. What matters is `recognized_specific_order`: did you know this order and what it is historically known for before you read it? This field isn't part of the score. Answer honestly either way.

Batches of 20–30 items per response are fine. Keep the `order_id` labels exact.

## Scoring notes

- There's no expected distribution and no target average. Score what's in front of you.
- Length doesn't tell you the score. Judge the architecture, not the word count.
- If the rubric is ambiguous for an item, make your best call, note the ambiguity briefly and move on.
