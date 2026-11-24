#!/usr/bin/env bash
# Rollt die CI-Vorlagen auf die passenden G4MEOVER-Repos aus (via gh API, Default-Branch).
# Idempotent: existierende Workflows werden uebersprungen. Commits laufen auf den gh-Nutzer.
set -uo pipefail
OWNER=G4MEOVER18
DIR="$(cd "$(dirname "$0")" && pwd)"

push() {  # $1=repo  $2=quelldatei  $3=zielname
  local repo="$1" src="$2" name="$3" path
  path=".github/workflows/$3"
  if gh api "repos/$OWNER/$repo/contents/$path" >/dev/null 2>&1; then
    echo "SKIP  $repo ($name existiert bereits)"; return 0
  fi
  local b64; b64=$(base64 -w0 "$DIR/$src")
  if gh api -X PUT "repos/$OWNER/$repo/contents/$path" \
       -f message="CI: $name via rollout hinzugefuegt" \
       -f content="$b64" >/dev/null 2>&1; then
    echo "OK    $repo <- $name"
  else
    echo "FAIL  $repo <- $name"
  fi
}

PYTHON="web-recon-toolkit subdomain-takeover-scanner http-header-auditor sqli-hunter cors-scanner xss-hunter hashpwn jwt-pwn netmap g4meover-security-suite g4meover-pentest-cockpit g4meover-deck StoneBook"
PLATFORMIO="stm32-usb-fuzzer heltec-v4-hub heltec-ukfe-rx g4meover-wifi-relay lilygo-ukfe-rx usb-army-penetrator ESP32S3-MiniPwn-Dashboard ESP32-LCD-Time-SD-FTP LoRa-Ra-08-CubeCell ESP32-CaptivePortal RadioGateway TFT-AutoProbe"
FLIPPER="lora-ukfe RollLab RollJam ProtoPirate RollForge FlipperJammer"

echo "== Python-Lint =="
for r in $PYTHON;     do push "$r" python-lint.yml      python-lint.yml;      done
echo "== PlatformIO-Build =="
for r in $PLATFORMIO; do push "$r" platformio-build.yml platformio-build.yml; done
echo "== Flipper-FAP =="
for r in $FLIPPER;    do push "$r" flipper-fap.yml       flipper-fap.yml;      done
