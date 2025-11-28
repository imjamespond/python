import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

MODEL_PROVIDER = "openai"

BASE_URL_MD="https://api-inference.modelscope.cn/v1"
BASE_URL_BD="https://aistudio.baidu.com/llm/lmapi/v3"
BASE_URL_ZP="https://open.bigmodel.cn/api/paas/v4"
BASE_URL_CF="https://gateway.ai.cloudflare.com/v1/7b606aa2446b22c790782eaba9cf2ce8/aistudio/compat"
BASE_URL_OR="https://openrouter.ai/api/v1/"
BASE_URL_NV="https://integrate.api.nvidia.com/v1"

# ---------- 配置 ----------
# 直接初始化ChatOpenAI
LLM_BAIDU = init_chat_model(
    # model="ernie-4.5-21b-a3b" ,              # modelname: 指定模型名称
    model="ernie-4.5-turbo-128k-preview" , 
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("ERNIE_API_KEY"),      # apikey: 设置API密钥
    base_url=BASE_URL_BD,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.2,
    max_tokens=8192,
    timeout=30
)

LLM_QWEN = init_chat_model(
    # "Qwen/Qwen3-Next-80B-A3B-Instruct" 
    # model="Qwen/Qwen3-32B",   
    # model="Qwen/Qwen3-14B",
    model="Qwen/Qwen3-Coder-30B-A3B-Instruct",              
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("MODELSCOPE_API_KEY"),      # apikey: 设置API密钥
    base_url=BASE_URL_MD,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.1,
    max_tokens=8192,
    timeout=30,
    # https://www.dataleadsfuture.com/build-autogen-agents-with-qwen3-structured-output-thinking-mode/
    # Qwen3's extra_body parameters
    extra_body={
      "enable_thinking":False
    }
)

LLM_ZHIPU = init_chat_model(
    model="GLM-4.5-Flash", # 不能输出纯JSON！
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url=BASE_URL_ZP,  # apiurl: 设置基础URL
    # 其他可选参数
    temperature=0.7,
    max_tokens=8192,
    timeout=30,
    extra_body={
      "thinking":{
        "type":"disabled"
      }
    }
    
)

LLM_GEMINI = init_chat_model(
    model="google-ai-studio/gemini-2.5-flash-lite",  # 逻辑能力强
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("GM_API_KEY"),    
    base_url=BASE_URL_CF,  
    # 其他可选参数
    temperature=0.2,
    max_tokens=8192,
    timeout=30
)

LLM_OR = init_chat_model(
    # model="x-ai/grok-4.1-fast:free",      
    # model="tngtech/deepseek-r1t2-chimera:free",  
    model="openai/gpt-oss-20b:free",   
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("OR_API_KEY"),   
    base_url=BASE_URL_OR,  
    # 其他可选参数
    temperature=0.2,
    max_tokens=8192,
    timeout=30
)

# https://build.nvidia.com/search?q=text-generation
api_key_nv = os.getenv("NV_API_KEY")
LLM_NV2 = init_chat_model(
    model="qwen/qwen3-next-80b-a3b-instruct", # 生成json不错
    # model="qwen/qwen3-next-80b-a3b-thinking", too slow
    # model="deepseek-ai/deepseek-v3.1-terminus", not good
    # model="deepseek-ai/deepseek-v3.1", # 还行
    # model="moonshotai/kimi-k2-instruct-0905", # 较快
    # model="bytedance/seed-oss-36b-instruct", # 不错
    model_provider=MODEL_PROVIDER,
    api_key=api_key_nv,   
    base_url=BASE_URL_NV,  
    # 其他可选参数
    temperature=0.2,
    max_tokens=8192,
    timeout=60
)

LLM_NV1 = init_chat_model(
    model="nvidia/nvidia-nemotron-nano-9b-v2",    
    model_provider=MODEL_PROVIDER,
    api_key=api_key_nv,   
    base_url=BASE_URL_NV,  
    # 其他可选参数
    temperature=0.2,
    max_tokens=8192,
    timeout=30
)

LLM_OLLAMA = init_chat_model(
    model="modelscope.cn/unsloth/Qwen3-4B-Instruct-2507-GGUF:Q8", # 小模型一定要把input不能太大！！！否则会忽略很多细节，最好不超1倍，即4096。
    model_provider="ollama",
    api_key="",   
    # base_url=,  
    # 其他可选参数
    temperature=0.2,
    max_tokens=4096,
    timeout=30
)

LLM_TEXT = init_chat_model(
    model=os.getenv("TEXT_MODEL","qwen/qwen3-next-80b-a3b-instruct"), 
    model_provider=MODEL_PROVIDER,
    api_key=os.getenv("TEXT_API_KEY", api_key_nv),   
    base_url=os.getenv("TEXT_API_BASE", BASE_URL_NV),  
    temperature=0.2,
    timeout=60
)

LLM_JSON=LLM_QWEN
LLM_TOOLS=LLM_OLLAMA

PROMPT_PERSON = os.getenv("PROMPT_PERSON") or ""