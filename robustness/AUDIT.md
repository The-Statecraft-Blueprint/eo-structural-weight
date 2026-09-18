# Robustness Audit: What Holds, What Doesn't, What Is Untested

*2026-09-18. Every number below comes from `audit.py` (numpy only, deterministic seed 20260918). The full output is in `audit-output.json`. Re-run with `python3 robustness/audit.py`.*

This audit was prompted by a review which found that the divergence examples in `mayer-price-validation/comparison-to-mayer-price.md` were taken from the label-aware original coding, although the document says they come from the blind run. It checks that finding and then looks for other weak points a discussant could find.

---

## 1. Validation (Mayer & Price AUC)

| Coding | Label-aware? | n | AUC | 95% bootstrap CI |
|---|---|---|---|---|
| Original (`claude-church-bells-v1`) | yes | 297 | 0.673 | 0.615–0.731 |
| Blind v1 | no | 296 | 0.766 | 0.712–0.818 |
| **Blind v2 (reported)** | no | 297 | **0.784** | **0.731–0.835** |

**Holds:** the 0.78 is computed from the blind run, and the CI stays above the pre-registered 0.70 floor only barely, so it should be reported with the CI. The label-aware coding scored *lower* (0.67), so knowing the labels didn't inflate the result.

**New vulnerability: document length does almost as well as the score.**

- Word count alone separates the classes with AUC = 0.781, virtually the same as the score. Year alone gives 0.645.
- The score does add information beyond length and year. In a logit model, adding it improves the fit by likelihood-ratio χ² = 31.6 (1 df), and AUC rises from 0.788 to 0.837.
- Within length terciles the score's AUC is 0.717, and 0.740 within length-tercile × era cells.
- The positive and negative classes also differ in era: positives cluster in 1970–99, while 22 of the 149 negatives come from the 1930s against 2 positives. Within-decade AUC is 0.782, so era isn't driving the result.

**What to report:** the AUC with its CI, the word-count baseline, and the within-length AUC (0.72). A discussant will ask whether the score is just a length proxy. The answer is "partly, but not only," and the paper should say so before being asked.

**Untested:** recognition. The blind coder saw each order's number, title, date and president, so it could have known which orders are famous. The masked re-coding test (`masked-recode/`) is designed to settle this.

## 2. Divergence examples

Using the blind-v2 figures, as the comparison document claims to:

| EO | Doc said | Original | Blind v1 | Blind v2 | Verdict |
|---|---|---|---|---|---|
| 12139 FISA implementation | 0.0 | 0.0 | 18.2 | 18.2 | **fails** |
| 11785 ends AG's list | 0.0 | 0.0 | 0.0 | 18.2 | **fails in v2** |
| 12958 classification | 4.5 | 4.55 | 27.3 | 31.8 | **fails badly** |
| 13010 critical infrastructure | 6.25 | 6.25 | 21.4 | 4.55 | unstable |
| 11375 sex discrimination | 5.0 | 5.0 | 4.5 | 4.55 | holds |
| 12088 federal pollution compliance (notable-findings "flagship") | 4.5 | 5.0 | 13.6 | 40.9 | **fails badly** |
| 11615 wage-price freeze | 31.8 | 31.8 | 40.9 | 50.0 | holds (heavier) |
| 9250 "Hold the Line" | 45.5 | 45.5 | 40.9 | 45.5 | holds |
| 9001 war contracting | 31.8 | 31.8 | 36.4 | 45.5 | holds (heavier) |
| 8565 Romania property control | 27.8 | 27.8 | 38.9 | 31.8 | holds |
| 12318 OIRA statistics | 8.3 | 8.3 | 13.6 | 13.6 | roughly |

**Why so many "significant but clean" examples fail: knowing the labels pushed significant orders down.** The original coder knew which orders Mayer & Price had flagged.

- It scored those orders **8.3 points lower on average than blind v2** (7.0 lower than blind v1): mean 10.9, against 19.2 and 17.9 in the blind runs.
- Non-significant orders moved only 1.5 points (0.6 against v1).
- In the original coding, 64% of significant orders score ≤10. Only 26% do in all three codings.

This fits the notable-findings log, which says the original coder "repeatedly flagged and explained" low-scoring significant orders as it met them. The coder was primed to find the "significant but architecturally clean" story, and found it more often than blind coders did. It also explains why the original coding's AUC (0.67) is *lower* than the blind runs'. The whole Type-A divergence index in `findings/notable-findings.md` has to be treated as a hypothesis generated under label awareness, not as a finding.

**Examples that hold in all three codings** (full lists in `audit-output.json` → `divergence`):

- *Significant but clean* (Mayer & Price positive, ≤10% in every coding; 38 orders): EO 9808 (Truman's President's Committee on Civil Rights, 0/0/0), EO 12202 (Nuclear Safety Oversight Committee, 1980), EO 12183 (revoking Rhodesian sanctions, 1979), EO 12961 (Gulf War veterans' illnesses committee, 1995) and EO 11375 (≈5 in all three).
- *Heavy but not in Mayer & Price's appendix* (negative, ≥25% in every coding; 6 orders): EO 9250, EO 9246, EO 11940 (export controls continued after the statute lapsed, 1976), EO 9001, EO 8565, EO 11190.
- *Both significant and heavy* (≥30% in every coding; 9 orders): EO 9102 (War Relocation Authority), EO 11615, EO 11796, EO 9570, EO 12735, EO 10193, EO 9040, EO 9661, EO 9989.

**Rule going forward:** name an order as an example only if it meets the claim in every available coding, and show all the scores.

**Instability:** 52 of 296 orders differ by 20 points or more across the three codings. The largest spreads:

- EO 12730: 54.5 / 13.6 / 50.0
- EO 9279: 18.2 / 59.1 / 40.9
- EO 9253: 0.0 / 35.0 / 40.9

Any single order's score is noisy. Claims about individual orders need the multi-coding check above.

## 3. Reliability

| Pair | Flag κ | Score ICC(2,1) | Pearson r | Mean abs. diff |
|---|---|---|---|---|
| Original vs blind v2 | 0.427 | 0.664 | 0.722 | 7.3 pts |
| Original vs blind v1 | 0.453 | — | 0.675 | — |
| Blind v1 vs blind v2 | 0.663 | 0.817 | 0.819 | 5.4 pts |
| ICR pilot, 30 orders: Gemini / GPT vs original | 0.20–0.49 | 0.50–0.73 | 0.76–0.84 | 5–18 pts |

**Weakest flags** (original vs blind v2 κ): Flag 10 Inter-Agency Cannibalization 0.06, Flag 11 Exemptions 0.11, Flag 3 Bundling 0.17, Flag 9 Second-Order Effects 0.25. These four flags carry little reliable signal. A sensitivity analysis scoring on the seven more reliable flags is worth adding.

**Gaps:**

- **Zero human codings** exist anywhere in the database.
- **Zero of the 6,844 extension orders** behind the long-run trend were coded twice.
- Both blind runs used the same model family that helped design the rubric. The v1.4 pre-registration amendment asked for a cross-vendor blind coder "where feasible", and none was used.

**Holds:** the Zombie Emergency Trap fired on the same four orders (11796, 11810, 11940, 12730) in all three codings. One caveat applies. The ZET test was narrowed in blind package v2 after a pilot compared it with "established practice", meaning the original coding. So agreement with the original coding is partly built in.

## 4. The long-run trend

Extension codings only (streams A and B, 6,844 orders).

**Composition drives most of the rise.** Zero-score orders fall from 90% of the total in the 1930s to 2% in the 2020s. Splitting the change in the mean into composition (share of orders with any flag) and within-order weight:

| Change | Total | Composition | Within-order |
|---|---|---|---|
| 1930s → 2020s | +30.8 | +24.1 (78%) | +6.7 |
| 1950s → 2010s | +14.8 | +10.3 (70%) | +4.5 |
| Reagan → Trump 1st term | +11.3 | +11.4 (≈100%) | 0.0 |
| Trump 1st → Trump 2nd term | +12.3 | +2.0 (16%) | +10.3 |

**Composition is largely document length.** Median length rises from 184 words (1930s) to 1,094 (2020s). Zero-score share by length quintile: 77%, 72%, 61%, 34%, 16%.

**Like-for-like comparison:** long orders only (top length quintile, >842 words), mean score with 95% CI:

| | Mean | CI |
|---|---|---|
| FDR | 13.4 | 10.6–16.5 |
| Truman | 23.5 | 19.6–27.9 |
| Eisenhower–Ford | 10–17 | |
| Carter | 20.9 | 16.2–26.4 |
| Reagan | 29.2 | 23.2–36.4 |
| Bush 41 | 31.5 | 25.0–38.5 |
| Clinton | 29.9 | 27.7–32.3 |
| Bush 43 | 29.3 | 26.9–31.6 |
| Obama | 32.1 | 30.2–34.0 |
| Trump 1st | 31.3 | 29.5–33.0 |
| **Biden** | **34.6** | 32.4–36.7 |
| **Trump 2nd** | **44.3** | 41.7–46.9 |

The defensible statement is:

1. The average rose mainly because orders stopped being short, machinery-free housekeeping documents.
2. Among orders that build something, weight stepped up around Reagan, held flat through Trump's first term, and rose under Biden and sharply under Trump's second term.

**New vulnerability: a seam between coder streams at 1953.** Stream A (FDR–Truman) and stream B (Eisenhower on) were separate coding efforts.

- The zero-score share jumps from 37.5% (stream A, 1951–52) to 68.1% (stream B, 1953–54).
- Among long orders, the mean falls from Truman's 23.5 to Eisenhower's 11.6.
- This might be real, but it sits exactly on the coder boundary. The masked test re-codes 10 orders from each side of the seam (H4). Until then, don't compare levels across 1953.

**New vulnerability: the coder knew the administration in every batch.** Stream B was coded one administration per batch (e.g. `batch-14-trump2.json`), so administration is perfectly confounded with coding session. In addition, the rubric's own CRITICAL calibration anchor is a 2025 order (EO 14257). The recent rise is the part of the trend most exposed to this bias. The masked test (H2) is designed to measure it.

**Seven-flag sensitivity:** dropping the four least reliable flags (3, 9, 10, 11):

- The blind-v2 AUC holds at 0.769.
- The recent rise holds. Among long orders: Trump 1st term 30.6, Biden 33.1, Trump 2nd term 42.5.
- The "flat from Reagan to Trump's first term" plateau does **not** hold cleanly. Long-order means go Reagan 17.5, Clinton 19.2, Bush 43 21.9, Obama 28.0, Trump 1st term 30.6, a gradual rise.

So the plateau depends on which flags are counted and should be stated with that caveat. The rise since 2021 is robust to the flag set.

**Trump's second term is mostly 2025.** The 2025 mean is 37.7 (237 orders). The partial 2026 figure is 29.5 (42 orders), back in the Biden range. Report the second-term figure by year as well as pooled.

**Annual series rebuilt:** `annual-series-rebuilt.csv` replaces the label-aware original coding with blind-v2 for the 297 validation orders, and adds zero-share, mean-if-nonzero and long-order columns. The older `extension/annual-structural-weight.csv` mixes in 306 label-aware codings.

## 5. Data quality

- `eos.word_count` is NULL for all 10,537 rows. Length has to be computed from `corpus-texts/`.
- Two orders (EO 14412, 14413) had a garbled `president` field ("Donald J. Trump (2nd Term)47th President of…"). This is fixed in `database/eo_coding.db`; see `data-fixes.md`.

## 6. What remains to be done

1. **Masked re-coding test** (`masked-recode/`), with at least two cross-vendor AI coders × 2 arms. Target date: March 18, 2027.
2. **Human hand-coding of the 80-item subset.** Ideally a second human coder who didn't design the rubric codes it too.
3. **Rebuild the trend chart** from `annual-series-rebuilt.csv`. Show the zero-share and long-order series next to the raw mean, so the composition story is visible on the figure itself.
4. **Re-check the Reagan-era step.** Among long orders, weight jumps from Carter to Reagan with all 11 flags (20.9 → 29.2) and with 7 (10.1 → 17.5). It's the largest single step before 2021. Read a sample of the flags that fire on Reagan-era long orders to see whether this is substance (e.g. regulatory-review machinery) or a shift in coding style.
