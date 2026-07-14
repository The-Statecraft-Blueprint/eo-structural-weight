# Archive

Superseded results, kept for the record rather than deleted.

## Files

| File | Description |
|---|---|
| `blind-coding-results-v1-20260705.json` / `.csv` | The first full-corpus blind validation run, AUC = 0.7662. Superseded by the current run (AUC = 0.7836) after a bug in the reference-material folder used during blind coding was found and fixed — see [`../auc-results.md`](../auc-results.md) for the full trajectory, what the bug actually was, and a specific accounting of which score changes trace to the fix versus ordinary re-coding variance. |

## Why this is kept rather than removed

The point of keeping a superseded validation run isn't nostalgia — it's that the *improvement* itself is evidence. The fact that fixing a known, disclosed limitation moved the AUC up rather than down or sideways is a real, checkable claim, and checking it requires having both numbers available, not just the final one. Deleting this would make `auc-results.md`'s account of its own history unverifiable.
