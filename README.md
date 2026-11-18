# g4meover18.github.io

Professionelle Portfolio- & Tool-Hub-Seite von **Yanis Ameseder (G4MEOVER18)**.

🔗 **Live:** https://g4meover18.github.io

## Was die Seite kann
- **Tool-/Repo-Explorer** — alle öffentlichen Projekte durchsuchbar, filterbar, sortierbar (datengetrieben aus `REPOS` in `index.html`).
- **Web-Flasher** — ESP32-Firmware direkt im Browser via Web Serial (ESP Web Tools) + Flipper-Zero-Firmware-Hub.
- **Support** — PayPal + Bitcoin mit QR-Codes und Copy-Buttons.
- **Bio** — kuratiert aus dem Profil-README.

## Technik
- Eine eigenständige `index.html` (kein Build-Schritt, kein Framework).
- Externe Libs nur: `qrcodejs` (cdnjs), `esp-web-tools` (unpkg), Google Fonts.
- Dark-first mit Theme-Toggle, voll responsiv, `prefers-reduced-motion`-sicher.

## Pflege
Die Repo-Karten stehen als JSON-Array `REPOS` oben im `<script>` von `index.html`.
Der Workflow `.github/workflows/update-catalog.yml` kann sie automatisch aus der
GitHub-API neu generieren (nächtlich/auf Abruf).

## Firmware fürs Web-Flashing hinzufügen
Siehe `firmware/README.md`. Kurz: pro Target einen Ordner `firmware/<repo>/` mit
`manifest.json` + `.bin`-Dateien; dann im `FIRMWARES`-Array `status:"ready"` setzen.
