import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("MODEL", "yolov11l-face.pt")
device = os.getenv("DEVICE", "cuda")