# Masked Re-coding Test: Analysis Plan

*Written 2026-09-18, before any masked-test data exists. Commit this file, `build_package.py` and `analyze.py` before the first coder sees a packet. After that, change none of them except to fix a bug, and log any bug fix at the bottom of this file with its date. Target completion: March 18, 2027.*

## Why this test exists

Every AI coding in the project so far showed the coder each order's number, title, date and president. That leaves three open questions a discussant can raise:

1. **Recognition.** The blind run may separate Mayer & Price's significant orders from the rest (AUC 0.78) partly because the coder recognized famous orders, not only because of the rubric.
2. **Administration knowledge.** The extension corpus was coded in batches, one administration per batch, and the coder always knew which president it was coding. Any shift in the coder's expectations by administration is fully confounded with the administration itself. The recent rise (Biden, then Trump's second term) is exactly where that matters. The rubric's own CRITICAL calibration anchor in `flags-canonical.md` is a 2025 order (EO 14257), which is a specific channel for this bias.
3. **Reliability.** None of the 6,844 extension orders behind the long-run trend has been coded twice. The only agreement figures are between AI runs on the validation sample: flag-level κ = 0.43 between the blind run and the original coding, and 0.66 between the two blind runs.

## Design

The same 210 orders are presented in two arms that differ only in what the coder can see. Nothing else changes: same instructions, same model version, and no predecessor texts in either arm.

- **Arm M (masked):** number, title, date, signer, signature block, filing notes, years, dates, and citation numbers (EO, proclamation, Public Law, Stat., FR, Congress) are removed. See `build_package.py` for the exact rules and `_sealed/redaction-log.csv` for per-item counts.
- **Arm U (unmasked):** the order as it was shown in the blind run.

The sample was drawn with seed 20260918:

| Stratum | n | Purpose |
|---|---|---|
| V-pos / V-neg | 40 / 40 | Recognition test (H1); drawn from the 297-order blind set |
| X1 1936–1950 | 20 | Reliability, stream A |
| X2 1951–1954 | 10 + 10 | Seam between extension streams A and B (H4) |
| X3 1955–1980, X4 1981–2000, X5 2001–2020 | 20 each | Reliability across eras |
| X6 Biden / Trump 2nd term | 15 / 15 | Administration-knowledge test (H2) |

A human hand-coding subset of 80 masked items (30 V, 50 X) is listed in `human-coding/human-coding-sheet.csv`.

### Coders

- Use at least two AI coders from different vendors, ideally three, including at least one that isn't a Claude model.
- Each coder codes both arms, in separate fresh sessions with no project context.
- Run arm M first, so the masked session can't be influenced by having seen the unmasked texts.
- Record the exact model and version string for each run. Save results as `results/arm-M/<coder>.json` and `results/arm-U/<coder>.json`, using the same `<coder>` name for both arms.
- Human coders code masked items only and never open `_sealed/` or the database until their sheet is final (see `human-coding/HUMAN-PROTOCOL.md`).

## Hypotheses and decision rules (fixed now)

`analyze.py` recomputes every score from the flag statuses. It doesn't trust a coder's own arithmetic.

**H1: Recognition inflates validation.** Statistic: AUC(U) − AUC(M) on the 80 V items, with a paired bootstrap 95% CI.
- If the difference is ≥ 0.05 and the CI excludes 0, recognition inflation is **confirmed**. The masked AUC becomes the headline validation figure, and the 0.78 is reported only alongside it.
- If masked AUC < 0.70, the validation claim is downgraded to "partial convergent validity" (0.60–0.70) or "not established" (< 0.60), following the original pre-registration's bands.
- Also reported: the masked AUC on items the coder didn't recognize.

**H2: Administration knowledge inflates the recent rise.** Statistic: the gap in mean score between Trump's second term and 2001–2020, in each arm, with bootstrap CIs.
- If the masked gap is less than half the unmasked gap, or its 95% CI includes 0, the Trump-second-term rise is **not reported as a finding**. It is then described as not robust to masking.
- Also reported: mean(U − M) for every stratum.
- Power note: with 15 vs 20 orders this only detects large effects. A null result here isn't proof that no bias exists.

**H3: Reliability of the existing codings.** Statistics: flag-level Cohen's κ and score-level ICC(2,1), comparing each new coding with the existing coding (blind-v2 for V items, extension for X items). Each AI coder and the human coder are compared separately.
- ICC interpretation follows Koo & Li (2016): below 0.50 is poor, 0.50–0.75 moderate, 0.75–0.90 good.
- If the extension ICC for every masked AI coder is < 0.50, the long-run trend is **not reported as a finding**.
- If it is 0.50–0.75, the trend is reported with the reliability figure stated next to it.
- κ is reported as is, with no threshold, because κ below 0.60 on 11 flags with a 4-level scale is common. The human coder's κ against the AI codings is the reliability anchor to cite.

**H4: Coder-stream seam in 1953.** Statistic: mean(existing − fresh unmasked re-code) for stream-A (1951–52) orders versus stream-B (1953–54) orders.
- If the two means differ by more than 5 points and the CIs don't overlap, a coder-stream artifact at 1953 is **confirmed**. Pre-1953 and post-1953 levels are then not compared directly.

**H5: Masking worked.** Statistics: the share of masked items where the coder says it recognized the specific order, and the share where it guessed the decade within ±10 years.
- If more than 25% of masked V items are recognized, H1 is reported as **inconclusive**.

## What gets reported regardless of outcome

The paper reports all five results, including any that go against the project. It does not re-run the test with different coders or redaction rules until a preferred result appears. If a second round is run for a documented reason (for example, a coder failed to complete), both rounds are reported.

## Bug-fix log

*(empty)*
