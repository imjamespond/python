import os
import time
from ctypes import *
import cv2

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


DETETC_FUNC = CFUNCTYPE(c_void_p, POINTER(DETECTION), c_int)


DARKNET_DIR = os.getcwd()

libdarknet = CDLL(DARKNET_DIR + "/darknet/libdarknet.so", RTLD_GLOBAL)

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

# free_detections = libdarknet.free_detections
# free_detections.argtypes = [POINTER(DETECTION), c_int]

free_image = libdarknet.free_image
free_image.argtypes = [IMAGE]

libcodechiev = CDLL(DARKNET_DIR + "/build/libcodechiev.so", RTLD_GLOBAL)
predict_image = libcodechiev.predict_image
predict_image.argtypes = [DETETC_FUNC, c_void_p, IMAGE, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)] 
predict_image.restype = POINTER(DETECTION)

test = libcodechiev.test
test.argtypes = [DETETC_FUNC, c_void_p, POINTER(METADATA), c_char_p, c_float, c_float, POINTER(c_int), c_int] 

# test_callback = libcodechiev.test_callback
# test_callback.argtypes = [CFUNCTYPE(c_void_p, c_char_p)]

net = load_net((DARKNET_DIR + "/darknet/cfg/yolov3.cfg").encode('utf-8'),
                (DARKNET_DIR + "/darknet/yolov3.weights").encode('utf-8'), 0)
meta = load_meta((DARKNET_DIR + "/darknet/cfg/coco-1.data").encode('utf-8'))

def predict(im, thresh=.5, hier_thresh=.5):
    num = c_int(0)
    pnum = pointer(num)

    dets = predict_image(DETETC_FUNC(detect), net, im, im.w, im.h, c_float(thresh), c_float(hier_thresh), None, 0, pnum)

def detect(dets, num, nms=.45):

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

    for x in res:
        print(x[0].decode('utf-8'), x[1], x[2])

    time.sleep(.5)


# img = load_image((DARKNET_DIR + "/darknet/data/dog.jpg").encode('utf-8'), 0, 0)
# r = predict(img)
# free_image(img)

# test("rtsp://10.0.0.2:8080/video/h264".encode('utf-8'))
test(DETETC_FUNC(detect), net, meta,"/home/james/Downloads/tf_traffic_cut.mp4".encode('utf-8'), c_float(.5), c_float(.5), None, 0)

# world = "world"
# def hello(hello):
#     print(hello.decode('utf-8') +" "+world)

# FUNC = CFUNCTYPE(c_void_p, c_char_p)
# test_callback(FUNC(hello))