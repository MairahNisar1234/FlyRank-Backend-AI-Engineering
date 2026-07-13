import json
import random
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8000


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Health Check
        if path == "/api/health":
            self.send_json({
                "status": "ok",
                "message": "Server is running!"
            })

        # Greeting
        elif path == "/api/greet":
            name = query.get("name", ["World"])[0]

            self.send_json({
                "message": f"Hello, {name}!"
            })

        # Student Information
        elif path == "/api/student":
            self.send_json({
                "name": "Mairah",
                "university": "UTM",
                "degree": "Master of Data Science",
                "semester": 1
            })

        # Current Time
        elif path == "/api/time":
            self.send_json({
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # Random Number
        elif path == "/api/random":
            self.send_json({
                "number": random.randint(1, 100)
            })

        # Add Two Numbers
        elif path == "/api/add":
            try:
                a = int(query.get("a", [0])[0])
                b = int(query.get("b", [0])[0])

                self.send_json({
                    "a": a,
                    "b": b,
                    "sum": a + b
                })

            except ValueError:
                self.send_json({
                    "error": "Please provide valid numbers."
                }, status=400)

        # Book Information
        elif path == "/api/book":
            self.send_json({
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "year": 1937
            })

        # Quote
        elif path == "/api/quote":
            quotes = [
                "Keep learning.",
                "Practice makes progress.",
                "Every expert was once a beginner.",
                "Code. Test. Improve."
            ]

            self.send_json({
                "quote": random.choice(quotes)
            })

        # Unknown endpoint
        else:
            self.send_json({
                "error": "Endpoint not found."
            }, status=404)

    def log_message(self, format, *args):
        print(f"[SERVER] {self.address_string()} - {format % args}")


def main():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Server running at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()