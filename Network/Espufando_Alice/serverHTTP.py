import http.server
import socketserver

hostName = "172.19.0.127"
serverPort = 80

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/debian/pool/main/g/gnome-calculator':
            self.send_response(200)
            self.send_header('Content-Disposition', 'attachment; filename=gnome-calculator_43.0.1-2_amd64.deb')
            self.send_header('Content-Length', str(os.path.getsize(file_path)))
            self.send_header('X-HTTP-Version', self.request_version)
            self.end_headers()
            with open('./debian/pool/main/g/gnome-calculator/gnome-calculator_43.0.1-2_amd64.deb', 'rb') as f:
                self.wfile.write(f.read())
            self.wfile.close()
        else:
            super().do_GET()

try:
    with socketserver.TCPServer((hostName, serverPort), CustomHandler) as httpd:
        print(f"Servidor rodando na porta {serverPort}")
        httpd.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down server')
    httpd.socket.close()
