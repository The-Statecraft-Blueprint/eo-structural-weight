# Source Data

The inputs the validation sample was built from — Mayer & Price's own published classification, the matched random draw that completes the sample, and the record of how the calibration set was established before any of it was coded for real.

## Files

| File | Description |
|---|---|
| [`mayer-price-2002-appendix.csv`](mayer-price-2002-appendix.csv) | The 149 positive-class orders — every executive order Mayer & Price (2002) classified as "significant" in their published appendix, resolved to a clean, citable list. |
| [`mayer-price-2002-appendix-provenance.md`](mayer-price-2002-appendix-provenance.md) | How that appendix list was actually reconciled into the CSV above — the source, the resolution process, and any judgment calls made along the way. Read this before trusting the appendix CSV blindly. |
| [`mayer-price-2002-appendix-as-printed.csv`](mayer-price-2002-appendix-as-printed.csv) | The raw as-printed extraction from the PSQ appendix, before the date corrections described in the provenance doc above were applied. Kept for the same reason the provenance doc's correction narrative is kept — so the "before" state of the eight corrected dates is inspectable, not just described in prose. |
| [`negative-sample-v1.csv`](negative-sample-v1.csv) | The 149 negative-class orders: a random draw from the general population of executive orders, matched in scale to the positive class. Seed `20260703`, disclosed for reproducibility — re-running the draw with the same seed reproduces the same sample. |
| [`calibration-record.md`](calibration-record.md) | The initial 10-order calibration set, coded before the full 298-order validation batch began, used to pressure-test the scoring scheme and flag definitions while they could still be revised without contaminating the actual validation run. |
| `calibration-set/` | The actual text of those 10 calibration orders (9066, 9981, 10924, 11069, 12291, 12717, 13228, 13769, 14257, 14412), one JSON file per order. |
| `policy-agendas-project/` | Background data from the Policy Agendas Project's executive orders coding effort (codebooks, their own EO dataset, citations) — an independent classification this project's positive/negative sample can be cross-checked against, and the provenance trail for how the corpus itself was originally assembled (`scrape_app_eos.py`, the American Presidency Project scraping script). Not yet used in any published comparison, kept here for that future work. |

## Why the split between positive and negative class

Mayer & Price's own significance judgment only tells you about the 149 orders they flagged — it says nothing about how structural weight behaves on everything *else*. The negative sample exists to test both directions at once: does structural weight stay low on routine orders, and does it correctly separate the two populations. The full accounting of how well it does that is in [`../auc-results.md`](../auc-results.md).
