import contextlib
import socket
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from probe import probe

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')
    def log_message(self,*args):
        pass

class RecoveryDrill(unittest.TestCase):
    def test_local_success_failure_and_recovery(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        port=server.server_port
        worker=threading.Thread(target=server.serve_forever);worker.start()
        url='http://127.0.0.1:'+str(port)
        try:
            self.assertTrue(probe(url,1)['ok'])
        finally:
            server.shutdown();server.server_close();worker.join()
        with socket.socket() as reservation:
            reservation.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            reservation.bind(('127.0.0.1',port))
            self.assertFalse(probe(url,0.2)['ok'])
        recovered=ThreadingHTTPServer(('127.0.0.1',port),Handler)
        worker=threading.Thread(target=recovered.serve_forever);worker.start()
        try:
            self.assertTrue(probe(url,1)['ok'])
        finally:
            recovered.shutdown();recovered.server_close();worker.join()
