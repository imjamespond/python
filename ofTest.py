# -*- coding: utf-8 -*-

import __main__
import openface
from PIL import Image
import numpy as np
import os
import time
import StringIO
import urllib
import base64
import json
import cv2
import imagehash
import matplotlib.pyplot as plt
from matplotlib import cm

from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.manifold import TSNE
from sklearn.svm import SVC

align = openface.AlignDlib(__main__.args.dlibFacePredictor)
net = openface.TorchNeuralNet(__main__.args.networkModel, 
  __main__.args.imgDim, cuda=__main__.args.cuda)

rep_ = None

class Face:

  def __init__(self, rep, identity):
    self.rep = rep
    self.identity = identity

  def __repr__(self):
    return "{{id: {}, rep[0:5]: {}}}".format(
        str(self.identity),
        self.rep[0:5]
    )

def processFrame(dataURL):
  head = "data:image/jpeg;base64,"
  assert(dataURL.startswith(head))
  imgdata = base64.b64decode(dataURL[len(head):])
  imgFile = StringIO.StringIO()
  imgFile.write(imgdata)
  imgFile.seek(0)
  img = Image.open(imgFile)

  buf = np.fliplr(np.asarray(img))
  rgbFrame = np.zeros((300, 400, 3), dtype=np.uint8) #构建像素数组
  rgbFrame[:, :, 0] = buf[:, :, 2]
  rgbFrame[:, :, 1] = buf[:, :, 1]
  rgbFrame[:, :, 2] = buf[:, :, 0]

  return rgbFrame, np.copy(buf)

def getBase64Image(rgbFrame):
  plt.figure()
  plt.imshow(rgbFrame)
  plt.xticks([])
  plt.yticks([])

  imgdata = StringIO.StringIO()
  plt.savefig(imgdata, format='png', bbox_inches='tight', pad_inches = 0)
  imgdata.seek(0)
  content = 'data:image/png;base64,' + \
      urllib.quote(base64.b64encode(imgdata.buf))
  
  plt.close()

  return content

def faceBoundingBox(dataURL, identity, client):

  rgbFrame, annotatedFrame = processFrame(dataURL)

  # cv2.imshow('frame', rgbFrame)
  # if cv2.waitKey(1) & 0xFF == ord('q'):
  #   return

  bb = align.getLargestFaceBoundingBox(rgbFrame)
  bbs = [bb] if bb is not None else []
  #bbs = align.getAllFaceBoundingBoxes(rgbFrame)
  print(len(bbs))
  for bb in bbs:
    bl = (bb.left(), bb.bottom())
    tr = (bb.right(), bb.top())
    cv2.rectangle(annotatedFrame, bl, tr, color=(153, 255, 204), thickness=2)

    #for p in openface.AlignDlib.OUTER_EYES_AND_NOSE:
    #cv2.circle(annotatedFrame, center=landmarks[p], radius=3, color=(102, 204, 255), thickness=-1)

    # `img` is a numpy matrix containing the RGB pixels of the image.
    alignedFace = align.align(__main__.args.imgDim, rgbFrame, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

    if alignedFace is None:
      continue

    rep = net.forward(alignedFace) 
    #if(rep is not None):
    #  compareLast(rep)
    inferWhom(rep, client)

  content = getBase64Image(annotatedFrame)
  msg = {
      "type": "ANNOTATED",
      "content": content
  }
  client.sendMessage(json.dumps(msg))


def compareLast(rep):
  global rep_
  if rep_ is not None:
    d = rep - rep_
    distance = np.dot(d, d)
    print(distance)
  rep_ = rep

svm = None
people = []
images = {}

def initImgs(imgPath, person):
  bgrImg = cv2.imread(imgPath)
  if bgrImg is None:
      raise Exception("Unable to load image: {}".format(imgPath))
  rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
  if __main__.args.verbose:
      print("  + Original size: {}".format(rgbImg.shape))
  start = time.time()
  rep = net.forward(rgbImg)
  if __main__.args.verbose:
      print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
      print("Representation:")
      print(rep)
      print("-----\n")
  
  if person not in people:
    people.append(person) 
  images[hash(imgPath)] = Face(rep, len(people))

def getData():
  X = []
  y = []
  for img in images.values():
    X.append(img.rep)
    y.append(img.identity)
  X = np.vstack(X)
  y = np.array(y)
  return (X, y)

def trainData(dataURL, person, client):
  if person not in people:
    people.append(person) 

  rgbFrame, annotatedFrame = processFrame(dataURL)
  bb = align.getLargestFaceBoundingBox(rgbFrame)
  bbs = [bb] if bb is not None else [] 
  print(len(bbs))
  for bb in bbs:
    bl = (bb.left(), bb.bottom())
    tr = (bb.right(), bb.top())
    cv2.rectangle(annotatedFrame, bl, tr, color=(153, 255, 204), thickness=2)
  
    alignedFace = align.align(__main__.args.imgDim, rgbFrame, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
      continue

    phash = str(imagehash.phash(Image.fromarray(alignedFace)))#Returns An image object
    print(phash)#find_similar_images 
    if phash in images:
        identity = images[phash].identity
        print("phash: {}".format(phash))
        pass
    else: 
      rep = net.forward(alignedFace) 
      images[phash] = Face(rep, len(people))
    
  content = getBase64Image(annotatedFrame)
  msg = {
      "type": "ANNOTATED",
      "content": content
  }
  client.sendMessage(json.dumps(msg))

from sklearn.externals import joblib
svmpkl = 'svm.pkl.gz'
labels = 'labels.gz'
try:
  svm = joblib.load(svmpkl)
  people = joblib.load(labels)
  pass
except:
  pass
def train():
  global svm
  print("+ Training SVM on {} labeled images.".format(len(images)))
  d = getData()
  if d is None:
      svm = None
      return
  else:
      (X, y) = d
  param_grid = [
      {'C': [1, 10, 100, 1000],
        'kernel': ['linear']},
      {'C': [1, 10, 100, 1000],
        'gamma': [0.001, 0.0001],
        'kernel': ['rbf']}
  ] 
  svm = GridSearchCV(SVC(C=1, probability=True), param_grid, cv=5)
  svm.fit(X, y)
  joblib.dump(svm, svmpkl, compress=True) 
  joblib.dump(people, labels, compress=True) 

def inferWhom(rep, client):
  start = time.time()
  #predictions = clf.predict_proba(rep).ravel()
  # print (predictions)
  #maxI = np.argmax(predictions)
  # max2 = np.argsort(predictions)[-3:][::-1][1]
  #persons.append(le.inverse_transform(maxI))
  # print (str(le.inverse_transform(max2)) + ": "+str( predictions [max2]))
  # ^ prints the second prediction
  #confidences.append(predictions[maxI])
  identity = -1
  if len(people) == 0:
    identity = -1
  elif len(people) == 1:
    identity = 0
  elif svm: 
    reshaped = np.array(rep).reshape((1, -1))
    #identity = svm.predict(reshaped)[0]
    predictions = svm.predict_proba(reshaped).ravel()
    client.sendMessage(json.dumps( {
        "type": "INFER",
        #"person": people[identity-1]
        "predictions": dict([(people[i], val) for i,val in enumerate(predictions.tolist())])
    })) 
    

  if __main__.args.verbose:
    print("Prediction took {} seconds, identity: {}."
      .format(time.time() - start, identity))
    pass


import dlib
class Tracker:

    def __init__(self, img, bb, rep):
        self.t = dlib.correlation_tracker()
        self.t.start_track(img, bb)
        self.rep = rep
        self.bb = bb
        self.pings = 0

    def updateRep(self, rep):
        self.pings = 0
        alpha = 0.9
        self.rep = alpha * self.rep + (1. - alpha) * rep
        return self.rep

    def overlap(self, bb):
        p = float(self.bb.intersect(bb).area()) / float(self.bb.area())
        return p > 0.3

    def ping(self):
        self.pings += 1

trackers = []

def trackFaces(dataURL, client):
  rgbFrame, annotatedFrame = processFrame(dataURL)
  #ret, frame = video_capture.read()
  #frame = cv2.flip(frame, 1)
  #frameSmall = cv2.resize(frame, (int(__main__.args.width),
                                #int(__main__.args.height)))

  bbs = align.getAllFaceBoundingBoxes(rgbFrame)
  pts, clrs = [], []
  for i, bb in enumerate(bbs):
    #cv2.rectangle(annotatedFrame, bl, tr, color=(153, 255, 204), thickness=2)
 
    alignedFace = align.align(96, rgbFrame, bb,
                              landmarkIndices=openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
    if alignedFace is None:
      continue

    rep = net.forward(alignedFace) 

    center = bb.center()
    centerI = 0.7 * center.x * center.y / (400* 300)
    color_np = cm.Set1(centerI)
    color_cv = list(np.multiply(color_np[:3], 255))

    bl = (bb.left(), bb.bottom())
    tr = (bb.right(), bb.top())
    cv2.rectangle(annotatedFrame, bl, tr, color=color_cv, thickness=3)

    tracked = False
    for i in xrange(len(trackers) - 1, -1, -1):
        t = trackers[i]
        t.t.update(annotatedFrame)
        if t.overlap(bb):
            rep = t.updateRep(rep)
            pts.append(rep)
            clrs.append(color_cv)
            tracked = True
            break
        print("tracked: {}".format(tracked))

    if not tracked:
        trackers.append(Tracker(annotatedFrame, bb, rep))
        pts.append(rep)
        clrs.append(color_cv)

  for i in xrange(len(trackers) - 1, -1, -1):
      t = trackers[i]
      t.ping()
      if t.pings > 10:
          del trackers[i]
          continue

      for j in range(i):
          if t.t.get_position().intersect(trackers[j].t.get_position()).area() / \
              t.t.get_position().area() > 0.4:
              del trackers[i]
              continue

  content = getBase64Image(annotatedFrame)
  msg = {
      "type": "ANNOTATED",
      "content": content
  }
  client.sendMessage(json.dumps(msg))
