# Mayer & Price 2002 Appendix — Provenance and Limitations

*Companion note to `mayer-price-2002-appendix.csv`. Created 2026-07-03.*

## Source

Kenneth R. Mayer and Kevin Price, "Unilateral Presidential Powers: Significant Executive Orders, 1949–99," *Presidential Studies Quarterly* 32, no. 2 (June 2002): 367–386. Appendix, pp. 380–384. Transcribed from the JSTOR PDF (stable URL: https://www.jstor.org/stable/27552391) uploaded by Jason on 2026-07-03.

Mayer confirmed by email (June 2026) that the original dataset underlying this paper is lost. The published appendix is therefore the surviving authoritative record of the significant-order codings.

## What this list is

The 149 executive orders coded as significant out of a pooled random sample of 1,028 orders drawn from the full population of 7,471 orders issued March 1936 – December 1999 (EO 5674 – EO 13144). Sampling: 1,000 orders drawn from March 1936 – December 1995 (17.6% of population), later extended by drawing the same fraction of orders issued January 1996 – December 1999.

An order was coded significant if it met at least one of six criteria: (1) press attention, (2) congressional notice (hearings or override legislation reaching the floor), (3) scholarly treatment in legal or presidency literature, (4) presidential emphasis via nonroutine public statement, (5) federal litigation, (6) creation of institutions with substantive policy responsibility, expansion/contraction of significant private rights, or significant departure from existing policy. The authors state they resolved ambiguity conservatively, toward insignificance.

## Critical limitation: positives only

The appendix lists the 149 significant orders. It does **not** list the ~879 sampled orders coded insignificant. Sample membership for negatives is unrecoverable. Consequences for validation design are addressed in the validation-design decision memo (pending Jason's call).

## Transcription integrity

- Row count verified at 149, matching the paper's stated figure.
- EO numbers are strictly increasing throughout the transcription, which supports the correction of one printed number: the appendix prints "12262" dated Dec. 31, 1988 ("Implementing the U.S.-Canada Free Trade Act") between 12661 and 12675. EO 12262 does not exist in that range and the title/date match EO 12662. Corrected to 12662 in the CSV, flagged in `transcription_note`.
- Eight printed dates are out of sequence with surrounding entries or inconsistent with the known signing date for that EO number (9863, 9981, 11375, 11697, 12340, 12369, 12400, 12834). These appear to be typesetting errors in the published appendix. The CSV preserves the printed date in `date_as_printed` and flags each in `transcription_note`.
- **Resolution rule:** the EO *number* is the join key and is treated as authoritative (the titles corroborate the numbers). Dates in this file are informational only; signing dates come from our own American Presidency Project corpus after the join. Any join failure by EO number gets investigated individually before the validation run.

## Usage constraint

This list was extracted after the scoring scheme and calibration codings were pre-registered and committed, and before any validation-sample EO was coded. Per pre-registration integrity: structural-weight coding of validation-sample orders must be performed against EO text using the eleven-flag rules only, without reference to this list, and the coding record should note that the coder had access to the appendix in-context. Appendix membership is revealed to the analysis only at the AUC computation step.
