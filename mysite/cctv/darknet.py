import os
import time
from ctypes import *
import cv2
import threading

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

class COUNT_ARGS(Structure):
    _fields_ = [("net", c_void_p),
                ("metadata", POINTER(METADATA)),
                ("name", c_char_p),
                ("url", c_char_p),
                ("thresh", c_float),
                ("hier", c_float),
                ("map", POINTER(c_int)),
                ("relative", c_int),
                ("debug", c_bool),
                ("x1", c_float),("y1", c_float),("x2", c_float),("y2", c_float)]

LOCK_FUNC = CFUNCTYPE(c_void_p)
DETETC_FUNC = CFUNCTYPE(c_void_p, POINTER(DETECTION), c_int)
TRACK_FUNC = CFUNCTYPE(c_void_p, c_int,c_int,c_int,c_int)


COMMAND_DIR = os.getcwd() 

if 'CCTVLIB' in os.environ:
    libdarknet = CDLL(os.environ['CCTVLIB'] + "/libdarknet.so", RTLD_GLOBAL)
else:
    libdarknet = CDLL(COMMAND_DIR + "/darknet/libdarknet.so", RTLD_GLOBAL)

load_net = libdarknet.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_meta = libdarknet.get_metadata
load_meta.argtypes = [c_char_p]
load_meta.restype = METADATA

load_image = libdarknet.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

do_nms_obj = libdarknet.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = libdarknet.free_image
free_image.argtypes = [IMAGE]

if 'CCTVLIB' in os.environ:
    libcodechiev = CDLL(os.environ['CCTVLIB'] + "/libcodechiev.so", RTLD_GLOBAL)
else:
    libcodechiev = CDLL(COMMAND_DIR + "/detector/build/libcodechiev.so", RTLD_GLOBAL)

c_detect = libcodechiev.detect
c_detect.argtypes = [LOCK_FUNC, DETETC_FUNC, TRACK_FUNC, POINTER(COUNT_ARGS)] 


net = load_net((COMMAND_DIR + "/darknet/cfg/yolov3.cfg").encode('utf-8'),
                (COMMAND_DIR + "/darknet/yolov3.weights").encode('utf-8'), 0)
meta = load_meta((COMMAND_DIR + "/darknet/cfg/coco-1.data").encode('utf-8'))

threads = {}

lock = threading.Lock()
maplock = threading.Lock()

def _lock():
    lock.acquire(True, 60)

def _detect(cam, dets, num, nms=.45):

    if (nms): 
        do_nms_obj(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    # free_image(im)
    # free_detections(dets, num)

    # for x in res:
    #     print(x[0].decode('utf-8'), x[1], x[2])
    
    lock.release()

    maplock.acquire(True)
    # time.sleep(1.5) 
    if cam in threads and threads[cam]['running']:
        # print(cam, 'is running')
        maplock.release()
        return True
    else:
        print(cam, 'is not running')
        maplock.release()
        return False


def _track(t,b,l,r):
    print('on track t,b,l,r: ', t,b,l,r)

def detect(cam, url, x1, y1, x2, y2, on_track=_track, debug=False):
    print("box: ", x1, y1, x2, y2)

    t = threading.Thread(target=__detect__, args = (cam, url, x1, y1, x2, y2, on_track, debug))
    t.start() 

    threads[cam] = {'running': True, 'thread': t}

def __detect__(cam, url, x1, y1, x2, y2, on_track, debug):

    on_detect = lambda dets, num, nms=.45: _detect(cam, dets, num, nms)

    args = COUNT_ARGS(
        net=net, 
        meta=meta, 
        name=cam.encode('utf-8'),
        url=url.encode('utf-8'),  
        thresh=c_float(.5), 
        hier=c_float(.5), 
        map=None, 
        relative=0, 
        debug=True,
        x1=x1,y1=y1,x2=x2,y2=y2 )
    c_detect(LOCK_FUNC(_lock), DETETC_FUNC(on_detect), TRACK_FUNC(on_track), args)

    maplock.acquire(True)
    if cam in threads:
        t = threads[cam]
        del threads[cam]
        maplock.release()


# detect("rtsp://10.0.0.2:8080/video/h264".encode('utf-8'), _track)
# detect("foobar","/home/james/Downloads/tf_traffic_cut.mp4",.4,0,1,1)

