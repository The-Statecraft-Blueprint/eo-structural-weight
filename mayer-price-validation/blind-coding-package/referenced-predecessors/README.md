# referenced-predecessors

612 reference-only files, named by real EO number (`EO-{number}.md`) — **not part of the scored batch.** These exist so that when an order in `../eo-batch/` says "EO 10651 is hereby amended" or "EO 10651 is revoked," the blind coder can actually see what EO 10651 said, rather than guessing or scoring the amending order as if it existed in a vacuum.

`INDEX.csv` maps each predecessor number to its citing order(s).

## How this was built, and its one real limit

Built as a recursive backward citation walk: starting from all 298 orders in the validation sample, following each cited predecessor's own citations backward until nothing new turns up (as far as 8 links back in a few cases — mostly a long-running export-control continuation chain). This can only discover *older* material a text actually names. It structurally cannot discover a more recent intermediate amendment that isn't cited — if an order says "amending the regulations established by EO 10001" without naming a closer amendment that's actually its operative baseline, that closer amendment may not be here even though it exists in the historical record. This is a disclosed, known limitation, not a bug — see `../coder-instructions.md` for how a coder handles hitting it (state the gap explicitly rather than guess).

## A version-history note, since this folder went through real revisions

An earlier version of this folder had a logic bug — any predecessor that happened to also be one of the 298 validation orders was incorrectly excluded, even when something else in the batch cited it. That was found and fixed after the first blind run had already used the buggy version; the specific, measured cost of that bug (and why it pulled scores toward zero rather than introducing errors) is documented in `../../auc-results.md`, since it's part of the AUC's own trajectory, not just this folder's history.
