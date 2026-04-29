import sys

import cv2
from ultralytics import YOLO

img_path = "e:/temp/covers/IMG_349-gigapixel-hq-scale-8_00x_Nero AI_Photo_Face.jpeg"

# 自动下载 yolo11n.pt 预训练权重, 当前目录下读取
model = YOLO("yolov11l-face.pt")

# 指定 GPU 推理（device=0 表示第一张卡，也可写 device="cuda"）
results = model.predict(img_path, device=0, conf=0.3)

# # 3. 获取预测结果并画图
# # results[0] 是第一张图的结果
# result = results[0]

# # 将检测到的框画在原图上
# annotated_frame = result.plot()

# # 保存结果
# cv2.imwrite("result.jpg", annotated_frame)

# # 2. 读取原始图像
# image = cv2.imread(img_path)
# if image is None:
#     print(f"找不到图片: {img_path}")
#     sys.exit(0)


# 遍历检测到的物体
for result in results:
    # result.show()
    result.save_txt("result.txt")
    result.save_crop("crop", "output")
    print(result.verbose())
    # boxes = result.boxes
    # for box in boxes:
    #     cls = int(box.cls[0])
    #     label = result.names[cls]
    #     print(f"检测到物体: {cls} {label}")
    #     # 获取左上角和右下角坐标
    #     x1, y1, x2, y2 = map(int, box.xyxy[0])
    #     # 画出人脸区域（绿色粗框）
    #     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    #     cv2.putText(image, label, (x1, y1 - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


# # 5. 保存最终画好的 image
# cv2.imwrite("result.jpg", image)


# # 显示图片（按任意键关闭窗口）
# cv2.imshow("YOLO Face Detection", annotated_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
