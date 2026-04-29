import cv2
from deepface import DeepFace

import resize


def test1(img_path: str, detector: str, align=True):
    # 提取人脸
    faces = DeepFace.extract_faces(
        img_path=img_path, detector_backend=detector, align=align)

    # ==============================================================
    # 方式一：在原图上用矩形框出人脸并显示 (推荐，最直观)
    # ==============================================================
    img_bgr = cv2.imread(img_path)

    for face in faces:
        # 获取人脸区域坐标
        facial_area = face["facial_area"]
        x = facial_area["x"]
        y = facial_area["y"]
        w = facial_area["w"]
        h = facial_area["h"]

        # 在原图上画蓝色矩形框
        cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Original Image with Faces", img_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test2(img_path: str, detector: str, align=True):
    risized_img = resize.resize_to_width(img_path)
    # 提取人脸
    faces = DeepFace.extract_faces(
        img_path=risized_img, detector_backend=detector, align=align)

    # ==============================================================
    # 方式二：将提取出的“干净人脸”单独显示出来
    # ==============================================================
    for i, face in enumerate(faces):
        # 1. 获取人脸图像数据 (此时可能是 float64)
        face_img_rgb = face["face"]

        # 关键修复：先将数据类型转为 float32 (cv2.COLOR_RGB2BGR 不支持 float64)
        face_img_rgb = face_img_rgb.astype("float32")

        # 2. 颜色通道从 RGB 转换为 BGR
        face_img_bgr = cv2.cvtColor(face_img_rgb, cv2.COLOR_RGB2BGR)

        # 3. 像素值从 0~1.0 转换为 0~255，并转为 uint8
        face_img_bgr = (face_img_bgr * 255).astype("uint8")

        save_filename = f"img_{i}.jpg"
        cv2.imwrite(save_filename, face_img_bgr)

        # 显示提取出的人脸
        cv2.imshow(f"Extracted Face {i+1}", face_img_bgr)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test3(img_path: str):
    for i in range(1000):
        try:
            embeddings = DeepFace.represent(
                img_path, detector_backend='skip', align=True)
            print(i, embeddings[0]['embedding'][:100])
        except Exception as e:
            print(i, e)



if __name__ == '__main__':
    # import sys
    # import config
    # if len(sys.argv) < 2:
    #     sys.exit(1)
    # file_path = sys.argv[1]
    # test2(file_path, config.detector_backend, True)

    test3("./img_0.jpg")
