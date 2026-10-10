#!/usr/bin/env python3
"""Local web server for Builder Prep. Same as python3 -m http.server, but tells the browser never to reuse old copies of files,
so updated lessons and scripts always show up on a normal reload. Usage: python3 tools/serve.py [port]"""
import http.server, os, sys
class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()
    def log_message(self, *a): pass
if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(('127.0.0.1', port), NoCache).serve_forever()
