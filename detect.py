from ultralytics import YOLO
from typing import Callable
import os
import cv2
import math
import config

model = YOLO(config.model)
def detect_face(img_path: str, count: int, callback: Callable[[str], None]):
  results = model.predict(img_path, device=config.device, conf=0.3)
  for result in results:
    # img_file = f"img{count}"
    # result.save_crop("crops", img_file)
    image = result.orig_img
    boxes = result.boxes
    for i, box in enumerate(boxes):
        cls = int(box.cls[0])
        label = result.names[cls]
        # 获取左上角和右下角坐标
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # 从原图中裁剪人脸区域
        face_img = image[y1:y2, x1:x2]

        # 保存人脸图片
        # 计算子文件夹编号（每1000张图片一个文件夹）
        folder_num = math.floor(count / 1000)
        subfolder = os.path.join("crops", str(folder_num))

        # 如果子文件夹不存在，则创建
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        face_filename = os.path.join(subfolder, f"img{count}-{i}.jpg")
        cv2.imwrite(face_filename, face_img)

        callback(img_path)