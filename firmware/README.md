# Firmware-Verzeichnis (Web-Flasher)

Der Web-Flasher auf der Startseite nutzt **ESP Web Tools**. Jedes flashbare Target
braucht hier einen Ordner mit einem `manifest.json` und den `.bin`-Dateien.

## Struktur
```
firmware/
  <repo-id>/
    manifest.json
    firmware.bin        (merged, Offset 0x0 — empfohlen)
```

## manifest.json (Beispiel, ESP32)
```json
{
  "name": "USB Army Penetrator",
  "version": "1.0.0",
  "builds": [
    {
      "chipFamily": "ESP32",
      "parts": [{ "path": "firmware.bin", "offset": 0 }]
    }
  ]
}
```
> Für ein *merged* Binary (via `esptool.py merge_bin`) reicht ein Part mit Offset 0.
> Sonst getrennte Parts: bootloader @ 0x1000, partitions @ 0x8000, app @ 0x10000.

## Target aktivieren
In `index.html` → Array `FIRMWARES` beim passenden Eintrag `status:"ready"` setzen.
Der Flash-Button erscheint dann automatisch.

## Automatisch via CI
Der Workflow `firmware-build.yml` (im jeweiligen ESP32-Repo) baut mit PlatformIO,
führt `merge_bin` aus und veröffentlicht `firmware.bin` + `manifest.json` als
Release-Asset. Ein Sync-Schritt kopiert sie hierher.
