from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import socket
import mimetypes
import json
import pathlib
import urllib.parse
from datetime import datetime
import threading
import os

HOST = '127.0.0.1'
HTTP_PORT = 3000
SOCKET_PORT = 5000
DATA_FILE_PATH = 'storage/data.json'


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def _write_to_json(message_data):
    if not os.path.exists('storage'):
        os.makedirs('storage')
        print("Folder 'storage' was created")

    timestamp = message_data['timestamp']
    data_to_write = {timestamp: {
        'username': message_data['username'], 'message': message_data['message']}}

    with open(DATA_FILE_PATH, 'a') as file:
        json.dump(data_to_write, file, indent=2)
        file.write('\n')


def _process_form(data):
    messages = []
    if 'username' in data and 'message' in data:
        username = data['username'][0]
        message = data['message'][0]
        timestamp = datetime.now().isoformat()

        message_data = {
            'username': username,
            'message': message,
            'timestamp': timestamp
        }
        messages.append(message_data)
        _write_to_json(message_data)


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == '/':
            self.send_html_file("index.html")
        elif pr_url.path == '/message':
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(post_data)

        _process_form(urllib.parse.parse_qs(post_data))

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=202):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


class SocketServerThread(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))
            print(f"Socket server listening on {self.host}:{self.port}")
            while True:
                data, addr = sock.recvfrom(1024)
                print(f"Received data: {data}")


def main():
    http_server = ThreadedHTTPServer((HOST, HTTP_PORT), HTTPHandler)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()
    print(f"HTTP server listening on {HOST}:{HTTP_PORT}")

    socket_server_thread = SocketServerThread(HOST, SOCKET_PORT)
    socket_server_thread.daemon = True
    socket_server_thread.start()

    print("Servers started successfully!")

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == "__main__":
    main()
