import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path
from functools import partial

PORT = 8000
ROOT = Path(__file__).parent.resolve()

AUDIO_EXT = {'.mp3', '.m4a', '.wav', '.ogg', '.flac', '.aac', '.opus'}
IMG_EXT   = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path_only = self.path.split('?')[0]
        if path_only in ('/lista.php', '/lista.json', '/lista'):
            self.serve_lista()
            return
        super().do_GET()

    def serve_lista(self):
        songs = []
        canzoni_dir = ROOT / 'canzoni'
        cover_dir   = ROOT / 'cover'

        if canzoni_dir.is_dir():
            for f in sorted(canzoni_dir.iterdir()):
                if not f.is_file() or f.suffix.lower() not in AUDIO_EXT:
                    continue

                base = f.stem
                artist, title = 'Artista sconosciuto', base
                if ' - ' in base:
                    artist, title = base.split(' - ', 1)

                cover = ''
                for ext in IMG_EXT:
                    if (cover_dir / (base + ext)).exists():
                        cover = 'cover/' + urllib.parse.quote(base + ext)
                        break
                    if (canzoni_dir / (base + ext)).exists():
                        cover = 'canzoni/' + urllib.parse.quote(base + ext)
                        break

                songs.append({
                    'title':  title.strip(),
                    'artist': artist.strip(),
                    'src':    'canzoni/' + urllib.parse.quote(f.name),
                    'cover':  cover
                })

        songs.sort(key=lambda s: s['title'].lower())
        body = json.dumps(songs, ensure_ascii=False).encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)


handler = partial(Handler, directory=str(ROOT))

print()
print("=" * 52)
print("  🎵  Server musicale avviato")
print(f"  Apri nel browser:  http://localhost:{PORT}")
print(f"  Cartella servita:  {ROOT}")
print("  Premi Ctrl+C per fermarlo")
print("=" * 52)
print()

with socketserver.TCPServer(("", PORT), handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer fermato. Ciao!")