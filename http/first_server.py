import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"GET {self.path}")
        filename = "./http/"
        if self.path == "/":
            filename = "".join([filename, "index.html"])
        else:
            filename = "".join([filename, self.path[self.path.index("/") + 1:]])
            
        if os.path.isfile(filename):
            self.flush_file(filename)
            return

        if self.path == "/auth":
            self.auth()
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("<h1>404</h1>".encode())
        return

    def auth(self):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.send_401("Authorization header required")
            return
        
        if auth_header.startswith("Basic "):
            credentials = auth_header[6:]
        else:
            self.send_401("Authorization scheme Basic required")
            return
        
        try:
            data = base64.b64decode(credentials, validate = True)\
                .decode('utf-8')
        except:
            self.send_401("Invalid credentials: Base64 string required")
            return

        if not ':' in data:
            self.send_401("Invalid credentials: login:password format expected")
            return

        login, password = data.split(':', maxsplit = 1)

        self.send_200(login + password)
        return

    def send_401(self, message = None):
        self.send_response(401, "Unauthorized")
        if message:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def send_200(self, message = None, type = "text"):
        self.send_response(200)
        if type == "json":
            content_type = "application/json"
        else:
            content_type = "text/plain"
        self.send_header("Content-Type", f"{content_type}; charset=UTF-8")
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def flush_file(self, filename: str):
        extension = filename[filename.rindex(".") + 1:]
        if extension == "ico":
            content_type = "image/x-icon"
        elif extension in ("html", "htm"):
            content_type = "text/html"
        elif extension == "js":
            content_type = "application/javascript"
        elif extension == "css":
            content_type = "text/css"
        else:
            content_type = "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()        
        with open(filename, "rb") as file:
            self.wfile.write(file.read())
        return

    def log_request(self, code = ..., size = ...):
        return


def main():
    http_server = HTTPServer(("127.0.0.1", 88), MainHandler)
    try:
        print("Server started")
        http_server.serve_forever()
    except:
        print("Server stopped")


if __name__ == "__main__":
    main()