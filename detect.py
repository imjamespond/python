from numpy import ndarray
from ultralytics import YOLO
from typing import Callable

import config

model = YOLO(config.model)
def detect_face(img_path: str, callback: Callable[[str, ndarray], None]):
  results = model.predict(img_path, device=config.device, conf=0.3)
  for result in results:
    # result.save_crop("crops", img_file)
    image = result.orig_img
    boxes = result.boxes
    for box in boxes:
        # cls = int(box.cls[0])
        # label = result.names[cls]
        # 获取左上角和右下角坐标
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # 从原图中裁剪人脸区域
        face_img = image[y1:y2, x1:x2]

        callback(img_path, face_img)