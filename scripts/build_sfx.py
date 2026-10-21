"""Baut sfx/ aus den Kenney-Audiopaketen (CC0) und schreibt sfx/catalog.json.

Aufruf: python scripts/build_sfx.py <ordner-mit-entpackten-paketen>
Jedes Paket liegt dort als <paket>/Audio/**.ogg + License.txt (wie von kenney.nl geladen).
Die Dateien werden unverändert kopiert (OGG Vorbis), Dauer per ffprobe.
"""

import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Paket → (Kategorie-Kennung, Quelle)
PACKS = {
    "interface-sounds": "ui",
    "ui-audio": "ui",
    "digital-audio": "digital",
    "impact-sounds": "impact",
    "sci-fi-sounds": "scifi",
    "casino-audio": "casino",
    "rpg-audio": "rpg",
    "music-jingles": "jingle",
}

CATEGORIES = {
    "ui": {"de": "Klicks & Oberfläche", "en": "Clicks & UI"},
    "digital": {"de": "Digital", "en": "Digital"},
    "impact": {"de": "Aufprall & Schritte", "en": "Impacts & steps"},
    "scifi": {"de": "Sci-Fi", "en": "Sci-fi"},
    "casino": {"de": "Karten & Münzen", "en": "Cards & coins"},
    "rpg": {"de": "Abenteuer", "en": "Adventure"},
    "jingle": {"de": "Jingles", "en": "Jingles"},
}


def label(stem: str) -> str:
    """„impactGlass_heavy_003“ → „Impact glass heavy 3“."""
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", stem).replace("_", " ").replace("-", " ")
    s = re.sub(r"\b0+(\d)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:1].upper() + s[1:].lower()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return round(float(out), 3)


def main(src: str) -> None:
    out_dir = os.path.join(ROOT, "sfx")
    shutil.rmtree(out_dir, ignore_errors=True)
    entries = []
    for pack, category in PACKS.items():
        base = os.path.join(src, pack)
        target = os.path.join(out_dir, "kenney", pack)
        os.makedirs(target, exist_ok=True)
        shutil.copy(os.path.join(base, "License.txt"), os.path.join(target, "License.txt"))
        files = []
        for dirpath, _, names in os.walk(os.path.join(base, "Audio")):
            for n in names:
                if n.lower().endswith(".ogg"):
                    files.append(os.path.join(dirpath, n))
        for path in sorted(files):
            stem = os.path.splitext(os.path.basename(path))[0]
            name = slug(stem) + ".ogg"
            dest = os.path.join(target, name)
            shutil.copy(path, dest)
            entries.append(
                {
                    "id": f"kenney-{slug(pack)}-{slug(stem)}",
                    "file": f"sfx/kenney/{pack}/{name}",
                    "label": label(stem),
                    "category": category,
                    "duration": duration(dest),
                    "source": "Kenney",
                    "license": "CC0-1.0",
                }
            )
    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids)), "doppelte Kennungen"
    catalog = {"version": 1, "categories": CATEGORIES, "sounds": entries}
    with open(os.path.join(out_dir, "catalog.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(len(entries), "Sounds")


if __name__ == "__main__":
    main(sys.argv[1])
