import json
from langchain_core.messages import HumanMessage, SystemMessage

import models

def getJSON(json_data: str, retry_count: int = 0):
  try:
    return json.loads(json_data.replace("```json\n", "").replace("```\n", "").replace("```", "").strip())
     
  except:
    if retry_count >= 2:
      raise Exception("JSON解析失败，已重试2次")
    
    print(f"修复JSON (第{retry_count + 1}次尝试)")
    messages = [
    SystemMessage(content="修复JSON,你必须只返回纯 JSON，不允许出现任何 Markdown、代码块、反引号或额外说明。输出必须可被 JSON 解析器直接解析。"),
    HumanMessage(content=json_data)
]
    full_content = ""
    for chunk in models.LLM_JSON.stream(messages):
      chunk_text = ""
      if hasattr(chunk, 'content'):
        chunk_text = str(chunk.content)
        print(chunk_text, end="")
      elif hasattr(chunk, 'text'):
        chunk_text = str(chunk.text)
        print(chunk_text, end="")
      full_content += chunk_text
    
    try:
      return json.loads(full_content)
    except:
      return getJSON(full_content, retry_count + 1)



if __name__ == "__main__":
    # Test cases for the recursive JSON parsing
    test_cases = [
        # Valid JSON
        '{"name": "test", "value": 123}',
        
        # JSON with markdown formatting
        '```json\n{"name": "test", "value": 123}\n```',
        
        # Malformed JSON that needs repair
        '{"name": "test", "value": 123,}',  # Extra comma
        
        # More complex malformed JSON
        '{"users": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30,}]}',  # Extra comma in nested array
        
        # Completely broken JSON
        '{name: "test", value: 123}',  # Missing quotes around keys
    ]
    
    print("=== 测试递归JSON解析功能 ===\n")
    
    for i, test_json in enumerate(test_cases, 1):
        print(f"测试用例 {i}:")
        print(f"输入: {test_json}")
        
        try:
            result = getJSON(test_json)
            print(f"✅ 成功解析: {result}")
        except Exception as e:
            print(f"❌ 解析失败: {e}")
        
        print("-" * 50)