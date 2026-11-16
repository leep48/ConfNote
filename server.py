import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def load_env(env_path: Path) -> None:
    """Load key=value pairs from .env into os.environ if not already set."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


BASE_DIR = Path(__file__).resolve().parent
load_env(BASE_DIR / ".env")


class ConfNoteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_POST(self):
        if self.path != "/api/compile":
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(content_length))
        except json.JSONDecodeError:
            self._send_json(400, {"error": {"message": "Invalid JSON body"}})
            return

        model = body.get("model", "gemma-4-31b-it")
        parts = body.get("parts", [])
        api_key = (body.get("apiKey") or os.environ.get("GEMINI_API_KEY", "")).strip()

        if not api_key:
            self._send_json(400, {"error": {"message": "Missing GEMINI_API_KEY in .env or request"}})
            return

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(model, safe='')}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
        )
        payload = json.dumps({"contents": [{"parts": parts}]}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as err:
            err_body = err.read()
            self.send_response(err.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as exc:
            self._send_json(500, {"error": {"message": str(exc)}})

    def _send_json(self, status: int, data: dict) -> None:
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), ConfNoteHandler)
    print(f"ConfNote running at http://localhost:{port}")
    server.serve_forever()
