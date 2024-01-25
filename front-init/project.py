import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime

PORT = 3000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Custom logic for handling GET requests
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, World!')
        elif parsed_url.path == '/message':
            self.send_response(200)
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        # Custom logic for handling POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())
        
        # Process post_params and save to data.json
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        message_dict = {
            'username': post_params['username'][0],
            'message': post_params['message'][0]
        }

        with open('storage/data.json', 'a') as file:
            json.dump({timestamp: message_dict}, file)
            file.write('\n')

        # Redirect to index after processing POST data
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

