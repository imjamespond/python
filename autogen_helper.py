import os
from autogen_ext.models.openai import OpenAIChatCompletionClient

import models
# ================================
# 创建一个 model_client 的工厂函数
# 返回一个实现 ChatCompletionClient 协议的实例
# ================================


def extractor_model_client(model: str = "qwen/qwen3-next-80b-a3b-instruct"):
    """
    示例使用 OpenAI 兼容的客户端。若使用 Azure/其他，请替换为相应的实现类。
    需要安装 extras： pip install "autogen-ext[openai]"
    """
    family = os.getenv("MODEL_TYPE", "qwen")
    api_key = os.getenv("TEXT_API_KEY", models.API_KEY_NV)
    # 可选：用于自定义 OpenAI 兼容 endpoint
    base_url = os.getenv("TEXT_API_BASE", models.BASE_URL_NV)
    # create_args = _create_args_from_config(copied_args)
    # create_args = {k: v for k, v in config.items() if k in create_kwargs}
    """ 
    说明能读取extra_body键
    create_kwargs = set(completion_create_params.CompletionCreateParamsBase.__annotations__.keys()) | set(
        ("timeout", "stream", "extra_body")
    ) 
    """
    return OpenAIChatCompletionClient(model=os.getenv("TEXT_MODEL", model), api_key=api_key, base_url=base_url, extra_body={
        # "enable_thinking": False
    }, model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": family,
        "structured_output": True,
    })


def analyze_model_client():

    api_key = models.API_KEY_NV
    base_url = models.BASE_URL_NV

    return OpenAIChatCompletionClient(model="qwen/qwen3-next-80b-a3b-instruct", api_key=api_key, base_url=base_url, extra_body={
    }, model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "qwen3",
        "structured_output": True,
    })
