import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("MODEL", "yolov11l-face.pt")
device = os.getenv("DEVICE", "cuda")

img_path = os.getenv("IMG_PATH")

depth_max = int(os.getenv("DEPTH_MAX", "-1"))
