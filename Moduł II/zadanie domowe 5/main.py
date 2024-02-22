from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import mimetypes
import pathlib
import aiohttp
import urllib.parse
from datetime import datetime, timedelta
import asyncio
import sys
import platform
import template_index

HOST = '127.0.0.1'
HTTP_PORT = 3000


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file("index.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
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
    print(f"HTTP server listening on {HOST}:{HTTP_PORT}")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


def url_generate(currency, delta):
    end = datetime.now()
    start = end-timedelta(days=int(delta))
    start_date = start.date()
    end_date = end.date()
    url = f'http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date.isoformat()}/{end_date.isoformat()}/'
    return url


async def get_data():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(open_page(url_generate("EUR", sys.argv[1]), session), open_page(url_generate("USD", sys.argv[1]), session))
        template_index.main(results)


async def open_page(url, session):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                return html
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectionError as error:
        print(f"Connection error: {url}", str(error))


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) > 1 and int(sys.argv[1]) < 11:
        asyncio.run(get_data())
        run()
    else:
        print(f"\nUsage:\npython main 'number of days' or py .\main.py 'number of days'.\nYou can see the exchange rate summary for a maximum of 10 days.\n")
