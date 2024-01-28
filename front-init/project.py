import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime
import socket
import threading

PORT = 3000
SOCKET_PORT = 5000

def save_message_to_json(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    message_dict = {'username': username, 'message': message}
    with open('storage/data.json', 'a') as file:
        json.dump({timestamp: message_dict}, file)
        file.write('\n')

def start_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', SOCKET_PORT))
    while True:
        data, addr = server.recvfrom(1024)
        message_dict = json.loads(data.decode())
        save_message_to_json(message_dict['username'], message_dict['message'])

def start_web_server():
    handler = MyHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/':
            self.send_response(200)
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_url.path == '/message':
            self.send_response(200)
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_url.path == '/logo.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo.png', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode())
        save_message_to_json(post_params['username'][0], post_params['message'][0])

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == "__main__":
    socket_thread = threading.Thread(target=start_socket_server)
    socket_thread.start()

    start_web_server()
