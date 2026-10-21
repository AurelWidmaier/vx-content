# vx-content

Inhalte für **VX Studio**, die nicht in den Installer gehören. Die App lädt sie bei Bedarf über
jsDelivr mit festem Tag (`https://cdn.jsdelivr.net/gh/AurelWidmaier/vx-content@<tag>/…`) und hält
sie lokal im App-Ordner. Ein Tag wird nie verändert – neue Inhalte bekommen einen neuen Tag.

## Inhalt

| Ordner | Was | Quelle | Lizenz |
| --- | --- | --- | --- |
| `sfx/kenney/<paket>/` | Soundeffekte (OGG Vorbis) | [Kenney](https://kenney.nl) – Interface Sounds, UI Audio, Digital Audio, Impact Sounds, Sci-fi Sounds, Casino Audio, RPG Audio, Music Jingles | CC0 1.0 (je Paket `License.txt`) |
| `sfx/catalog.json` | Liste: Kennung, Datei, Name, Kategorie, Dauer, Quelle, Lizenz | erzeugt | – |

Nur Inhalte mit freier Lizenz (CC0, OFL, MIT, Apache-2.0); je Quelle liegt die Lizenzdatei neben den
Dateien. Pixabay/Pexels werden nicht übernommen (Lizenz verbietet Weitergabe als Sammlung).

## Neu bauen

```
python scripts/build_sfx.py <ordner-mit-entpackten-kenney-paketen>
```
