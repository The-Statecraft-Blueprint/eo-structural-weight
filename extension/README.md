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

Mean structural weight rises from roughly 1–3% in the late 1930s to the 22–38% range by the 2020s. The rise isn't smooth — real year-to-year noise is visible in the unsmoothed mean line — but the multi-decade direction is unambiguous. **2025 is a genuine standout** (37.93% mean, 38.89% median, 238 orders — a real sample, not noise). **2026 is a partial year** (43 orders as of this data pull) and shouldn't be read as a completed data point.

## Known limitations worth carrying forward

- **Coding depth is consistent, but the two extension streams and the primary coding were produced independently over an extended period, not as one continuous pass.** Each stream's own notable-patterns logs document self-caught and corrected errors as they went — evidence of care, worth citing as such rather than treating as a weakness to hide.
- **This is validated methodology applied at scale, not an independently re-validated result in its own right.** The Mayer & Price blind validation (AUC = 0.7836, see `../mayer-price-validation/`) is what demonstrates the methodology reproduces external judgment. This extension applies that already-validated instrument to the full corpus; it wasn't itself re-validated end to end against an external benchmark.
- **Annual aggregation is a simple mean/median of individual order scores** — not weighted by significance, word count, or order type. The per-order data supports recomputing this differently if a different weighting is wanted.

## Rolling up to Congress sessions or presidential terms

Every order in `../database/eo_coding.db` has a resolvable date, so regrouping to a presidential term or a Congress session is a straightforward re-aggregation of the same underlying data — not a separate coding effort. Ask for the specific grouping needed and it can be produced directly from the database rather than reconstructed from the annual figures.
