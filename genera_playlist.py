import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
CANZONI_DIR = ROOT / 'canzoni'
COVER_DIR = ROOT / 'cover'

AUDIO_EXT = {'.mp3', '.m4a', '.wav', '.ogg', '.flac', '.aac', '.opus'}
IMG_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


def genera_playlist():
    songs = []

    if CANZONI_DIR.is_dir():
        for f in sorted(CANZONI_DIR.iterdir()):
            if not f.is_file() or f.suffix.lower() not in AUDIO_EXT:
                continue

            base = f.stem
            artist, title = 'Artista sconosciuto', base
            if ' - ' in base:
                artist, title = base.split(' - ', 1)

            # Cerca copertina con lo stesso nome
            cover = ''
            for ext in IMG_EXT:
                if (COVER_DIR / (base + ext)).exists():
                    cover = 'cover/' + urllib.parse.quote(base + ext)
                    break
                if (CANZONI_DIR / (base + ext)).exists():
                    cover = 'canzoni/' + urllib.parse.quote(base + ext)
                    break

            songs.append({
                'title': title.strip(),
                'artist': artist.strip(),
                'src': 'canzoni/' + urllib.parse.quote(f.name),
                'cover': cover
            })

    songs.sort(key=lambda s: s['title'].lower())

    with open(ROOT / 'playlist.json', 'w', encoding='utf-8') as fp:
        json.dump(songs, fp, ensure_ascii=False, indent=2)

    print(f'✅ Generati {len(songs)} brani in playlist.json')
    for s in songs:
        print(f"   · {s['title']} — {s['artist']}")


if __name__ == '__main__':
    genera_playlist()