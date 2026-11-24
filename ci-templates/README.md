# CI-Vorlagen & Rollout

Wiederverwendbare GitHub-Actions-Workflows fuer das G4MEOVER-Repo-Oekosystem.

| Vorlage | Zielrepos | Zweck |
|---|---|---|
| `python-lint.yml` | Python-Tools | Ruff-Lint (als Annotationen, nicht-blockierend) + Syntax-Check |
| `platformio-build.yml` | ESP32/STM32 mit `platformio.ini` | `pio run`, laedt `firmware.bin`/`.elf` als Artefakt hoch |
| `flipper-fap.yml` | Flipper-Apps mit `application.fam` | `ufbt`-Build, laedt `.fap` als Artefakt hoch |

## Ausrollen
```bash
./rollout.sh        # idempotent, ueberspringt vorhandene Workflows
```
Die Repo-Listen stehen oben in `rollout.sh`. Neue Repos dort eintragen.

## Design-Entscheidungen
- **Defensiv:** Build-Workflows pruefen erst, ob die Build-Datei existiert, und ueberspringen sauber statt rot zu werden.
- **Nicht-blockierend am Anfang:** Lint und FAP-Build brechen den Check (noch) nicht ab — erst Sichtbarkeit schaffen, spaeter verschaerfen.
- **Firmware → Web-Flasher:** `firmware.bin`-Artefakte sind die Grundlage, um pro Geraet ein `manifest.json` zu erzeugen und das Target auf der Hub-Seite auf `ready` zu setzen.
