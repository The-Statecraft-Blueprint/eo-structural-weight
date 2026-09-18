# EO Structural Weight — Full Corpus, 1936–2026

*Step 4 of the pre-registered order of operations. This is the dataset behind the annual trend chart, along with what it covers, what it doesn't, and how it was assembled.*

## Coverage

**7,149 of 7,151 executive orders from 1936–present carry a structural weight score.** The two gaps are known and documented, not oversights:
- **EO 9681** has no published text anywhere in the source corpus. It's coded — the three always-answerable decision-structure flags are scored from the title alone — but with no defined percentage, since a real denominator requires knowing what the other eight flags would find.
- **One very recent June 2026 order** (on regenerative agriculture) whose official EO number hadn't been assigned yet when the source corpus was built.

Composition, by `coder_id` in `../database/eo_coding.db`:
- **306 orders** — primary coding (`claude-church-bells-v1`), the original Mayer & Price validation census plus calibration set.
- **3,032 orders** — `cowork-extension-stream-a`, FDR and Truman, 1936–1953. Raw output in `stream-a/`.
- **3,812 orders** — `cowork-extension-stream-b`, Eisenhower through the present. Raw output in `stream-b/`.

Zero duplicate scoring, zero overlap between the two extension streams, zero overlap between either stream and the primary coding — verified directly against every batch file, not assumed.

## What's here

| File | Description |
|---|---|
| `annual-structural-weight.csv` | Year, order count, mean and median structural weight, 1936–2026 |
| `annual-structural-weight-chart.png` | The chart: raw annual mean/median plus a 5-year rolling mean for readability |
| `stream-a/` | 11 raw batch files (one per year or short year-range) plus `notable-patterns-log.md` |
| `stream-b/` | 14 raw batch files (one per administration) plus one `notable-patterns-log*.md` per batch |

The consolidated database itself — every record from every coder, fully queryable — lives at [`../database/eo_coding.db`](../database/eo_coding.db).

## Reading the trend

*Revised 2026-09-18. See `../robustness/AUDIT.md` §4 for every figure below and how it was computed.*

Mean structural weight rises from about 1–3% in the late 1930s to 30–38% in the 2020s. **Most of that rise is a change in the mix of orders, not in how heavy individual orders are:**

- Orders with no governance machinery at all (score 0) fall from 90% of all orders in the 1930s to 2% in the 2020s.
- Median order length rises from 184 to 1,094 words. Short orders (land withdrawals, individual civil-service waivers and the like) mostly score zero. Modern orders are rarely short.
- Splitting the 1930s→2020s change into parts, 78% comes from composition (fewer machinery-free orders) and 22% from heavier orders.

**Among orders that build something,** comparing like with like (orders over 842 words, the longest fifth):

- Weight was 10–24% from FDR through Carter.
- It stepped up to about 29–32% under Reagan and held there through Trump's first term.
- It rose to 34.6% under Biden and 44.3% under Trump's second term (95% CIs 32.4–36.7 and 41.7–46.9).

Two qualifications:

- The Reagan–Trump-first-term plateau is flatter with all 11 flags than with the 7 most reliable ones. With 7 flags it looks like a gradual rise.
- The Trump-second-term figure is driven by 2025 (37.7% mean across 237 orders). The partial 2026 figure is 29.5%.

The rise since 2021 isn't tied to one party.

**Not yet ruled out:**

- **Administration knowledge.** Stream B was coded one administration per batch, with the coder knowing the president. The masked re-coding test (`../robustness/masked-recode/`, H2) measures whether masking changes the recent gap.
- **Coder seam at 1953.** The zero-score share jumps from 38% (stream A, 1951–52) to 68% (stream B, 1953–54) exactly at the boundary between coding streams. Don't compare levels across 1953 until H4 of the masked test is in.

**Use `../robustness/annual-series-rebuilt.csv` for new work.** It swaps the label-aware codings of the 297 validation orders for their blind-v2 codings, and adds zero-share, mean-if-nonzero and long-order columns. `annual-structural-weight.csv`, listed above, is the original series, kept for the record.

## Known limitations worth carrying forward

- **Coding depth is consistent, but the two extension streams and the primary coding were produced independently over an extended period, not as one continuous pass.** Each stream's own notable-patterns logs document self-caught and corrected errors as they went — evidence of care, worth citing as such rather than treating as a weakness to hide.
- **No extension order has been coded twice.** The masked re-coding test re-codes 130 extension orders (and a human coder 50 of them), which will give the first reliability estimate for this corpus.
- **This is validated methodology applied at scale, not an independently re-validated result in its own right.** The Mayer & Price blind validation (AUC = 0.7836, see `../mayer-price-validation/`) is what demonstrates the methodology reproduces external judgment. This extension applies that already-validated instrument to the full corpus; it wasn't itself re-validated end to end against an external benchmark.
- **Annual aggregation is a simple mean/median of individual order scores** — not weighted by significance, word count, or order type. The per-order data supports recomputing this differently if a different weighting is wanted.

## Rolling up to Congress sessions or presidential terms

Every order in `../database/eo_coding.db` has a resolvable date, so regrouping to a presidential term or a Congress session is a straightforward re-aggregation of the same underlying data — not a separate coding effort. Ask for the specific grouping needed and it can be produced directly from the database rather than reconstructed from the annual figures.
