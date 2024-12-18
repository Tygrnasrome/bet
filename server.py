from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import unquote

hostName = "localhost"
serverPort = 8080
base_directory = "templates"
static_directory = "static"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = unquote(self.path.strip("/"))  # Decode URL-encoded paths
        if file_path == "":
            file_path = "index.html"

        # Determine the directory to serve from
        if file_path.startswith("static/"):
            full_path = os.path.join(static_directory, file_path[len("static/"):])
        else:
            full_path = os.path.join(base_directory, file_path)

        try:
            if os.path.isfile(full_path):
                # Determine the Content-Type based on the file extension
                mime_type = self.get_mime_type(full_path)
                with open(full_path, "rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", mime_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.wfile.write(e) 
            self.end_headers()
            self.wfile.write(b"<html><body><h1>500 Internal Server Error</h1></body></html>")

    def get_mime_type(self, file_path):
        # Map file extensions to MIME types
        extension = os.path.splitext(file_path)[1].lower()
        return {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".ico": "image/x-icon",
            ".json": "application/json",
            ".webmanifest": "application/manifest+json",
        }.get(extension, "application/octet-stream")  # Default MIME type

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")

