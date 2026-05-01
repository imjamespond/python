```bash
uv venv --python 3.10
# cuda 11.8
uv pip install torch==2.6.0 torchaudio==2.6.0 torchvision==0.21 -f https://mirrors.aliyun.com/pytorch-wheels/cu118
uv pip install ultralytics dotenv
uv run python -c "import torch; print(torch.cuda.is_available())"
```

[yolo11n.pt](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt)  
[yolo-face](https://github.com/YapaLab/yolo-face/releases)  
[yolo-face](https://github.com/akanametov/yolo-face/releases)  
[deepface](https://github.com/serengil/deepface/blob/3897c8d23887d3ea4e66cff6b4291cf0ccf89b7e/deepface/models/face_detection/Yolo.py)  