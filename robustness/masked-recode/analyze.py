#!/usr/bin/env python3
"""
analyze.py: computes every statistic named in ANALYSIS-PLAN.md, and nothing else.
Written and committed BEFORE any masked-test data exists.

Inputs:
  results/arm-M/<coder>.json      masked-arm records (item_id ...)
  results/arm-U/<coder>.json      unmasked-arm records (order_id ...), same coder name as its arm-M file
  human-coding/human-coding-sheet.csv   (optional; rows with all 11 statuses filled are used)
  _sealed/key.csv                  opened only here, by the script
Existing codings are read from ../../database/eo_coding.db
  (validation items -> cowork-blind-v2; extension items -> cowork-extension-stream-a/b).
Run:  python3 analyze.py [--boot 2000] [--results DIR] > results/REPORT.txt
"""
import argparse, csv, json, sqlite3, collections, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser(); ap.add_argument("--boot", type=int, default=2000); ap.add_argument("--results", default=str(HERE / "results"))
args = ap.parse_args(); RES = pathlib.Path(args.results)
rng = np.random.default_rng(20260918)
PTS = {"ABSENT": 0, "PRESENT": 1, "CRITICAL": 2}

key = list(csv.DictReader(open(HERE / "_sealed" / "key.csv")))
byM = {r["masked_item_id"]: r for r in key}; byU = {r["unmasked_order_id"]: r for r in key}
con = sqlite3.connect(f"file:{HERE.parent.parent / 'database' / 'eo_coding.db'}?mode=ro", uri=True)
def existing(eo, validation):
    cids = ("cowork-blind-v2",) if validation else ("cowork-extension-stream-a", "cowork-extension-stream-b")
    q = f"select coder_id from eo_scores where eo_number=? and coder_id in ({','.join('?'*len(cids))})"
    r = con.execute(q, (eo, *cids)).fetchone()
    if not r: return None
    s = con.execute("select structural_weight_pct from eo_scores where eo_number=? and coder_id=?", (eo, r[0])).fetchone()[0]
    fl = {f: st for f, st in con.execute("select flag_number,status from flag_codings where eo_number=? and coder_id=?", (eo, r[0]))}
    return dict(score=s, flags=fl)

def norm_status(s): return (s or "").strip().upper().replace(" ", "_").replace("N/A", "NOT_APPLICABLE")
def score_from_flags(fl):
    app = [PTS[s] for s in fl.values() if s in PTS]
    return None if not app else 100 * sum(app) / (2 * len(app))   # recomputed; never trust the coder's arithmetic

def load_arm(arm):
    out = {}
    for f in sorted((RES / f"arm-{arm}").glob("*.json")):
        recs = json.load(open(f)); d = {}
        for r in recs:
            rid = r.get("item_id") or r.get("order_id")
            k = (byM if arm == "M" else byU).get(rid)
            if not k: print(f"WARNING {f.name}: unknown id {rid}", file=sys.stderr); continue
            fl = {int(x["flag_number"]): norm_status(x["status"]) for x in r["flags"]}
            if len(fl) != 11: print(f"WARNING {f.name} {rid}: {len(fl)} flags", file=sys.stderr)
            ac = r.get("after_coding", {}) or {}
            d[k["eo_number"]] = dict(flags=fl, score=score_from_flags(fl), recognized=bool(ac.get("recognized_specific_order")),
                                     guess_decade=str(ac.get("guess_decade", "")), guess_president=str(ac.get("guess_president", "")))
        out[f.stem] = d
    return out
def load_human():
    p = HERE / "human-coding" / "human-coding-sheet.csv"; d = {}
    for r in csv.DictReader(open(p)):
        fl = {i: norm_status(r[f"f{i}_status"]) for i in range(1, 12)}
        if all(fl.values()):
            k = byM[r["item_id"]]
            d[k["eo_number"]] = dict(flags=fl, score=score_from_flags(fl), recognized=r["AFTER_CODING_recognized_order_Y_N"].strip().upper().startswith("Y"),
                                     guess_decade=r["AFTER_CODING_guess_decade"], guess_president=r["AFTER_CODING_guess_president"])
    return d

# ---------------------------------------------------------------- stats helpers
def auc(y, s):
    y = np.asarray(y); s = np.asarray(s, float); p, q = s[y == 1], s[y == 0]
    d = p[:, None] - q[None, :]; return float(((d > 0).sum() + 0.5 * (d == 0).sum()) / d.size)
def kappa(pairs):
    if not pairs: return None
    a, b = zip(*pairs); n = len(a); po = sum(x == y for x, y in pairs) / n
    ca, cb = collections.Counter(a), collections.Counter(b); pe = sum(ca[t] * cb[t] for t in ca) / n / n
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None
def icc21(a, b):
    M = np.column_stack([a, b]); n = len(a); gm = M.mean()
    msr = 2 * ((M.mean(1) - gm) ** 2).sum() / (n - 1); msc = n * ((M.mean(0) - gm) ** 2).sum()
    mse = ((M - M.mean(1, keepdims=True) - M.mean(0) + gm) ** 2).sum() / (n - 1)
    return round(float((msr - mse) / (msr + mse + 2 * (msc - mse) / n)), 3)
def agree(A, B, label):
    ks = [e for e in A if e in B and A[e]["score"] is not None and B[e]["score"] is not None]
    if len(ks) < 5: return f"  {label}: n={len(ks)} (too few)"
    a = np.array([A[e]["score"] for e in ks]); b = np.array([B[e]["score"] for e in ks])
    fk = kappa([(A[e]["flags"].get(f), B[e]["flags"].get(f)) for e in ks for f in range(1, 12)])
    return (f"  {label}: n={len(ks)}  flag kappa={fk}  ICC(2,1)={icc21(a, b)}  r={np.corrcoef(a, b)[0,1]:.3f}"
            f"  mean diff (A-B)={np.mean(a-b):+.1f} pts  mean |diff|={np.mean(abs(a-b)):.1f}")
def boot_mean_ci(v):
    v = np.asarray(v); bs = [rng.choice(v, len(v)).mean() for _ in range(args.boot)]
    return f"{v.mean():+.1f} [{np.percentile(bs, 2.5):+.1f}, {np.percentile(bs, 97.5):+.1f}]"

M, U = load_arm("M"), load_arm("U"); H = load_human() if (HERE / "human-coding" / "human-coding-sheet.csv").exists() else {}
EX = {r["eo_number"]: existing(r["eo_number"], r["stratum"].startswith("V")) for r in key}
EX = {e: v for e, v in EX.items() if v}
strat = {r["eo_number"]: r["stratum"] for r in key}; cls = {r["eo_number"]: r["validation_class"] for r in key}
year = {r["eo_number"]: int(r["date"][:4]) for r in key}
print("MASKED RE-CODING TEST: REPORT\n")
print(f"coders arm M: {list(M)}   arm U: {list(U)}   human items complete: {len(H)}\n")

for coder in sorted(set(M) & set(U)):
    m, u = M[coder], U[coder]
    print(f"=== coder: {coder}")
    # H1 recognition
    V = [e for e in m if e in u and strat[e].startswith("V") and m[e]["score"] is not None and u[e]["score"] is not None]
    y = np.array([cls[e] == "positive" for e in V], int)
    sm = np.array([m[e]["score"] for e in V]); su = np.array([u[e]["score"] for e in V])
    if len(V) >= 20 and 0 < y.sum() < len(y):
        d = []
        for _ in range(args.boot):
            i = np.concatenate([rng.choice(np.where(y == 1)[0], y.sum()), rng.choice(np.where(y == 0)[0], len(y) - y.sum())])
            d.append(auc(y[i], su[i]) - auc(y[i], sm[i]))
        lo, hi = np.percentile(d, [2.5, 97.5])
        print(f"H1  AUC unmasked={auc(y, su):.3f}  AUC masked={auc(y, sm):.3f}  diff(U-M)={auc(y, su)-auc(y, sm):+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]  n={len(V)}")
        print(f"    positives: mean(U-M)={boot_mean_ci(su[y==1]-sm[y==1])}   negatives: mean(U-M)={boot_mean_ci(su[y==0]-sm[y==0])}")
        nr = [i for i, e in enumerate(V) if not m[e]["recognized"]]
        if len(nr) >= 20 and 0 < y[nr].sum() < len(nr): print(f"    masked AUC on items the coder did NOT recognize: {auc(y[nr], sm[nr]):.3f} (n={len(nr)})")
        rec_u = [e for e in V if u[e]["recognized"]]
        print(f"    unmasked arm: coder says it recognized {len(rec_u)}/{len(V)} validation orders "
              f"({sum(cls[e]=='positive' for e in rec_u)} positives)")
    # H2 administration / era
    print("H2  mean(U - M) score by stratum (points, bootstrap 95% CI):")
    for s in sorted(set(strat.values())):
        es = [e for e in m if e in u and strat[e] == s and m[e]["score"] is not None and u[e]["score"] is not None]
        if len(es) >= 5: print(f"    {s:18s} n={len(es):3d}  {boot_mean_ci([u[e]['score']-m[e]['score'] for e in es])}")
    t2 = [e for e in m if e in u and strat[e] == "X6-Trump2"]; x5 = [e for e in m if e in u and strat[e] == "X5-2001-2020"]
    if len(t2) >= 5 and len(x5) >= 5:
        for lab, arm in (("unmasked", u), ("masked", m)):
            a = np.array([arm[e]["score"] for e in t2]); b = np.array([arm[e]["score"] for e in x5])
            bs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(args.boot)]
            print(f"    Trump-2nd-term minus 2001-2020 gap, {lab}: {a.mean()-b.mean():+.1f} pts "
                  f"[{np.percentile(bs, 2.5):+.1f}, {np.percentile(bs, 97.5):+.1f}]")
    # H3 reliability against existing codings
    print("H3  agreement with existing codings (A = this coder, B = existing):")
    for lab, arm in (("masked", m), ("unmasked", u)):
        for grp, pred in (("validation", lambda e: strat[e].startswith("V")), ("extension", lambda e: strat[e].startswith("X"))):
            print(agree({e: arm[e] for e in arm if pred(e)}, {e: EX[e] for e in EX if pred(e)}, f"{lab} vs existing, {grp}"))
    print(agree(m, u, "masked vs unmasked, same coder (all items)"))
    # H4 seam
    print("H4  stream seam 1951-54: mean(existing - this coder unmasked):")
    for s in ("X2-seam-streamA", "X2-seam-streamB"):
        es = [e for e in u if strat[e] == s and e in EX and u[e]["score"] is not None]
        if es: print(f"    {s}: n={len(es)}  {boot_mean_ci([EX[e]['score']-u[e]['score'] for e in es])}")
    # H5 masking check
    def dec_ok(e):
        g = "".join(ch for ch in m[e]["guess_decade"] if ch.isdigit())[:4]
        return len(g) == 4 and abs(int(g) - (year[e] // 10) * 10) <= 10
    print(f"H5  masked arm: recognized specific order {sum(v['recognized'] for v in m.values())}/{len(m)}; "
          f"decade guessed within +/-10y {sum(dec_ok(e) for e in m)}/{len(m)}")
    print()

# Coders pairwise (arm M), and human
names = sorted(M)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        print(agree(M[names[i]], M[names[j]], f"arm M: {names[i]} vs {names[j]}"))
if H:
    print("\n=== HUMAN (masked items)")
    print(agree(H, {e: EX[e] for e in EX}, "human vs existing codings (all)"))
    print(agree(H, {e: EX[e] for e in EX if strat[e].startswith('X')}, "human vs existing, extension only"))
    for c in names: print(agree(H, M[c], f"human vs {c} masked"))
    Hv = [e for e in H if strat[e].startswith("V") and H[e]["score"] is not None]
    yh = np.array([cls[e] == "positive" for e in Hv], int)
    if len(Hv) >= 20 and 0 < yh.sum() < len(yh): print(f"  human AUC on validation items: {auc(yh, [H[e]['score'] for e in Hv]):.3f} (n={len(Hv)})")
    print(f"  human recognized {sum(v['recognized'] for v in H.values())}/{len(H)} items")
