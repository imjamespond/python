import math
import os

import chroma
import config

config.config_gpu()

filelist = os.getenv("FILELIST")
crops_path = os.getenv("CROPS_PATH")

if __name__ == '__main__':
    with open(filelist, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=0):          # 逐行流式读取，内存友好
            path = line.strip()  # 去掉换行符和首尾空白

            folder_num = math.floor(i / 1000)
            subfolder = os.path.join(crops_path, str(folder_num))

            face_filename = os.path.join(subfolder, f"img{i}.jpg")
            print(i, path, face_filename)

            chroma.save_embeding(face_filename, path)
