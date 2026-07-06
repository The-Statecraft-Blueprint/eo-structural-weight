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

## Transcription integrity — resolved against corpus (2026-07-03)

- Row count verified at 149, matching the paper's stated figure.
- All 149 EO numbers joined cleanly against the 10,537-order American Presidency Project corpus in `eo_coding.db`. Zero misses.
- One printed EO number was corrected pre-join: the appendix prints "12262" dated Dec. 31, 1988 ("Implementing the U.S.-Canada Free Trade Act"). EO 12262 does not exist in that range; the title and date match EO 12662, which is the number used. The clean join against the corpus (title match: "Implementing the United States-Canada Free Trade Agreement Act of 1988") confirms this correction.
- Eight printed dates in the PSQ appendix do not match the actual signing date for that EO number in the corpus. This is evidently an error in the original 2002 published appendix, not a transcription error on our end — titles match the corpus exactly in every case, only the date is wrong. Two error patterns appear:
  - **Off-by-one-year:** 9863 (printed 1946, actual 1947), 9981 (printed 1946, actual 1948), 11375 (printed 1966, actual 1967), 12369 (printed 1980, actual 1982).
  - **Month swapped (Dec ↔ Jan, day retained):** 11697 (printed Dec 17 1973, actual Jan 17 1973), 12400 (printed Dec 3 1983, actual Jan 3 1983), 12834 (printed Dec 20 1993, actual Jan 20 1993).
  - **Unrelated date entirely:** 12340 (printed May 25 1980, actual Jan 20 1982).
- **Resolution:** `mayer-price-2002-appendix-resolved.csv` supersedes the original extraction. It carries the corpus's authoritative `date_signed` for every row and flags the nine rows where the PSQ-printed date differed. EO number remains the join key throughout; titles were used only to confirm each resolution, never as the primary key.

## Usage constraint

This list was extracted after the scoring scheme and calibration codings were pre-registered and committed, and before any validation-sample EO was coded. Per pre-registration integrity: structural-weight coding of validation-sample orders must be performed against EO text using the eleven-flag rules only, without reference to this list, and the coding record should note that the coder had access to the appendix in-context. Appendix membership is revealed to the analysis only at the AUC computation step.
