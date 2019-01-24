#https://docs.opencv.org/3.4.5/d4/d93/group__img__hash.html
import cv2
# retval = cv2.img_hash.ColorMomentHash_create()
retval = cv2.img_hash.AverageHash_create()

cap = cv2.VideoCapture('/some.mp4')
while(1): 
  ret, frame = cap.read()
  if(ret):
    _hash = retval.compute(frame)
    print(_hash)
  else:
    break

