#!/usr/bin/env python3
"""Aktualisiert das REPOS-Array in index.html aus `gh repo list --json`-Daten.

Regeln:
- Nur öffentliche, nicht archivierte Repos (private werden strikt ausgeschlossen).
- Kuratierte Felder (cat, d, flag, rel, fw, pages) bestehender Einträge bleiben erhalten.
- Aktualisiert werden: Sterne (s), Sprache (lang), Wiki-Flag (w).
- Neue Repos landen mit cat "Sonstige" und ihrer GitHub-Beschreibung am Ende.
- Repos, die nicht mehr öffentlich/aktiv sind, werden entfernt.

Aufruf:  python3 scripts/update_catalog.py repos.json [index.html]
repos.json = Ausgabe von:
  gh repo list G4MEOVER18 --limit 200 --json name,description,primaryLanguage,isArchived,visibility,stargazerCount,hasWikiEnabled,isFork
"""
import json, re, sys
from pathlib import Path

BLOCK = re.compile(r"(const REPOS = \[\n)(.*?)(\n\];)", re.S)
ENTRY = re.compile(r"  \{n:\"(?P<n>[^\"]+)\", cat:\"(?P<cat>[^\"]*)\", lang:\"(?P<lang>[^\"]*)\", "
                   r"s:(?P<s>\d+), w:(?P<w>true|false)(?P<extra>[^\n]*)\n\s+d:(?P<d>\"(?:[^\"\\]|\\.)*\")(?P<tail>[^}]*)\}", re.S)


def parse(block):
    out = []
    for m in ENTRY.finditer(block):
        flags = re.findall(r"(flag|rel|fw|pages):true", m["extra"] + m["tail"])
        out.append({"n": m["n"], "cat": m["cat"], "lang": m["lang"], "s": int(m["s"]),
                    "w": m["w"] == "true", "flags": flags, "d": m["d"]})
    return out


def fmt(e):
    extra = "".join(f", {f}:true" for f in e["flags"] if f in ("flag",))
    tail = "".join(f", {f}:true" for f in e["flags"] if f != "flag")
    return (f'  {{n:"{e["n"]}", cat:"{e["cat"]}", lang:"{e["lang"]}", s:{e["s"]}, '
            f'w:{"true" if e["w"] else "false"}{extra},\n   d:{e["d"]}{tail}}}')


def main():
    repos_file = Path(sys.argv[1])
    index = Path(sys.argv[2] if len(sys.argv) > 2 else "index.html")
    gh = json.loads(repos_file.read_text(encoding="utf-8"))
    live = {r["name"]: r for r in gh
            if str(r.get("visibility", "")).upper() == "PUBLIC" and not r.get("isArchived")}
    if not live:
        sys.exit("Abbruch: keine öffentlichen Repos geliefert (API-Fehler?) — Katalog bleibt unverändert.")

    html = index.read_text(encoding="utf-8")
    m = BLOCK.search(html)
    if not m:
        sys.exit("REPOS-Block nicht gefunden.")
    entries = parse(m.group(2))
    if not entries:
        sys.exit("Keine Einträge geparst — Format geändert?")

    result, seen = [], set()
    for e in entries:
        r = live.get(e["n"])
        if not r:
            print(f"ENTFERNT {e['n']} (nicht mehr öffentlich/aktiv)")
            continue
        e["s"] = r.get("stargazerCount", e["s"])
        e["w"] = bool(r.get("hasWikiEnabled", e["w"]))
        lang = (r.get("primaryLanguage") or {}).get("name")
        if lang:
            e["lang"] = lang
        result.append(e); seen.add(e["n"])
    for name, r in sorted(live.items()):
        if name in seen or name == "g4meover18.github.io" or name == "G4MEOVER18":
            continue
        desc = (r.get("description") or "Keine Beschreibung.").replace("\\", "\\\\").replace('"', '\\"')
        lang = (r.get("primaryLanguage") or {}).get("name") or ""
        result.append({"n": name, "cat": "Sonstige", "lang": lang, "s": r.get("stargazerCount", 0),
                       "w": bool(r.get("hasWikiEnabled")), "flags": [], "d": f'"{desc}"'})
        print(f"NEU      {name}")

    new_block = ",\n".join(fmt(e) for e in result)
    index.write_text(html[:m.start(2)] + new_block + html[m.end(2):], encoding="utf-8")
    print(f"{len(result)} Repos geschrieben.")


if __name__ == "__main__":
    main()
