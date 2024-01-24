from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
from threading import Thread

app = Flask(__name__)

# Config
WEB_PORT = 3000
SOCKET_PORT = 5000

# Socket server
def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', SOCKET_PORT))

    while True:
        data, addr = server.recvfrom(1024)
        message_dict = json.loads(data.decode())

        # Save to data.json
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open('storage/data.json', 'a') as file:
            json.dump({timestamp: message_dict}, file)
            file.write('\n')

# Start socket server in a separate thread
socket_thread = Thread(target=socket_server)
socket_thread.start()

# Web routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        # Send data to socket server
        message_dict = {
            'username': request.form['username'],
            'message': request.form['message']
        }
        message_str = json.dumps(message_dict)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(message_str.encode(), ('localhost', SOCKET_PORT))
        client.close()
        return redirect(url_for('index'))

    return render_template('message.html')

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    # Start Flask web server
    app.run(port=WEB_PORT, debug=True)
