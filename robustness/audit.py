#!/usr/bin/env python3
"""
robustness/audit.py — reproducible robustness audit of the EO Structural Weight results.

Reads only: ../database/eo_coding.db, ../mayer-price-validation/validation-key.csv
Writes:     audit-output.json (all numbers), printed summary to stdout.
Run:        python3 robustness/audit.py        (numpy only; no scipy/sklearn needed)

Every number quoted in robustness/AUDIT.md comes from this script.
"""
import csv, json, sqlite3, collections, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "database" / "eo_coding.db"
KEY = ROOT / "mayer-price-validation" / "validation-key.csv"
OUT = pathlib.Path(__file__).resolve().parent / "audit-output.json"
SEED = 20260918
N_BOOT = 2000

PRIMARY, BV1, BV2 = "claude-church-bells-v1", "cowork-blind-v1", "cowork-blind-v2"
EXT = ("cowork-extension-stream-a", "cowork-extension-stream-b")

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
meta = {e: dict(date=d, pres=p, words=None, title=t) for e, d, p, t in
        con.execute("select eo_number,date_iso,president,title from eos")}
# eos.word_count is NULL for every row, so word counts are computed from the corpus text files.
for f in (ROOT / "database" / "corpus-texts").glob("EO-*.json"):
    d = json.load(open(f))
    if d.get("eo_number") in meta:
        meta[d["eo_number"]]["words"] = len((d.get("text") or "").split())
def clean_pres(p):
    return "Donald J. Trump (2nd Term)" if p.startswith("Donald J. Trump (2nd Term)") else p

def scores(cid):
    return {e: s for e, s in con.execute(
        "select eo_number, structural_weight_pct from eo_scores where coder_id=?", (cid,)) if s is not None}
def flags(cid):
    return {(e, f): s for e, f, s in con.execute(
        "select eo_number, flag_number, status from flag_codings where coder_id=?", (cid,))}

key = {r["eo_number"]: 1 if r["validation_class"] == "positive" else 0 for r in csv.DictReader(open(KEY))}
out = {}

# ---------------------------------------------------------------- AUC helpers
def auc(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    order = s.argsort(kind="mergesort"); ranks = np.empty(len(s))
    ss = s[order]; i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]: j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1; i = j + 1
    n1 = y.sum(); n0 = len(y) - n1
    return (ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def boot_ci(y, s, rng, n=N_BOOT):
    y, s = np.asarray(y), np.asarray(s, float)
    pos, neg = np.where(y == 1)[0], np.where(y == 0)[0]
    vals = []
    for _ in range(n):
        idx = np.concatenate([rng.choice(pos, len(pos)), rng.choice(neg, len(neg))])
        vals.append(auc(y[idx], s[idx]))
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]

def stratified_auc(y, s, strata):
    """AUC counting only positive/negative pairs within the same stratum (pooled)."""
    y, s, strata = map(np.asarray, (y, s, strata))
    num = den = 0.0
    for g in set(strata):
        m = strata == g; p = s[m & (y == 1)]; q = s[m & (y == 0)]
        if len(p) and len(q):
            d = p[:, None] - q[None, :]
            num += (d > 0).sum() + 0.5 * (d == 0).sum(); den += d.size
    return num / den, int(den)

def logit_fit(X, y, iters=50):
    X = np.column_stack([np.ones(len(y)), X]); b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b)); W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-9 * np.eye(X.shape[1])
        b += np.linalg.solve(H, X.T @ (y - p))
    p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    return b, float((y * np.log(p) + (1 - y) * np.log(1 - p)).sum()), p

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- 1. AUC per coding, with CIs
out["auc"] = {}
for cid in (PRIMARY, BV1, BV2):
    sc = scores(cid); ks = [e for e in key if e in sc]
    y = [key[e] for e in ks]; s = [sc[e] for e in ks]
    out["auc"][cid] = dict(n=len(ks), auc=round(auc(y, s), 4), ci95=boot_ci(y, s, rng),
                           label_aware=(cid == PRIMARY))

# ---------------------------------------------------------------- 2. Confounds: era and length
sc = scores(BV2); ks = [e for e in key if e in sc]
y = np.array([key[e] for e in ks]); s = np.array([sc[e] for e in ks])
year = np.array([int(meta[e]["date"][:4]) for e in ks])
words = np.array([meta[e]["words"] or 0 for e in ks], float)
dec = (year // 10) * 10
era3 = np.where(year < 1953, "1936-52", np.where(year < 1977, "1953-76", "1977-99"))
conf = {}
conf["auc_year_alone"] = round(auc(y, year), 4)
conf["auc_wordcount_alone"] = round(auc(y, words), 4)
conf["auc_score_within_decade"] = round(stratified_auc(y, s, dec)[0], 4)
conf["auc_score_within_era3"] = round(stratified_auc(y, s, era3)[0], 4)
wt = np.digitize(np.log1p(words), np.quantile(np.log1p(words), [1/3, 2/3]))
conf["auc_score_within_length_tercile"] = round(stratified_auc(y, s, wt)[0], 4)
conf["auc_score_within_length_tercile_x_era3"] = round(stratified_auc(y, s, [f"{a}|{b}" for a, b in zip(wt, era3)])[0], 4)
# Nested logits: does score add information beyond year + log length?
Xb = np.column_stack([(year - 1970) / 20, np.log1p(words)])
_, ll0, p0 = logit_fit(Xb, y)
_, ll1, p1 = logit_fit(np.column_stack([Xb, s / 10]), y)
conf["logit_baseline_year_loglength"] = dict(loglik=round(ll0, 2), auc=round(auc(y, p0), 4))
conf["logit_plus_score"] = dict(loglik=round(ll1, 2), auc=round(auc(y, p1), 4),
                                LR_chi2_1df=round(2 * (ll1 - ll0), 2))
conf["decade_counts"] = {int(d): dict(pos=int(((dec == d) & (y == 1)).sum()), neg=int(((dec == d) & (y == 0)).sum()))
                         for d in sorted(set(dec))}
out["confounds_blind_v2"] = conf

# ---------------------------------------------------------------- 3. Divergence examples: robust across all three codings
P, A, B = scores(PRIMARY), scores(BV1), scores(BV2)
common = [e for e in key if e in P and e in A and e in B]
def row(e): return dict(eo=e, year=meta[e]["date"][:4], title=meta[e]["title"], primary=P[e], blind_v1=A[e], blind_v2=B[e])
clean_pos = sorted([row(e) for e in common if key[e] == 1 and max(P[e], A[e], B[e]) <= 10], key=lambda r: max(r["primary"], r["blind_v1"], r["blind_v2"]))
heavy_neg = sorted([row(e) for e in common if key[e] == 0 and min(P[e], A[e], B[e]) >= 25], key=lambda r: -min(r["primary"], r["blind_v1"], r["blind_v2"]))
heavy_pos = sorted([row(e) for e in common if key[e] == 1 and min(P[e], A[e], B[e]) >= 30], key=lambda r: -min(r["primary"], r["blind_v1"], r["blind_v2"]))
unstable = sorted([row(e) for e in common if max(P[e], A[e], B[e]) - min(P[e], A[e], B[e]) >= 20], key=lambda r: -(max(r["primary"], r["blind_v1"], r["blind_v2"]) - min(r["primary"], r["blind_v1"], r["blind_v2"])))
cited = ["11375", "12139", "12958", "11785", "13010", "9250", "9001", "8565", "12318", "11615", "9808", "11940"]
out["divergence"] = dict(
    cited_in_old_comparison_doc=[row(e) for e in cited if e in common],
    positives_clean_in_all_three=clean_pos, negatives_heavy_in_all_three=heavy_neg,
    positives_heavy_in_all_three=heavy_pos, orders_with_20pt_spread=unstable,
    n_orders_with_20pt_spread=len(unstable), n_common=len(common))

# Label-aware coding bias: original minus blind, by class
lab_bias = {}
for cls_name, cv in (("positive", 1), ("negative", 0)):
    ks_ = [e for e in common if key[e] == cv]
    lab_bias[cls_name] = dict(n=len(ks_), mean_original=round(float(np.mean([P[e] for e in ks_])), 1),
                              mean_blind_v1=round(float(np.mean([A[e] for e in ks_])), 1), mean_blind_v2=round(float(np.mean([B[e] for e in ks_])), 1),
                              original_minus_blind_v2=round(float(np.mean([P[e] - B[e] for e in ks_])), 1),
                              original_minus_blind_v1=round(float(np.mean([P[e] - A[e] for e in ks_])), 1),
                              share_le10_original=round(float(np.mean([P[e] <= 10 for e in ks_])), 3),
                              share_le10_all_three=round(float(np.mean([max(P[e], A[e], B[e]) <= 10 for e in ks_])), 3))
out["divergence"]["label_aware_bias_by_class"] = lab_bias
# ---------------------------------------------------------------- 4. Reliability
def kappa(x, y_):
    k = [q for q in x if q in y_]; n = len(k)
    po = sum(x[q] == y_[q] for q in k) / n
    cx = collections.Counter(x[q] for q in k); cy = collections.Counter(y_[q] for q in k)
    pe = sum(cx[t] * cy[t] for t in cx) / n / n
    return dict(n_flag_judgments=n, pct_agree=round(po, 3), kappa=round((po - pe) / (1 - pe), 3))
def per_flag_kappa(x, y_):
    return {f: kappa({k: v for k, v in x.items() if k[1] == f}, {k: v for k, v in y_.items() if k[1] == f})["kappa"] for f in range(1, 12)}
def score_rel(x, y_):
    k = [e for e in x if e in y_]; a = np.array([x[e] for e in k]); b = np.array([y_[e] for e in k])
    rk = lambda v: np.argsort(np.argsort(v))
    # ICC(2,1) absolute agreement
    M = np.column_stack([a, b]); n = len(k); gm = M.mean()
    msr = 2 * ((M.mean(1) - gm) ** 2).sum() / (n - 1); msc = n * ((M.mean(0) - gm) ** 2).sum()
    mse = ((M - M.mean(1, keepdims=True) - M.mean(0) + gm) ** 2).sum() / (n - 1)
    icc = (msr - mse) / (msr + mse + 2 * (msc - mse) / n)
    return dict(n=n, pearson=round(float(np.corrcoef(a, b)[0, 1]), 3), spearman=round(float(np.corrcoef(rk(a), rk(b))[0, 1]), 3),
                icc_2_1=round(float(icc), 3), mean_abs_diff_pts=round(float(np.abs(a - b).mean()), 2),
                share_diff_ge_10pts=round(float((np.abs(a - b) >= 10).mean()), 3),
                binary_agree_at_35pct=round(float(((a >= 35) == (b >= 35)).mean()), 3))
FP, F1, F2 = flags(PRIMARY), flags(BV1), flags(BV2)
out["reliability"] = {
    "primary_vs_blind_v2": dict(flags=kappa(FP, F2), per_flag_kappa=per_flag_kappa(FP, F2), scores=score_rel(P, B)),
    "primary_vs_blind_v1": dict(flags=kappa(FP, F1), scores=score_rel(P, A)),
    "blind_v1_vs_blind_v2": dict(flags=kappa(F1, F2), per_flag_kappa=per_flag_kappa(F1, F2), scores=score_rel(A, B)),
}
pilot = {}
for cid in ("gemini-2.5-collaborator", "gemini-2.5-flash", "gpt-5.5-thinking-v1", "gpt-5.5-thinking-v2"):
    pilot[cid] = dict(vs_primary_flags=kappa(FP, flags(cid)), vs_primary_scores=score_rel(P, scores(cid)))
out["reliability"]["icr_pilot_30"] = pilot
ext_ids = set(scores(EXT[0])) | set(scores(EXT[1]))
out["reliability"]["extension_orders_coded_more_than_once"] = sum(
    1 for e in ext_ids if con.execute("select count(*) from eo_scores where eo_number=?", (e,)).fetchone()[0] > 1)
out["reliability"]["extension_orders_total"] = len(ext_ids)
out["reliability"]["human_codings"] = con.execute("select count(*) from eo_scores where coder_id like 'human%'").fetchone()[0]

# ---------------------------------------------------------------- 5. Trend: composition vs within-order weight
ext = {}
for cid in EXT: ext.update(scores(cid))
nacount = {e: n for e, n in con.execute(
    "select eo_number, na_count from eo_scores where coder_id in (?,?)", EXT)}
def summarize(vals):
    v = np.array(vals); nz = v[v > 0]
    return dict(n=len(v), mean=round(float(v.mean()), 1), median=round(float(np.median(v)), 1),
                share_zero=round(float((v == 0).mean()), 3),
                mean_if_nonzero=round(float(nz.mean()), 1) if len(nz) else None,
                median_if_nonzero=round(float(np.median(nz)), 1) if len(nz) else None)
by_pres = collections.OrderedDict(); by_dec = collections.defaultdict(list); first = {}
for e, s_ in ext.items():
    p = clean_pres(meta[e]["pres"]); by_pres.setdefault(p, []).append(s_)
    first[p] = min(first.get(p, "9"), meta[e]["date"]); by_dec[int(meta[e]["date"][:3]) * 10].append(s_)
out["trend"] = dict(
    coder_ids=list(EXT),
    by_president={p: summarize(by_pres[p]) for p in sorted(by_pres, key=first.get)},
    by_decade={d: summarize(by_dec[d]) for d in sorted(by_dec)})
# bootstrap CI on mean-if-nonzero per president
cis = {}
for p, v in by_pres.items():
    nz = np.array([x for x in v if x > 0])
    if len(nz) > 5:
        bs = [rng.choice(nz, len(nz)).mean() for _ in range(N_BOOT)]
        cis[p] = [round(float(np.percentile(bs, 2.5)), 1), round(float(np.percentile(bs, 97.5)), 1)]
out["trend"]["mean_if_nonzero_ci95_by_president"] = cis
# Shift-share decomposition of change in mean between two periods:
#   mean = s * m  (s = share nonzero, m = mean if nonzero)
#   Δmean = Δs * m̄  (composition)  +  s̄ * Δm  (within)
def decompose(v0, v1):
    v0, v1 = np.array(v0), np.array(v1)
    s0, s1 = (v0 > 0).mean(), (v1 > 0).mean(); m0, m1 = v0[v0 > 0].mean(), v1[v1 > 0].mean()
    comp = (s1 - s0) * (m0 + m1) / 2; within = (s1 + s0) / 2 * (m1 - m0)
    return dict(mean_from=round(float(v0.mean()), 1), mean_to=round(float(v1.mean()), 1), change=round(float(v1.mean() - v0.mean()), 1),
                composition_part=round(float(comp), 1), within_part=round(float(within), 1),
                composition_share=round(float(comp / (comp + within)), 2))
out["trend"]["decomposition"] = {
    "1930s_to_2020s": decompose(by_dec[1930], by_dec[2020]),
    "1950s_to_2010s": decompose(by_dec[1950], by_dec[2010]),
    "Reagan_to_Trump1": decompose(by_pres["Ronald Reagan"], by_pres["Donald J. Trump (1st Term)"]),
    "Trump1_to_Trump2": decompose(by_pres["Donald J. Trump (1st Term)"], by_pres["Donald J. Trump (2nd Term)"]),
}
# Denominator check: how many flags are scoreable (not NA), by decade
na_dec = collections.defaultdict(list)
for e in ext:
    if e in nacount and nacount[e] is not None: na_dec[int(meta[e]["date"][:3]) * 10].append(nacount[e])
out["trend"]["mean_na_flags_by_decade"] = {d: round(float(np.mean(v)), 2) for d, v in sorted(na_dec.items())}
# Seam between extension streams (A ends 1953-01-19, B starts 1953-01-24)
a_last = [s_ for e, s_ in scores(EXT[0]).items() if meta[e]["date"] >= "1951"]
b_first = [s_ for e, s_ in scores(EXT[1]).items() if meta[e]["date"] < "1955"]
out["trend"]["stream_seam"] = dict(streamA_1951_52=summarize(a_last), streamB_1953_54=summarize(b_first))
# Word count as a composition driver
wc_dec = collections.defaultdict(list)
for e in ext: wc_dec[int(meta[e]["date"][:3]) * 10].append(meta[e]["words"] or 0)
out["trend"]["median_words_by_decade"] = {d: int(np.median(v)) for d, v in sorted(wc_dec.items())}
# Within-length-band trend: mean if nonzero by decade, orders >= 500 words only
long_dec = collections.defaultdict(list)
for e, s_ in ext.items():
    if (meta[e]["words"] or 0) >= 500: long_dec[int(meta[e]["date"][:3]) * 10].append(s_)
out["trend"]["orders_500plus_words_by_decade"] = {d: summarize(v) for d, v in sorted(long_dec.items())}
# Length standardization: direct standardization of each president's mean score to the
# pooled word-count distribution (quintile bins of the full extension corpus).
ext_e = [e for e in ext if meta[e]["words"]]
cuts = np.quantile([meta[e]["words"] for e in ext_e], [.2, .4, .6, .8])
binof = lambda e: int(np.digitize(meta[e]["words"], cuts))
pooled_w = collections.Counter(binof(e) for e in ext_e); tot = sum(pooled_w.values())
out["trend"]["word_quintile_cuts"] = [int(c) for c in cuts]
zero_by_bin = collections.defaultdict(list)
for e in ext_e: zero_by_bin[binof(e)].append(ext[e] == 0)
out["trend"]["share_zero_by_word_quintile"] = {b: round(float(np.mean(v)), 3) for b, v in sorted(zero_by_bin.items())}
std = {}
for p in sorted(by_pres, key=first.get):
    cells = collections.defaultdict(list)
    for e in ext_e:
        if clean_pres(meta[e]["pres"]) == p: cells[binof(e)].append(ext[e])
    if all(len(cells[b]) >= 3 for b in range(5)):
        std[p] = round(float(sum(np.mean(cells[b]) * pooled_w[b] / tot for b in range(5))), 1)
    else:
        std[p] = None  # too few orders in some length band to standardize
out["trend"]["length_standardized_mean_by_president"] = std
out["trend"]["length_band_cell_counts"] = {p: [sum(1 for e in ext_e if clean_pres(meta[e]["pres"]) == p and binof(e) == b) for b in range(5)] for p in by_pres}
# Like-for-like comparison: only long orders (top word-count quintile), which every president issues.
lf = {}
for p in sorted(by_pres, key=first.get):
    v = np.array([ext[e] for e in ext_e if clean_pres(meta[e]["pres"]) == p and binof(e) == 4])
    if len(v) >= 10:
        bs = [rng.choice(v, len(v)).mean() for _ in range(N_BOOT)]
        lf[p] = dict(n=len(v), mean=round(float(v.mean()), 1), share_zero=round(float((v == 0).mean()), 3),
                     ci95=[round(float(np.percentile(bs, 2.5)), 1), round(float(np.percentile(bs, 97.5)), 1)])
out["trend"]["top_length_quintile_by_president"] = lf
# ---------------------------------------------------------------- 6. Seven-flag sensitivity (drop the least reliable flags 3, 9, 10, 11)
DROP = {3, 9, 10, 11}
def score_subset(cid):
    acc = collections.defaultdict(list)
    for e, f, st in con.execute("select eo_number, flag_number, status from flag_codings where coder_id=?", (cid,)):
        if f not in DROP and st in ("ABSENT", "PRESENT", "CRITICAL"): acc[e].append({"ABSENT": 0, "PRESENT": 1, "CRITICAL": 2}[st])
    return {e: 100 * sum(v) / (2 * len(v)) for e, v in acc.items() if v}
sev = {}
for cid in (PRIMARY, BV1, BV2):
    sc7 = score_subset(cid); ks = [e for e in key if e in sc7]
    sev[cid] = dict(n=len(ks), auc_7flag=round(auc([key[e] for e in ks], [sc7[e] for e in ks]), 4))
ext7 = {}
for cid in EXT: ext7.update(score_subset(cid))
lf7 = {}
for p in sorted(by_pres, key=first.get):
    v = [ext7[e] for e in ext_e if e in ext7 and clean_pres(meta[e]["pres"]) == p and binof(e) == 4]
    nzall = [ext7[e] for e in ext7 if clean_pres(meta[e]["pres"]) == p]
    lf7[p] = dict(top_quintile_mean=round(float(np.mean(v)), 1) if v else None,
                  mean_if_nonzero=round(float(np.mean([x for x in nzall if x > 0])), 1) if any(x > 0 for x in nzall) else None)
out["seven_flag_sensitivity"] = dict(dropped_flags=sorted(DROP), auc=sev, trend_by_president=lf7)
# ---------------------------------------------------------------- 7. Rebuilt annual series (extension codings + blind-v2 for validation orders)
annual = collections.defaultdict(list)
series = dict(ext); series.update({e: v for e, v in scores(BV2).items()})
for e, v in series.items():
    annual[int(meta[e]["date"][:4])].append((v, meta[e]["words"] or 0))
with open(pathlib.Path(__file__).resolve().parent / "annual-series-rebuilt.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["year", "n_orders", "mean", "median", "share_zero", "mean_if_nonzero", "n_long_orders_gt842w", "mean_long_orders"])
    for y_ in sorted(annual):
        v = np.array([a for a, _ in annual[y_]]); lg = np.array([a for a, wds in annual[y_] if wds > cuts[3]])
        w.writerow([y_, len(v), round(v.mean(), 2), round(float(np.median(v)), 2), round(float((v == 0).mean()), 3),
                    round(float(v[v > 0].mean()), 2) if (v > 0).any() else "", len(lg), round(float(lg.mean()), 2) if len(lg) else ""])
out["annual_series_note"] = "annual-series-rebuilt.csv: extension codings plus blind-v2 for the 297 validation orders; label-aware original coding excluded"
# Metadata glitches
out["data_quality"] = dict(
    garbled_president_fields=[(e, m["pres"][:60]) for e, m in meta.items() if "47th President" in (m["pres"] or "")])

json.dump(out, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ("auc", "confounds_blind_v2")}, indent=1))
print(json.dumps(out["reliability"]["primary_vs_blind_v2"]["scores"]), json.dumps(out["reliability"]["blind_v1_vs_blind_v2"]["scores"]))
print(json.dumps(out["trend"]["decomposition"], indent=1))
print("20pt-spread orders:", out["divergence"]["n_orders_with_20pt_spread"], "of", out["divergence"]["n_common"])
