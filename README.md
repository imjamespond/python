```bash
uv venv --python 3.10
# cuda 11.2
uv pip install tensorflow==2.10.0 "numpy<2.0" chromadb==0.4.24
# mac
uv pip install tensorflow==2.13.0 chromadb==0.4.24 protobuf==3.20.3
uv pip install deepface tf-keras dotenv

uv pip show deepface  
```

## [deepface](https://github.com/serengil/deepface)
## [deepface_models](https://github.com/serengil/deepface_models/releases/download/v1.0/vgg_face_weights.h5)
to `$HOME\.deepface\weights\vgg_face_weights.h5`


WIN ENV PATH
- `%CUDA_PATH%\bin`
- `C:\dev\cuda11.2-cudnn8.1\bin`