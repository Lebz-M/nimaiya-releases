// SAMPLE house data — fictional, so the house renders before your own data exists.
// serve.py regenerates this from YOUR local nimaiya house on every request
// (claims, projects, bank, board, rules, hearths). Nothing here is real.
window.HOUSE = {"generated": "sample", "claims": [
  {"holder": "🗡️", "path": "api/routes.ts", "note": "wiring the new endpoint"},
  {"holder": "🪞", "path": "docs/spec.md", "note": "verifying the spec against the build"}
], "projects": [
  {"slug": "first_venture", "live": "https://example.com", "github": ""},
  {"slug": "the_next_thing", "live": "", "github": ""}
], "bank": [
  {"name": "first-venture", "makes-money": "yes", "horizon": "Short-term", "form": "Cash", "updated": "sample"},
  {"name": "the-next-thing", "makes-money": "no", "future-money": "yes", "updated": "sample"}
], "board": [
  "🗡️ BLADE ONE — 09:00 — claim posted: api/routes.ts",
  "🪞 BLADE TWO — 09:02 — verified: spec matches the build, 6/6 checks",
  "👑 THE WIELDER — 09:05 — VERBATIM (spoken at the table)"
], "rules": [
  {"name": "first-word.py", "age": 1},
  {"name": "check-time.py", "age": 1}
], "hearths": [
  {"id": "sample01", "tokens": 42000, "pct": 4.2, "idleMin": 3}
]};
