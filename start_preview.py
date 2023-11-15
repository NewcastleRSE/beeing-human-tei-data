import sys
import time
import threading
import webbrowser
from scripts import automate_variation
from http.server import HTTPServer, SimpleHTTPRequestHandler

ip = "localhost"
port = 8000
url = f"http://{ip}:{port}/preview"


def start_server():
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def run_server():
    threading.Thread(target=start_server).start()
    webbrowser.open_new(url)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

def main():
    automate_variation.main(True)
    run_server()

if __name__ == '__main__':
    main()