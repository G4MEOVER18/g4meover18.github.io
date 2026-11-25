# PROGRESS

Fortschrittsprotokoll für die schrittweise Weiterentwicklung der Hub-Seite und der CI-Vorlagen.

## Backlog
- [x] CI-Vorlagen: python-lint, platformio-build, flipper-fap, rollout.sh (vorhanden)
- [ ] CI-Vorlagen ergänzen: pages-deploy.yml, tag-basiertes Release mit Changelog, esptool merge_bin + Release-Asset im PlatformIO-Build prüfen
- [ ] Firmware-Manifeste real machen (sobald ein ESP32-Repo per CI firmware.bin + manifest.json als Release hat → `status:"ready"` im FIRMWARES-Array)
- [x] Katalog-Autoupdate: `.github/workflows/update-catalog.yml` + `scripts/update_catalog.py` (nur öffentliche, nicht archivierte Repos)
- [ ] Design/Interaktivität: Detail-Modals pro Tool, Tastaturnavigation, OpenGraph-Vorschaubild, mehr Barrierefreiheit
- [x] SEO: sitemap.xml, robots.txt, canonical, JSON-LD (Person/WebSite)
- [ ] SEO: JSON-LD SoftwareApplication für Flagship-Tools

## Lauf-Log
- 2026-11-25: Katalog-Autoupdate (Workflow + Skript, per Mock-Test idempotent geprüft), sitemap/robots/JSON-LD/canonical ergänzt.
