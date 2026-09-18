#!/usr/bin/env python3
"""
Builds the masked re-coding test and human hand-coding packet.

Two arms over the SAME 210 orders, differing only in what the coder can see:
  Arm M (masked):   EO number, title, date, president, signature block, filing notes,
                    years, dates, cross-referenced EO/proclamation numbers, Public Law,
                    Statutes-at-Large, Federal Register and Congress citations redacted.
  Arm U (unmasked): number + title header and full original text (as in the blind run).
Neither arm gets referenced-predecessor texts, so predecessor access is held constant.

Sample (seed 20260918), drawn only from orders with text and an existing score:
  V  = 80 validation orders (40 Mayer & Price positives, 40 negatives) from the blind-v2 set
  X1 = 20 extension orders 1936-1950 (stream A)
  X2 = 20 extension orders 1951-1954 (10 stream A, 10 stream B): the coder-stream seam
  X3 = 20 extension orders 1955-1980
  X4 = 20 extension orders 1981-2000
  X5 = 20 extension orders 2001-2020
  X6 = 30 extension orders 2021-2026 (15 Biden, 15 Trump 2nd term)
Human subset: 80 of the 210 (30 from V, 50 from X; recent administrations oversampled).

Outputs (relative to this folder):
  coder-packet-masked/items/item-NNN.md       -> give to masked-arm coders
  coder-packet-unmasked/items/order-NNN.md    -> give to unmasked-arm coders
  human-coding/human-coding-sheet.csv         -> the hand-coder's sheet (masked item IDs)
  _sealed/key.csv, _sealed/redaction-log.csv  -> NEVER give to any coder; do not open until coding is done
"""
import csv, json, random, re, sqlite3, shutil, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DB = ROOT / "database" / "eo_coding.db"
TEXTS = ROOT / "database" / "corpus-texts"
KEYCSV = ROOT / "mayer-price-validation" / "validation-key.csv"
BLIND = ROOT / "mayer-price-validation" / "blind-coding-package"
SEED = 20260918
rng = random.Random(SEED)

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
meta = {e: dict(date=d, pres=p, title=t) for e, d, p, t in con.execute("select eo_number,date_iso,president,title from eos")}
def coded(cid): return {e for (e,) in con.execute("select eo_number from eo_scores where coder_id=? and structural_weight_pct is not null", (cid,))}
def text_of(e):
    f = TEXTS / f"EO-{e}.json"
    if not f.exists(): return None
    t = json.load(open(f)).get("text") or ""
    return t if len(t.split()) >= 15 else None

# ------------------------------------------------------------------ sampling
vkey = {r["eo_number"]: r["validation_class"] for r in csv.DictReader(open(KEYCSV))}
bv2 = coded("cowork-blind-v2")
V_pos = sorted(e for e in bv2 if vkey.get(e) == "positive" and text_of(e))
V_neg = sorted(e for e in bv2 if vkey.get(e) == "negative" and text_of(e))
sA, sB = coded("cowork-extension-stream-a"), coded("cowork-extension-stream-b")
def pool(stream, lo, hi, pres=None):
    return sorted(e for e in stream if lo <= meta[e]["date"] <= hi and text_of(e)
                  and (pres is None or meta[e]["pres"].startswith(pres)))
strata = collections.OrderedDict()
strata["V-pos"] = rng.sample(V_pos, 40)
strata["V-neg"] = rng.sample(V_neg, 40)
strata["X1-1936-1950"] = rng.sample(pool(sA, "1936", "1950-12-31"), 20)
strata["X2-seam-streamA"] = rng.sample(pool(sA, "1951", "1954-12-31"), 10)
strata["X2-seam-streamB"] = rng.sample(pool(sB, "1951", "1954-12-31"), 10)
strata["X3-1955-1980"] = rng.sample(pool(sB, "1955", "1980-12-31"), 20)
strata["X4-1981-2000"] = rng.sample(pool(sB, "1981", "2000-12-31"), 20)
strata["X5-2001-2020"] = rng.sample(pool(sB, "2001", "2020-12-31"), 20)
strata["X6-Biden"] = rng.sample(pool(sB, "2021", "2026-12-31", "Joseph R. Biden"), 15)
strata["X6-Trump2"] = rng.sample(pool(sB, "2021", "2026-12-31", "Donald J. Trump (2nd Term)"), 15)
sample = [(e, s) for s, es in strata.items() for e in es]
assert len({e for e, _ in sample}) == 210

HUMAN_K = {"V-pos": 15, "V-neg": 15, "X1-1936-1950": 6, "X2-seam-streamA": 4, "X2-seam-streamB": 4,
           "X3-1955-1980": 6, "X4-1981-2000": 6, "X5-2001-2020": 6, "X6-Biden": 9, "X6-Trump2": 9}
human = set()
for s, es in strata.items():
    human |= set(rng.sample(es, HUMAN_K[s]))
assert len(human) == 80, len(human)

# ------------------------------------------------------------------ redaction
MONTHS = r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept?\.|Oct\.|Nov\.|Dec\.)"
SURN = r"(?:Roosevelt|Truman|Eisenhower|Kennedy|Johnson|Nixon|Ford|Carter|Reagan|Bush|Clinton|Obama|Trump|Biden)"
FIRST = r"(?:Franklin|Harry|Dwight|John|Lyndon|Richard|Gerald|Jimmy|James|Ronald|George|William|Bill|Barack|Donald|Joseph|Joe)"
def redact(text, log):
    counts = collections.Counter()
    def sub(pat, rep, s, flags=0, tag=None):
        new, n = re.subn(pat, rep, s, flags=flags); counts[tag or rep] += n; return new
    lines = text.split("\n")
    # strip trailing signature / date / filing / note lines
    tail_pat = re.compile(r"^\s*(\[?Filed with|NOTE:|Note:|THE WHITE HOUSE|The White House|" + MONTHS + r"\s+\d|" + FIRST + r"\b.*" + SURN + r"|[A-Z][A-Z .]+" + SURN.upper() + r")", re.I)
    while lines and (not lines[-1].strip() or tail_pat.match(lines[-1]) or re.fullmatch(r"[A-Z .,]{4,40}", lines[-1].strip())):
        counts["[signature/date/filing line removed]"] += 1; lines.pop()
    s = "\n".join(lines)
    s = sub(r"^\s*Executive Order[^\n]*—[^\n]*\n", "", s, flags=re.M, tag="[header removed]")
    # cross-referenced EO / proclamation numbers -> stable per-item placeholders
    eomap, prmap = {}, {}
    def ph(m, table, prefix):
        return re.sub(r"\d{3,5}(?:-[A-Z])?", lambda n: table.setdefault(n.group(0), f"[{prefix}-{chr(65 + len(table) % 26)}{'' if len(table) < 26 else len(table)//26}]"), m.group(0))
    s, n1 = re.subn(r"(?:Executive\s+Orders?|E\.\s?O\.|Ex\.\s?Ord\.|Orders?)(?:\s+(?:Nos?\.|Numbers?|numbered))?((?:\s*(?:,|and|or|Nos?\.|through)?\s*\d{3,5}(?:-[A-Z])?)+)",
                    lambda m: ph(m, eomap, "EO"), s); counts["[EO-x]"] += n1
    s, n2 = re.subn(r"Proclamations?(?:\s+(?:Nos?\.|numbered))?((?:\s*(?:,|and|or|Nos?\.)?\s*\d{3,5})+)",
                    lambda m: ph(m, prmap, "PROC"), s); counts["[PROC-x]"] += n2
    # second pass: any remaining EO-range number (5000-14999) within 250 chars after an order reference,
    # or directly after "No."/"Nos."; statute/code section numbers are left alone.
    def window_pass(s):
        out, last = [], 0
        spans = [m.start() for m in re.finditer(r"Executive\s+Orders?|E\.\s?O\.|\bOrders?\b", s)]
        hit = [False] * (len(s) + 1)
        for a in spans:
            for i in range(a, min(len(s), a + 250)): hit[i] = True
        def rep(m):
            n = int(m.group(0)); pre = s[max(0, m.start() - 12):m.start()]
            if not (5000 <= n <= 14999) or re.search(r"(U\.S\.C\.|section|Sec\.|§|title|Stat\.|Rule|R\.C\.M\.)\s*$", pre, re.I): return m.group(0)
            if hit[m.start()] or re.search(r"Nos?\.\s*$", pre):
                counts["[EO-x]"] += 1
                return eomap.setdefault(m.group(0), f"[EO-{chr(65 + len(eomap) % 26)}{'' if len(eomap) < 26 else len(eomap)//26}]")
            return m.group(0)
        return re.sub(r"(?<![\d.,$-])\b\d{4,5}\b(?![\d-])", rep, s)
    s = window_pass(s)
    s = sub(r"\b(?:Public|Private)\s+Law\s+(?:No\.\s*)?\d{1,3}\s*[-–]\s*\d{1,4}", "Public Law [PL]", s)
    s = sub(r"\b(?:Pub|Priv)\.\s?L\.\s*(?:No\.\s*)?\d{1,3}\s*[-–]\s*\d{1,4}", "Pub. L. [PL]", s)
    s = sub(r"\bP\.\s?L\.\s*\d{1,3}\s*[-–]\s*\d{1,4}", "P.L. [PL]", s)
    s = sub(r"\b\d{1,3}\s+Stat\.\s*\d+(?:\s*[-–]\s*\d+)?", "[STAT]", s)
    s = sub(r"\b\d{1,2}\s+(?:F\.\s?R\.|FR|Fed\.\s?Reg\.)\s*\d+", "[FR]", s)
    s = sub(r"\b(?:[A-Z][a-z]+-)?[A-Za-z]+(?:st|nd|rd|th)\s+Congress\b", "[CONGRESS]", s)
    s = sub(r"\b" + MONTHS + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}", "[DATE]", s)
    s = sub(r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?" + MONTHS + r",?\s+\d{4}", "[DATE]", s)
    s = sub(r"\b" + MONTHS + r",?\s+\d{4}", "[DATE]", s)
    s = sub(r"\b" + MONTHS + r"\s+\d{1,2}(?:st|nd|rd|th)?\b", "[DATE]", s)
    s = sub(r"(?<![\$\d,.])\b(?:17[89]\d|18\d\d|19\d\d|20[0-3]\d)\b(?![,.]?\d)", "[YEAR]", s)
    s = sub(r"\[YEAR\]\s*[-–/]\s*\d{2,4}\b", "[YEAR]", s, tag="[YEAR-range]")
    s = sub(r"(?:President\s+)?\b" + FIRST + r"\.?\s+(?:[A-Z]\.\s+)?(?:Delano\s+|Baines\s+|Milhous\s+|Walker\s+|Jefferson\s+|Hussein\s+|R\.\s+)?" + SURN + r"(?:,?\s+Jr\.)?", "[PRESIDENT]", s, flags=0)
    s = sub(r"\bPresident\s+" + SURN + r"\b", "President [PRESIDENT]", s)
    log.update(counts)
    return s.strip()

# ------------------------------------------------------------------ write packets
for d in ("coder-packet-masked/items", "coder-packet-unmasked/items", "human-coding", "_sealed"):
    (HERE / d).mkdir(parents=True, exist_ok=True)  # files are overwritten in place; the sample is deterministic
for arm in ("coder-packet-masked", "coder-packet-unmasked"):
    for f in ("scoring-instructions.md", "flags-canonical.md"):
        shutil.copy(BLIND / f, HERE / arm / f)

order_M = [e for e, _ in sample]; rng.shuffle(order_M)
order_U = [e for e, _ in sample]; rng.shuffle(order_U)
idM = {e: f"item-{i+1:03d}" for i, e in enumerate(order_M)}
idU = {e: f"order-{i+1:03d}" for i, e in enumerate(order_U)}
stratum = dict(sample)
rlog = []
for e in order_M:
    t = text_of(e); c = collections.Counter()
    masked = redact(t, c)
    (HERE / "coder-packet-masked/items" / f"{idM[e]}.md").write_text(f"# {idM[e]}\n\n{masked}\n")
    rlog.append(dict(item_id=idM[e], eo_number=e, words_original=len(t.split()), words_masked=len(masked.split()),
                     **{k: v for k, v in sorted(c.items())}))
for e in order_U:
    title = meta[e]["title"] or ""
    if not title.startswith("Executive Order"): title = f"Executive Order {e}—{title}"
    (HERE / "coder-packet-unmasked/items" / f"{idU[e]}.md").write_text(f"# {title}\n\n{text_of(e)}\n")

with open(HERE / "_sealed/key.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["masked_item_id", "unmasked_order_id", "eo_number", "stratum", "date", "president", "validation_class", "in_human_subset"])
    for e in sorted(order_M, key=lambda x: idM[x]):
        w.writerow([idM[e], idU[e], e, stratum[e], meta[e]["date"], meta[e]["pres"][:40], vkey.get(e, ""), int(e in human)])
keys = sorted({k for r in rlog for k in r})
with open(HERE / "_sealed/redaction-log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["item_id", "eo_number", "words_original", "words_masked"] + [k for k in keys if k not in ("item_id", "eo_number", "words_original", "words_masked")])
    w.writeheader(); [w.writerow(r) for r in rlog]

cols = ["item_id"]
for i in range(1, 12): cols += [f"f{i}_status", f"f{i}_note"]
cols += ["f5_zombie_emergency_trap", "minutes_spent", "AFTER_CODING_guess_decade", "AFTER_CODING_guess_president",
         "AFTER_CODING_recognized_order_Y_N", "AFTER_CODING_recognized_as", "general_notes"]
with open(HERE / "human-coding/human-coding-sheet.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for e in sorted(human, key=lambda x: rng.random()):
        w.writerow([idM[e]] + [""] * (len(cols) - 1))
print("strata:", {s: len(v) for s, v in strata.items()}, "human:", len(human))
print("redaction totals:", dict(sum((collections.Counter({k: v for k, v in r.items() if isinstance(v, int) and not k.startswith("words")}) for r in rlog), collections.Counter())))
