#!/usr/bin/env python3
"""Read-only diagram service. Explicit allowlist, no directory browsing or uploads."""
import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True, help='Curated public directory only')
    p.add_argument('--allowlist', type=Path, required=True, help='JSON array of published relative paths')
    p.add_argument('--host', default='127.0.0.1', help='Use 0.0.0.0 only for requested LAN access')
    p.add_argument('--port', type=int, default=8925)
    a = p.parse_args()
    root = a.root.resolve()
    allowed = json.loads(a.allowlist.read_text(encoding='utf-8'))
    if not isinstance(allowed,list) or not allowed or any(not isinstance(x,str) for x in allowed):
        p.error('allowlist must be a nonempty JSON string array')
    extensions = {'.html','.svg','.png','.jpg','.jpeg','.webp','.css','.js','.woff','.woff2'}
    for rel in allowed:
        target = (root / rel).resolve()
        if Path(rel).is_absolute() or '..' in Path(rel).parts or not target.is_relative_to(root) or not target.is_file() or target.suffix.lower() not in extensions:
            p.error(f'Invalid public asset: {rel}')
    allowed = set(allowed)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(root),**kwargs)

        def permitted(self):
            rel = unquote(urlsplit(self.path).path).lstrip('/') or 'index.html'
            target = (root / rel).resolve()
            return rel in allowed and target.is_relative_to(root) and target.is_file()

        def do_GET(self):
            if not self.permitted():
                self.send_error(404)
                return
            super().do_GET()

        def do_HEAD(self):
            if not self.permitted():
                self.send_error(404)
                return
            super().do_HEAD()

        def end_headers(self):
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Cache-Control','no-cache')
            super().end_headers()

        def list_directory(self,path):
            self.send_error(404)
            return None

    with ThreadingHTTPServer((a.host,a.port),Handler) as server:
        print(f'Diagram service http://{a.host}:{server.server_port}/ (read-only, no password)',flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
