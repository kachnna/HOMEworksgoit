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
        post_data = self.rfile.read(content_length)
        print(post_data)

        socket_run_client(HOST, SOCKET_PORT, post_data)

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


def run():
    http_server = ThreadedHTTPServer((HOST, HTTP_PORT), HTTPHandler)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()
    print(f"HTTP server listening on {HOST}:{HTTP_PORT}")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


def storage_folder():
    if not os.path.exists('storage'):
        os.makedirs('storage')
        print("Folder 'storage' was created")
    data_file_path = os.path.join('storage', 'data.json')
    if not os.path.exists(data_file_path):
        with open(data_file_path, 'w') as f:
            f.write('{}')
        print("File 'data.json' was created")


def socket_run_client(ip=HOST, port=SOCKET_PORT, data=b""):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ((ip, port))
    for i in range(0, len(data), 1024):
        data_part = data[i: i + 1024]
        sock.sendto(data_part, (ip, port))
    sock.sendto(b"END", server)
    sock.close()


def socket_run_server(ip=HOST, port=SOCKET_PORT):
    storage_folder()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ((ip, port))
    sock.bind(server)
    to_save = b""
    file_name = './storage/data.json'
    try:
        while True:
            data, address = sock.recvfrom(1024)
            if data == b"END":
                to_save_parse = urllib.parse.unquote_plus(to_save.decode())
                data_dict = {key: value for key, value in [
                    el.split('=') for el in to_save_parse.split('&')]}
                with open(file_name, "r") as fh:
                    json_dict = json.load(fh)
                json_dict[str(datetime.now())] = data_dict
                with open(file_name, "w") as fh:
                    json.dump(json_dict, fh)
                to_save = b""
            else:
                to_save += data
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def main():
    http_server = threading.Thread(target=run)
    socket_server = threading.Thread(
        target=socket_run_server, args=(HOST, SOCKET_PORT))
    socket_server.start()
    http_server.start()
    socket_server.join()
    http_server.join()
    print("Servers started successfully!")


if __name__ == '__main__':
    main()
