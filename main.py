import math
import os
import cv2
import detect
import traverse
import config

count = 0
debug = os.getenv("DEBUG")
depth_max = config.depth_max
start_from = os.getenv("START_FROM")
started = False
# output_file = open('output_file.txt', "a", encoding='utf-8')
output_file = open('output_file.txt', "w", encoding='utf-8')  # 清空文件


def append_filepath(img_path, face_img):
    global count

    # 保存人脸图片
    # 计算子文件夹编号（每1000张图片一个文件夹）
    folder_num = math.floor(count / 1000)
    subfolder = os.path.join("crops", str(folder_num))

    # 如果子文件夹不存在，则创建
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    face_filename = os.path.join(subfolder, f"img{count}.jpg")
    cv2.imwrite(face_filename, face_img)

    # 输出图片路径
    output_file.write(img_path + "\n")

    count += 1


def run(file_path, i, gap, next):
    global count, started

    if not file_path.suffix.lower() in [".jpg", ".png"]:
        return False

    file_path_str = str(file_path)
    if start_from:
        if start_from == file_path_str:
            started = True

        if not started:
            return True

    if debug:
        print(file_path_str)
        return True

    has_face = False

    try:
        has_face = detect.detect_face(file_path_str, append_filepath)

        print(f"count{count}, i {i}, gap {gap}, next {next} ")

    except Exception as e:
        print(file_path_str, e)
        return False

    if count % 10 == 0:
        output_file.flush()

    return has_face


if __name__ == '__main__':
    traverse.traverse_files(config.root_path, run, depth_max=depth_max)
    output_file.close()
