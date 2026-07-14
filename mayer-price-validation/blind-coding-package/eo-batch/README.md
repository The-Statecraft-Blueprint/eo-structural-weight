# eo-batch

The 297-order text batch given to the independent blind coder — the actual scored units. Each file is one executive order's title and full text, named `order-001.md` through `order-297.md`.

**The numbering is a randomized presentation order, not chronology or grouping — this is deliberate.** It's what made the coding genuinely blind: nothing about the sequence a coder worked through these in could reveal or suggest which orders were Mayer & Price-positive versus negative. `../../validation-key.csv` (one level up in `mayer-price-validation/`) maps each `order-NNN` back to its real EO number and true class — kept confidential during coding, published now that coding is complete so the result is independently checkable.

One order — EO 9981 — is deliberately excluded from this batch. It's used as a named, repeated calibration anchor inside `../flags-canonical.md` (the worked example that teaches the CRITICAL threshold), so a blind coder scoring it would effectively be shown the answer by required reading material. Full rationale in `../README.md`.
