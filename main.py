
import re
import sys
import asyncio

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
import agent_tools
import models
import tmp

CHUNK_SIZE = 4096


# ---------- Step 1: 小说分片 ----------


# ---------- Step 2: AI分析 ----------

def analyze_chunk(text_chunk):
    print(len(text_chunk))
    messages = [
    SystemMessage(content="你是一个专业的小说分析器，严格专注于提取片段中的核心要素：主要人物、关键事件和核心关系。忽略所有次要人物、事件和物件。"),
    HumanMessage(content=f"""
    请分析以下小说片段：
    {text_chunk}

    提取核心内容，并以**严格 JSON 格式**输出，仅包含以下字段：

    - **characters**: 主要人物列表（每个对象包含）：
      - `name`: 人物姓名
      - `description`: 1-2 句简要身份或性格描述（仅限关键人物）

    - **events**: 关键事件列表（每个对象包含）：
      - `description`: 一句话概括事件
      - `time`: 事件时间（未明确则设为 null）
      - `location`: 事件地点（未明确则设为 null）
      - `participants`: 参与事件的主要人物姓名列表

    - **relationships**: 核心关系列表（每个对象包含）：
      - `source`: 关系起始人物姓名
      - `target`: 关系目标人物姓名
      - `type`: 关系类型（如朋友、敌人、亲属、合作等）
      - `event`: 关联的主要事件描述（如无则省略或设为 null）

    **要求：**
    - 仅输出纯 JSON，无需任何额外说明、注释或文本。
    - 严格基于片段内容，避免推断或添加信息。
    - 忽略次要细节，仅保留最核心要素。
    """)
]
    # response = llm.invoke(messages)
    # content = response.content
    # return content
    full = None 
    for chunk in models.LLM_ZP.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text)
    return full.text
    # try:
    #     return json.loads(content)
    # except Exception as e:
    #     print("JSON解析失败:", e)
    #     return None

# ---------- Step 3: 调用 MCP Server ----------
async def send_to_mcp(json_data):
    print(len(json_data))


    # 获取工具并创建代理
    all_tools = await agent_tools.client.get_tools()
    # print(f"所有可用工具: {[tool.name for tool in all_tools]}")
    selected_tools = [
        tool for tool in all_tools 
        if tool.name in ['create_memory','update_memory', 'search_memories', 'create_connection', 'update_connection']
    ]
    # print(selected_tools)
    graph = create_agent(
        models.LLM_QW,
        selected_tools,
        system_prompt = """你是一个专业的记忆管理助手，负责处理与人物或其他实体相关的记忆操作，包括搜索、创建和更新。

## 核心工作流程

### 1. 创建记忆（严格流程）
- **创建 person 类型节点时**：
  - **必须首先调用** `search_memories` 对 `name` 字段进行搜索
  - **搜索结果处理**：
    - 无相关记录 → 调用 `create_memory` 创建新记忆
    - 已有相关记录 → 调用 `update_memory` 更新现有记忆
- **创建非 person 类型节点时**：可直接调用 `create_memory`

### 2. 更新记忆
- 直接调用 `search_memories` 查找目标记忆
- 确认存在后调用 `update_memory` 进行更新

### 3. 搜索记忆
- 用户仅要求查找时，直接使用 `search_memories`

### 4. 创建关联
- 使用相关工具创建记忆间关联
- **前提**：确保关联双方记忆均已存在（不确定时先搜索验证）

## 重要原则
- **🛑 禁止假设**：创建 person 节点时永远不要假设记忆不存在，必须通过搜索验证
- **🎯 类型区分**：仅 person 类型节点需要先搜索，其他类型可直接创建
- **🔄 严格执行**：person 节点必须遵循 搜索 → 创建/更新 的调用顺序
- **📝 保持一致性**：确保记忆准确性、一致性及 person 名称唯一性

请严格依据用户请求和节点类型，按照上述流程选择并调用正确的工具。""",
    )
    inputs = {"messages": [{"role": "user", "content": json_data}]}
    async for chunk in graph.astream(inputs, stream_mode="messages"):
        print(chunk)
        await asyncio.sleep(15)
    # rs = await asyncio.create_task(graph.ainvoke(inputs,stream_mode="messages")) 
    # print(rs)

# ---------- Step 4: 主流程 ----------
def process_novel_by_chapter(file_path):
    for chapter_title, chapter_text in chapter_stream(file_path):
        if len(chapter_text) > CHUNK_SIZE + 2000:
          chunks = []
          # 分块策略：每1000字
          for i in range(0, len(chapter_text), CHUNK_SIZE):
              chunk = chapter_text[i:i+CHUNK_SIZE]
              chunks.append(chunk)
        else:
          chunks = [chapter_text]
        
        # 然后处理 chunks 列表
        print(f"处理章节：{chapter_title}, chunks: {len(chunks)}")
        for chunk in chunks:
          analysis = analyze_chunk(chunk)  # 上面定义的分析函数
          if analysis:
              result = asyncio.run(send_to_mcp(analysis))  # 上面定义的 MCP 发送函数
              asyncio.sleep(10)
              print(f"MCP 返回：{result}")



def chapter_stream(file_path):
    """
    按章节流式读取小说，每次返回一个章节文本。
    假设章节以 '第X章' 开头
    """
    chapter_pattern = re.compile(r'(第.*章.*)')
    current_chapter = []
    chapter_title = None
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # 跳过空行
            match = chapter_pattern.match(line)
            if match:
                
                # 遇到新章节，先返回上一章
                if current_chapter:
                    if count > 2: # start from n+1 
                      yield chapter_title, "\n".join(current_chapter)
                    current_chapter = []
                
                chapter_title = line
             
                count += 1
                if count > 5: # end with n
                  break

            else:
                current_chapter.append(line)
        # 返回最后一章
        if current_chapter:
            yield chapter_title, "\n".join(current_chapter)

# ---------- 示例 ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供小说文件路径作为第一个参数")
        sys.exit(1)
    file_path = sys.argv[1]
    process_novel_by_chapter(file_path)
    # asyncio.run(send_to_mcp(tmp.JSON))

