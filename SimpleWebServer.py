from __future__ import print_function
import BaseHTTPServer, SimpleHTTPServer
import ssl
import sys, os
import argparse
import json
import logging
from threading import Thread

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--http_port', type=int, default=8000, help='Http Port')
parser.add_argument('--ws_port', type=int, default=9000, help='WebSocket Port')
#https://github.com/davisking/dlib-models checkout to see detail of each dlib model
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dir_path, "openface-master/models/dlib/shape_predictor_68_face_landmarks.dat"))
#http://cmusatyalab.github.io/openface/models-and-accuracies/ checkout to see detail of OpenFace neural network models 
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    #default='/Users/metasoft/Downloads/nn4.small2.3d.v1.t7')
                    default=os.path.join(dir_path, 'openface-master/models/openface/nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--cuda', action='store_true')
parser.add_argument('--width', type=int, default=320)
parser.add_argument('--height', type=int, default=200)
parser.add_argument('--verbose', action='store_true', default=True)
args = parser.parse_args()

'''Adopted from https://www.piware.de/2011/01/creating-an-https-server-in-python/'''

os.chdir('./web')

def http_srv(port):
  httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), SimpleHTTPServer.SimpleHTTPRequestHandler)
  httpd.socket = ssl.wrap_socket(httpd.socket, keyfile = 'key.pem', certfile='cert.pem', server_side=True)
  print('now serving tls http on port:', port)
  httpd.serve_forever()

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.internet import task, defer
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.python import log

import Handlers

class MyServerProtocol(WebSocketServerProtocol):
  def __init__(self):
    super(MyServerProtocol, self).__init__()

  def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))

  def onOpen(self):
      print("WebSocket connection open.")

  def onMessage(self, payload, isBinary):
    '''
    if isBinary:
        log.msg("Binary message received: {} bytes".format(len(payload)))
    else:
        log.msg("Text message received: {}".format(payload.decode('utf8')))
    '''
    raw = payload.decode('utf8')
    msg = json.loads(raw)
    result = {}
    if msg['type'] is None: 
        result['type'] = "error"
    else : 
      handler = getattr(Handlers, msg['type'])
      if handler is not None:
        result = handler(msg, self)
    self.sendMessage(json.dumps(result), isBinary)

  def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))

def start_websocket_server(reactor): 
  log.startLogging(sys.stdout)
  factory = WebSocketServerFactory()
  factory.protocol = MyServerProtocol
  ctx_factory = DefaultOpenSSLContextFactory('key.pem', 'cert.pem')
  reactor.listenSSL(args.ws_port, factory, ctx_factory)
  return defer.Deferred()

import ofTest
if __name__ == '__main__':
  faces = ['lennon-1.png','lennon-2.png']
  for f in faces:
    face_path = os.path.join(dir_path, "openface-master/images/examples-aligned", f)
    ofTest.initImgs(face_path, 'lennon')

  thread = Thread()
  thread.run = lambda: http_srv(int(args.http_port))
  thread.daemon = True
  thread.start()

  task.react(start_websocket_server)

  #thread.join()