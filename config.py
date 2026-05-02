import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("MODEL", "yolov11l-face.pt")
device = os.getenv("DEVICE", "cuda")

img_path = os.getenv("IMG_PATH")
gap_max = int( os.getenv("GAP_MAX", "100") )
gap_step = int( os.getenv("GAP_STEP", "1") )
depth_max = int( os.getenv("DEPTH_MAX", "-1") )