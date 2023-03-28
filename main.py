from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

import json
from service import Service

from utils.db import Db
 
host = ('localhost', 8888)
svc = Service()

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        url = urlparse(self.path) 
        path = url.path
        query = parse_qs(url.query)
        print(path,query)
        
        result = None
        if path == "/ip/get_result":
            result = svc.get_result(query)
        elif path == "/ip/read_result":
            result = svc.read_result()
        elif path == "/ip/clear_result":
            result = svc.clear_result()
        elif path == "/ip/total_result":
            result = svc.total()
            
        self.wfile.write(json.dumps(result).encode())

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))

        print('headers', self.headers)
        print("do post:", self.path, self.client_address, datas)

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
    print("Stop server")
    svc.db.close()

