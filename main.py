import math
import os

import cv2
import detect
import traverse

count = 0
start_from = os.getenv("START_FROM")
started = False
output_file = open('output_file.txt', "a")

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
    if not file_path.suffix.lower() in [".jpg", ".png"]:
      return False
  
    file = str(file_path)
    if start_from:
      if start_from == file:
        started = True
      
      if not started:
        return True
       
       
    global count
    
    try:
      detect.detect_face(file, append_filepath)

      print(f"count{count}, i {i}, gap {gap}, next {next} ")

    except Exception as e:
      print(file, e)
      return False

    if count % 10 == 0:
        output_file.flush()

    return True

if __name__ == '__main__':
    img_path = os.getenv("IMG_PATH")
    traverse.traverse_files(img_path, run)
    output_file.close()
