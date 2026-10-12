import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

app_env = os.getenv("APP_ENV", "development")


class CloudForgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "application": "CloudForge",
                "environment": app_env,
            }

            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/":
            body = (
                f"CloudForge application is running in "
                f"{app_env} environment!"
            ).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            body = json.dumps({"error": "Not found"}).encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), CloudForgeHandler)

    print(f"CloudForge running in {app_env} environment on port {port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down CloudForge...")
    finally:
        server.server_close()
