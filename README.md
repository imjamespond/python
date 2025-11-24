```
uv venv --python 3.10
source .venv/bin/activate
uv pip install modelscope transformers torch
modelscope download --model Qwen/Qwen3-Reranker-0.6B
modelscope download --model Qwen/Qwen3-Embedding-0.6B
```