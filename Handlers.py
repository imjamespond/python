def getResult(msg_, msg):
  return {'type': msg_['type'], 'msg': msg}

def foobar(msg, client):
  return getResult(msg, 'msg is foobar')

import ofTest
def FaceBoundingBox(msg, client):
  dataURL, identity = msg.get('dataURL',None), msg.get('identity',None)
  ofTest.faceBoundingBox(dataURL, identity, client)
  return getResult(msg, 'done')

def Train(msg, client):
  ofTest.train()
  return getResult(msg, 'done')

def TrainData(msg, client):
  dataURL, person = msg.get('dataURL',None), msg.get('person',None)
  ofTest.trainData(dataURL, person, client)
  return getResult(msg, 'done')

def TrackFaces(msg, client):
  dataURL = msg.get('dataURL',None)
  ofTest.trackFaces(dataURL, client)
  return getResult(msg, 'done')