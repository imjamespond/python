import os
from autogen_ext.models.openai import OpenAIChatCompletionClient

import models
# ================================
# 创建一个 model_client 的工厂函数
# 返回一个实现 ChatCompletionClient 协议的实例
# ================================


def make_model_client(model: str = "qwen/qwen3-next-80b-a3b-instruct"):
    """
    示例使用 OpenAI 兼容的客户端。若使用 Azure/其他，请替换为相应的实现类。
    需要安装 extras： pip install "autogen-ext[openai]"
    """
    api_key = os.getenv("TEXT_API_KEY", models.API_KEY_NV)
    # 可选：用于自定义 OpenAI 兼容 endpoint
    base_url = os.getenv("TEXT_API_BASE", models.BASE_URL_NV)
    return OpenAIChatCompletionClient(model=os.getenv("TEXT_MODEL", model), api_key=api_key, base_url=base_url, model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen3",
        "structured_output": True,

    })

