import os
import json

import http.server
import socketserver
import socket

from typing import Tuple
from http import HTTPStatus

class MyTCPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    @property
    def api_response(self):
        return json.dumps({"command": "python", "payload": True}).encode()

    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(self.api_response))

        elif self.path == '/users':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps([{}, {}, {}]).encode()))

        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.wfile.write(bytes(json.dumps({"command": "python", "payload": '404 Not Found'}).encode()))



if __name__ == "__main__":
    PORT = int(os.getenv('PORT')) or 8080
    server = MyTCPServer(("", PORT), Handler)
    print(f"Server started at http://localhost:{PORT}", flush=1)
    server.serve_forever()