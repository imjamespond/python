import os

from numpy import ndarray
from ultralytics import YOLO
from typing import Callable

import config

max_face_num = int(os.getenv("MAX_FACE_NUM", "3"))
conf = float(os.getenv("CONFIDENCE", "0.7"))

model = YOLO(config.model)
def detect_face(img_path: str, callback: Callable[[str, ndarray], None]) -> bool:
  has_face = False
  results = model.predict(img_path, device=config.device, conf=conf)
  for result in results:
    # result.save_crop("crops", img_file)
    image = result.orig_img
    boxes = result.boxes
    for i, box in enumerate(boxes):
        if i >= max_face_num:
            break
        has_face = True
        # cls = int(box.cls[0])
        # label = result.names[cls]
        # 获取左上角和右下角坐标
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # 从原图中裁剪人脸区域
        face_img = image[y1:y2, x1:x2]

        callback(img_path, face_img)
    
  return has_face