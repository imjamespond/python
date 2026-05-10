import os
import csv
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("MODEL", "yolov11l-face.pt")
device = os.getenv("DEVICE", "cuda")

img_path = os.getenv("IMG_PATH")

depth_max = int(os.getenv("DEPTH_MAX", "-1"))

# 根目录
root_path = os.getenv("ROOT_PATH")
def getenv_list(name):
    envstr = os.getenv(name)
    # return None if envstr == None else envstr.split(",")

    if envstr is None:
        return None
    reader = csv.reader([envstr])
    result = next(reader)
    return [item.strip() for item in result]
