#!/bin/bash
# nimaiya installer -- downloads the latest release binary and VERIFIES it before it runs.
# curl -fsSL https://raw.githubusercontent.com/Lebz-M/nimaiya-releases/main/install.sh | bash
# Plain ASCII on purpose: macOS ships bash 3.2, which chews multibyte chars next to variables.
set -euo pipefail
REPO="Lebz-M/nimaiya-releases"
DEST="${NIMAIYA_DEST:-$HOME/.local/bin}"
OS="$(uname -s)"; ARCH="$(uname -m)"
if [ "${OS}" = "Darwin" ] && [ "${ARCH}" = "arm64" ]; then ASSET="nimaiya-macos-arm64"
else
  echo "x  no prebuilt binary for ${OS}/${ARCH} yet (currently: macOS Apple Silicon)."
  echo "   watch https://github.com/${REPO}/releases -- more platforms are coming."
  exit 1
fi
TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
echo "-> downloading latest ${ASSET} ..."
curl -fL --progress-bar "https://github.com/${REPO}/releases/latest/download/${ASSET}" -o "${TMP}/${ASSET}"
echo "-> downloading SHA256SUMS ..."
curl -fsSL "https://github.com/${REPO}/releases/latest/download/SHA256SUMS" -o "${TMP}/SHA256SUMS"
echo "-> verifying checksum (the install REFUSES on mismatch) ..."
( cd "${TMP}" && grep " ${ASSET}\$" SHA256SUMS | shasum -a 256 -c - ) || { echo "x  CHECKSUM MISMATCH -- nothing installed. The download is corrupt or tampered."; exit 1; }
mkdir -p "${DEST}"
install -m 755 "${TMP}/${ASSET}" "${DEST}/nimaiya"
echo "OK installed: ${DEST}/nimaiya ($("${DEST}/nimaiya" --version))"
case ":${PATH}:" in *":${DEST}:"*) : ;; *) echo "!  add to PATH:  export PATH=\"${DEST}:\$PATH\"" ;; esac
echo "next: run nimaiya -- the front door greets you."
