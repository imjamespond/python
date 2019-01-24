#https://github.com/abidrahmank/OpenCV2-Python-Tutorials/blob/435328569162104db9c14f718f4ba170d1206470/source/py_tutorials/py_video/py_meanshift/py_meanshift.rst

import numpy as np
import cv2

# cap = cv2.VideoCapture('slow.flv')
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # setup initial location of window
        # r, h, c, w = 250, 90, 400, 125  # simply hardcoded the values
        # track_window = (c, r, w, h)
        boundingbox = cv2.selectROI(
            "frame", frame, fromCenter=False, showCrosshair=True)
        print(boundingbox)  # x, y, w, h
        r, h, c, w = boundingbox[1], boundingbox[3], boundingbox[0], boundingbox[2]
        track_window = (c, r, w, h)
        break


# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)),
                   np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while(1):
    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)
        cv2.imshow('frame', img2)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg", img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()
