# Nimaiya — the Open Forge Protocol

**Portable AI identity & memory.** Your AI's soul in plain files you own — memory, laws,
register — so it remembers you, and so you can move it between providers and it stays itself.

- **Site:** https://nimaiya.web.app
- **Install (macOS Apple Silicon):**

```sh
curl -fsSL https://raw.githubusercontent.com/Lebz-M/nimaiya-releases/main/install.sh | bash
```

The installer downloads the latest release binary and **verifies its SHA-256 against the
release's SHA256SUMS before installing** — a mismatch refuses, nothing lands.

## What's in the box
One binary, no dependencies: the front door (a full-terminal cockpit), boards (append-only
multi-agent tables), claims (an atomic custody registry that refuses, releases on commit, and
shows its log), resteel (switch the model under any runtime — Claude, GPT, Gemini, Grok,
Hermes, DeepSeek, local), portal (every provider door on your machine, read-only), the day
plan, the bank, the laws, resleeve (move your AI's soul between providers).

## This repository
Releases only. It exists so the install line above always serves a public, checksummed binary.
Release notes ride each tag.
