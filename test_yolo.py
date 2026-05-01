import sys
import os
import cv2
from ultralytics import YOLO

import config

img_path = sys.argv[1]

# 自动下载 yolo11n.pt 预训练权重, 当前目录下读取
model = YOLO(config.model)

# 指定 GPU 推理（device=0 表示第一张卡，也可写 device="cuda"）
results = model.predict(img_path, device=config.device, conf=0.3)

# # 3. 获取预测结果并画图
# # results[0] 是第一张图的结果
# result = results[0]

# # 将检测到的框画在原图上
# annotated_frame = result.plot()

# 2. 读取原始图像
# image = cv2.imread(img_path)
# if image is None:
#     print(f"找不到图片: {img_path}")
#     sys.exit(0)
image = None

# 遍历检测到的物体
for i, result in enumerate(results):
    # result.show()
    # result.save_txt("test.txt")
    # result.save_crop("test", f"img{i}")
    print(result.verbose())
    image = result.orig_img
    boxes = result.boxes
    for j, box in enumerate(boxes):
        cls = int(box.cls[0])
        label = result.names[cls]
        print(f"检测到物体: cls {cls}, label {label}")
        # 获取左上角和右下角坐标
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # 从原图中裁剪人脸区域
        face_img = image[y1:y2, x1:x2]
        # 保存人脸图片
        face_filename = os.path.join("crops", f"img{i}{j}.jpg")
        cv2.imwrite(face_filename, face_img)
        print(f"保存人脸: {face_filename}")

        # 画出人脸区域（绿色粗框）
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# # 5. 保存最终画好的 image
# cv2.imwrite("result.jpg", image)


# 显示图片（按任意键关闭窗口）
cv2.imshow("YOLO Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
