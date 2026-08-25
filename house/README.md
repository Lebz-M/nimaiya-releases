# The House · :8088

A pixel penthouse for your nimaiya house — every desk is a blade, the screen is the board,
the vault is the bank, the shrine is the laws. Flip the gold button and it becomes a desktop.

## Run
```
python3 serve.py        # http://localhost:8088 — loopback only
```
`serve.py` regenerates `data.js` from YOUR local nimaiya house on every request
(claims · projects · bank · board · rules · live hearths). Until you have one,
the bundled sample data renders a furnished demo house.

## Make the resident you
```
python3 make-you.py your-head.png [your-portrait.png]
```
Head crop on a transparent background → becomes the sprite (43×46) and the framed
portrait. Restyle the `YOU` config in `index.html` (fit, chain, crown, kicks).

## The gallery
Seven frames rotate through `ART[]` in `art.js` — placeholder pieces ship; replace
them with your own work (92×60, data-URIs).

Talks to the real board via `POST /api/say` and reads replies from `GET /api/board`.
Set `NIMAIYA_DEMO_BOARD` to point at a different board file.
