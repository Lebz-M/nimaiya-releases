#!/usr/bin/env python3
# Snapshot REAL house state into data.js — the demo shows the actual house, not lorem.
# Re-run any time; the page just includes the result.
import json, os, re, glob, time
H = os.path.expanduser("~")
out = {"generated": time.strftime("%Y-%m-%d %H:%M:%S")}

# blades + live claims (who holds what, right now)
claims = []
for f in glob.glob(H + "/.nimaiya/claims/*.json"):
    try:
        j = json.load(open(f))
        claims.append({"holder": j.get("holder","?"), "path": os.path.basename(j.get("path","")),
                       "note": (j.get("note") or "")[:90]})
    except Exception: pass
out["claims"] = claims

# projects (top few, with links when present)
projects = []
try:
    pj = json.load(open(H + "/.nimaiya/projects.json"))
    items = pj if isinstance(pj, list) else pj.get("projects", [])
    for p in items:
        links = p.get("links") or {}
        projects.append({"slug": p.get("slug") or p.get("name",""),
                         "live": links.get("live",""), "github": links.get("github","")})
except Exception: pass
out["projects"] = [p for p in projects if p["slug"]][:10] or \
    [{"slug": s, "live": "", "github": ""} for s in
     ["blinkip","hereyougo","rugby-overlay","tripza","girlhype","latent","supremacy","ive"]]

# bank ledger
bank = []
try:
    cur = None
    for line in open(H + "/.nimaiya/bank/ledger.md"):
        m = re.match(r"^## (.+)$", line)
        if m: cur = {"name": m.group(1).strip()}; bank.append(cur); continue
        kv = re.match(r"^- ([a-z-]+): (.+)$", line)
        if kv and cur is not None: cur[kv.group(1)] = kv.group(2).strip()
except Exception: pass
out["bank"] = bank

# last board headings (fence-aware enough for a demo: leading '## ' only)
heads = []
try:
    fence = False
    for line in open(H + "/My-Claude/nimaiya/home.md"):
        if line.startswith("```"): fence = not fence; continue
        if not fence and line.startswith("## "):
            heads.append(re.sub(r"\*\*|`", "", line[3:]).strip()[:110])
    heads = heads[-10:]
except Exception: pass
out["board"] = heads

# rules with ages (the laws surface)
rules = []
try:
    hooks = H + "/.claude/hooks"
    for f in sorted(os.listdir(hooks)):
        if f.endswith(".py") and not f.startswith("_"):
            age = int((time.time() - os.path.getmtime(os.path.join(hooks,f))) / 86400)
            rules.append({"name": f, "age": age})
except Exception: pass
out["rules"] = rules[:8]

# hearths: live context monitors — the 18:32 screenshot (Hermes' `21.9K/1M [bar] 2%%`) made
# real for OUR sessions. Reuses the 800k hook's method: tail-read the newest usage line of
# each recently-active transcript. Session→blade mapping is NOT knowable from here, so rows
# are labeled by recency, not by name — the record admits what it knows.
hearths = []
try:
    tdir = H + "/.claude/projects/-" + os.path.expanduser("~").strip("/").replace("/", "-")
    cands = [f for f in glob.glob(tdir + "/*.jsonl") if time.time() - os.path.getmtime(f) < 3*3600]
    cands.sort(key=os.path.getmtime, reverse=True)
    for f in cands[:6]:
        tokens = 0
        try:
            size = os.path.getsize(f)
            with open(f, "rb") as fh:
                fh.seek(max(0, size - 262144))
                for line in reversed(fh.read().decode("utf-8", "ignore").splitlines()):
                    try: j = json.loads(line)
                    except Exception: continue
                    u = (j.get("message") or {}).get("usage")
                    if isinstance(u, dict) and "input_tokens" in u:
                        tokens = (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
                        break
        except Exception: pass
        if tokens:
            hearths.append({"id": os.path.basename(f)[:8], "tokens": tokens,
                            "pct": round(tokens/1_000_000*100, 1),
                            "idleMin": int((time.time()-os.path.getmtime(f))/60)})
except Exception: pass
out["hearths"] = hearths

open("data.js","w").write("window.HOUSE = " + json.dumps(out, ensure_ascii=False) + ";")
print("data.js written:", os.path.getsize("data.js"), "bytes ·",
      len(claims), "claims ·", len(out['projects']), "projects ·", len(bank), "bank rows ·",
      len(heads), "headings ·", len(rules), "rules")
