#!/usr/bin/env python3
# Serve the vision demo with LIVE house data: data.js is regenerated on every request,
# so the office can never contradict `nimaiya claims`. 🗡️ caught the stale-snapshot
# failure ("if he reads a desk that contradicts the registry, the demo's whole claim —
# real data — dies on the spot"). This is the fix, not a reminder to re-run a script.
#
# 08-22 (👑 04:30): "the game mode should link to real terminal chats · desktop mode should
# also allow me to interface real hearths." The real channel this house runs on is the
# BOARD — every blade's terminal watches it, and `nimaiya table` writes his words to it as
# `## 👑 THE WIELDER — HH:MM — VERBATIM (...)`. So the game and the desktop write the same
# heading, to the same file, and read replies back from it. Nothing simulated:
#   POST /api/say      {text, to?, via}  → appends a 👑 entry to the home board
#   GET  /api/board?after=N             → entries after index N (heading + body), for replies
#   GET  /api/hearths                   → live hearths (context) + which blade wears which
# Loopback only, as before. The board path is the one the CLI symlinks (FORGE-BOARD.md → home.md).
import http.server, subprocess, os, json, re, time, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
BOARD = os.environ.get("NIMAIYA_DEMO_BOARD") or os.path.realpath(f"{HOME}/My-Claude/nimaiya/FORGE-BOARD.md")

def entries():
    try: txt = open(BOARD, encoding="utf-8", errors="replace").read()
    except FileNotFoundError: return []
    parts = re.split(r"(?m)^(?=## )", txt)
    out = []
    for p in parts:
        if not p.startswith("## "): continue
        head, _, body = p.partition("\n")
        out.append({"heading": head[3:].strip(), "body": body.strip()[:1200]})
    return out

def hearths():
    subprocess.run(["python3", "build-data.py"], capture_output=True)
    data = {}
    try:
        js = open("data.js", encoding="utf-8").read()
        data = json.loads(js[js.index("{"):js.rindex("}")+1])
    except Exception: pass
    wear = {}
    for f in glob.glob(f"{HOME}/.nimaiya/presence/*.json"):
        try:
            p = json.load(open(f)); wear[os.path.basename(p["transcript"])[:8]] = p["blade"]
        except Exception: pass
    hs = data.get("hearths", [])
    for h in hs: h["blade"] = wear.get(h["id"])
    return {"hearths": hs, "generated": data.get("generated")}

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        path, _, qs = self.path.partition("?")
        if path == "/data.js": subprocess.run(["python3", "build-data.py"], capture_output=True)
        if path == "/api/hearths": return self._json(hearths())
        if path == "/api/board":
            q = dict(x.split("=", 1) for x in qs.split("&") if "=" in x)
            after = int(q.get("after", "0") or 0); es = entries()
            return self._json({"total": len(es), "entries": [dict(i=i, **e) for i, e in enumerate(es) if i >= after][-40:]})
        super().do_GET()
    def do_POST(self):
        if self.path.split("?")[0] != "/api/say": return self._json({"error": "no such route"}, 404)
        n = int(self.headers.get("Content-Length", "0") or 0)
        try: body = json.loads(self.rfile.read(n) or b"{}")
        except Exception: return self._json({"error": "bad json"}, 400)
        text = (body.get("text") or "").strip()
        if not text: return self._json({"error": "empty"}, 400)
        if not os.path.exists(BOARD): return self._json({"error": f"board missing: {BOARD}"}, 500)
        to = (body.get("to") or "").strip(); via = (body.get("via") or "the house").strip()
        stamp = time.strftime("%H:%M")
        where = f"spoken in {via}" + (f" · @{to}" if to else "")
        entry = f"\n## 👑 THE WIELDER — {stamp} — VERBATIM ({where})\n\n{text}\n\n---\n"
        with open(BOARD, "a", encoding="utf-8") as f: f.write(entry)
        return self._json({"ok": True, "stamp": stamp, "index": len(entries()) - 1})
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", 8088), H).serve_forever()
