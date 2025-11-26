import json
from langchain_core.messages import HumanMessage, SystemMessage

import models

def getJSON(json_data: str):
  try:
    return json.loads(json_data)
     
  except:
    print("修复JSON")
    messages = [
    SystemMessage(content="修复JSON,你必须只返回纯 JSON，不允许出现任何 Markdown、代码块、反引号或额外说明。输出必须可被 JSON 解析器直接解析。"),
    HumanMessage(content=json_data)
]
    full = None
    for chunk in models.LLM_QWEN.stream(messages):
      full = chunk if full is None else full + chunk
      print(chunk.text, end="")
    return json.loads(full.content)