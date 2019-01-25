import cv2
import numpy as np
from darknet import test

# retval = cv2.img_hash.ColorMomentHash_create()
# retval = cv2.img_hash.PHash_create()
retval = cv2.img_hash.BlockMeanHash_create()
# retval = cv2.img_hash.AverageHash_create()

# cap = cv2.VideoCapture('/Users/zyy/Downloads/tf_traffic_cut.mp4')
# while(1):
#   ret, frame = cap.read()
#   if(ret):
#     test()
#     # _hash = retval.compute(frame)
#     # print(_hash)
#   else:
#     break

img1 = "/Users/zyy/Downloads/1.png"
img2 = "/Users/zyy/Downloads/2.png"
rs1 = test(img1)
# rs2 = test(img2)

mat1 = cv2.imread(img1, cv2.IMREAD_COLOR)
# mat1 = cv2.resize(mat1, (2*width, 2*height), interpolation=cv2.INTER_CUBIC)
mat2 = cv2.imread(img2, cv2.IMREAD_COLOR)
# cv2.imshow('image', mat1)

# height, width = mat1.shape[:2]
# print(height, width)


def imghash(rs, ii):
    for i, confidence in enumerate(rs):
        # print(x[0].decode('utf-8'), x[1], x[2])
        pos = np.array(confidence[2]).astype(int)
        h = pos[3]
        w = pos[2]
        y = pos[1]-(h >> 1)
        x = pos[0]-(w >> 1)

        cv2.imwrite("./"+str(ii)+str(i)+".jpg", mat2[y:y+h, x:x+w])
        _hash = retval.compute(mat2[y:y+h, x:x+w])
        print(confidence[0].decode('utf-8'), pos, _hash)


# imghash(rs1,1)
# print('-----')
# imghash(rs2,2)

def track(rs):
    trackers = []
    for i, confidence in enumerate(rs):
        # print(confidence[0].decode('utf-8'), confidence[1], confidence[2])
        pos = np.array(confidence[2]).astype(int)
        h = pos[3]
        w = pos[2]
        y = pos[1]-(h >> 1)
        x = pos[0]-(w >> 1)
        tracker = cv2.TrackerKCF_create()
        tracker.init(mat2, (x, y, w, h))
        trackers.append(tracker)

    return trackers


for i, tracker in enumerate(track(rs1)):
    (success, box) = tracker.update(mat2)
    if success: 
        print(box)
        (x, y, w, h) = [int(v) for v in box]
        cv2.imwrite("./"+str(i)+".jpg", mat2[y:y+h, x:x+w])

cv2.waitKey(0)
cv2.destroyAllWindows()
