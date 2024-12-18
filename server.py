from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "0.0.0.0"
serverPort = 8080
base_directory = "templates"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = self.path.strip("/")
        if file_path == "":
            file_path = "index.html"
        
        full_path = os.path.join(base_directory, file_path)
        try:
            if os.path.isfile(full_path):
                with open(full_path, "rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
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
            self.end_headers()
            self.wfile.write(b"<html><body><h1>500 Internal Server Error</h1></body></html>")

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")

