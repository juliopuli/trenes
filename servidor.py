#!/usr/bin/env python3
"""
Servidor local para la app de trenes Renfe.
- Sirve trenes-renfe.html en http://localhost:8000
- Hace de proxy (evita el bloqueo CORS) hacia los dominios *.renfe.com

Uso:   python servidor.py        (Python 3.8+, sin instalar nada)
Luego abre http://localhost:8000
"""
import os
import sys
import urllib.request
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "trenes-renfe.html")
UA = "Mozilla/5.0 (compatible; trenes-renfe-local/1.0)"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            try:
                with open(HTML, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                self._send(404, "No encuentro trenes-renfe.html junto a servidor.py")
            return
        if parsed.path == "/api":
            qs = urllib.parse.parse_qs(parsed.query)
            url = (qs.get("url") or [""])[0]
            host = urllib.parse.urlparse(url).hostname or ""
            if not (host == "renfe.com" or host.endswith(".renfe.com")):
                self._send(403, "Solo se permiten dominios renfe.com")
                return
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    data = r.read()
                    ctype = r.headers.get("Content-Type", "application/json")
                self._send(200, data, ctype)
            except Exception as e:
                self._send(502, f"Error al consultar Renfe: {e}")
            return
        self._send(404, "No encontrado")

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    print(f"Abre http://localhost:{PORT}  (Ctrl+C para parar)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
