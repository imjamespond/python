from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = "openai"

BASE_URL_MD="https://api-inference.modelscope.cn/v1"
BASE_URL_BD="https://aistudio.baidu.com/llm/lmapi/v3"
BASE_URL_ZP="https://open.bigmodel.cn/api/paas/v4"


# ---------- 配置 ----------
# 直接初始化ChatOpenAI
LLM_BD = init_chat_model(
    # model="ernie-4.5-21b-a3b" ,              # modelname: 指定模型名称
    model="ernie-4.5-turbo-128k-preview" , 
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("ERNIE_API_KEY"),      # apikey: 设置API密钥
    base_url=BASE_URL_BD,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.5,
    max_tokens=8192,
    timeout=30
)

LLM_QW = init_chat_model(
  #  "Qwen/Qwen3-Next-80B-A3B-Instruct" 
    model="Qwen/Qwen3-32B",              # modelname: 指定模型名称
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("MODELSCOPE_API_KEY"),      # apikey: 设置API密钥
    base_url=BASE_URL_MD,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.5,
    max_tokens=8192,
    timeout=30,
    # https://www.dataleadsfuture.com/build-autogen-agents-with-qwen3-structured-output-thinking-mode/
    # Qwen3's extra_body parameters
    extra_body={
      "enable_thinking":False
    }
)

LLM_ZP = init_chat_model(
    model="GLM-4.5-Flash",              # modelname: 指定模型名称
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("ZHIPUAI_API_KEY"),      # apikey: 设置API密钥
    base_url=BASE_URL_ZP,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.5,
    max_tokens=8192,
    timeout=30,
    extra_body={
      "thinking":{
        "type":"disabled"
      }
    }
    
)