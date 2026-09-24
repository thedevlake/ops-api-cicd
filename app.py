from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import platform


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "ok"
            }

        elif self.path == "/system":
            response = {
                "platform": platform.system(),
                "python": platform.python_version()
            }

        else:
            response = {
                "error": "Not found"
            }

        body = json.dumps(response).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)


server = HTTPServer(("0.0.0.0", 8000), Handler)

print("Ops API running on port 8000")

server.serve_forever()
