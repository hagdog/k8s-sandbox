import os
import sys
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Testing  load balancer sheduling and pod restarts.
        # Otherwise, O/S-specific data not normally served.
        self.wfile.write(str.encode(f"GET request provided by {os.getpid()}."))


def clean_exit(http_server):
    httpd.server_close()
    print("Server stopped.")
    sys.exit(0)


if __name__ == "__main__":
    host = os.getenv("HTTP_HOST", "localhost")
    port = os.getenv("HTTP_PORT", 8088)
    try:
        port = int(port)
    except ValueError as e:
        print(f"HTTP_PORT must be an integer: {e}")
        sys.exit(1)

    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Server started http://{host}:{port}")

    # A clean exit for normal shutdown in a container.
    def __handle_sigterm(signum, sigstack):
        print(f"SIGTERM received.")
        clean_exit(httpd)

    signal.signal(signal.SIGTERM, __handle_sigterm)

    # A clean exit from a command line request.
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"Keyboard interrupt received.")

    clean_exit(httpd)
