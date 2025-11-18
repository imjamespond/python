
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
    SystemMessage(content="你是一个小说分析器，只提取主要人物、主要事件和核心关系。忽略次要人物、次要事件与物件。"),
    HumanMessage(content=f"""
请分析以下小说片段：
{text_chunk}

请只抓取最重要的内容，并以**严格 JSON** 格式输出，包含以下字段：

1. characters: 主要人物列表，每个对象包含：
    - name: 人物名字
    - description: 1–2 句简要说明其身份或性格（仅主要人物）

2. events: 主要事件列表，每个对象包含：
    - description: 用一句话概括该片段中最重要的事件
    - time: 若文本未明确则写 null
    - location: 若文本未明确则写 null
    - participants: 参与该主要事件的主要人物名字列表

3. relationships: 主要人物之间的核心关系，每个对象包含：
    - source: 人物名字
    - target: 人物名字
    - type: 关系类型（如朋友、敌人、亲属、合作等）
    - event: 相关联的主要事件描述（如适用）

请严格按照 JSON 输出，不要添加任何额外说明或文本。
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
        system_prompt= """你是一个记忆管理助手，负责处理与人物或其他对象相关的记忆的搜索、创建与更新。

核心工作规则：

1. **所有创建操作必须先搜索**
   - 当用户请求创建某个记忆（特别是人物记忆）时，你必须先调用 `search_memories`。
   - 若该记忆与人物相关，你必须优先使用人物的 **name 字段** 进行搜索。

2. **搜索后的行动逻辑**
   - 如果搜索结果显示该记忆不存在：使用 `create_memory` 创建新记忆。
   - 如果搜索结果显示该记忆已存在：使用 `update_memory` 更新该记忆，而不是再次创建。

3. **更新请求**
   - 若用户要求更新记忆，你可以直接使用 `search_memories` 查找目标记忆，然后调用 `update_memory`。

4. **搜索请求**
   - 当用户只要求查找记忆时，直接使用 `search_memories`。

5. **创建连接请求**
   - 若用户要求在记忆之间创建关联，可以直接使用相关工具，但必须保证关联的双方都已存在（如不确定需先搜索）。

重要原则：
- **永远不要假设记忆不存在，必须先验证。**
- **保持记忆的准确性、一致性以及人物名称的唯一识别性。**
- **严格遵守工具调用顺序：搜索 → 创建或更新。**

请根据用户请求，选择正确的工具，并严格按照流程执行。
""",
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
                    if count > 0: # start from n+1 
                      yield chapter_title, "\n".join(current_chapter)
                    current_chapter = []
                
                chapter_title = line
             
                count += 1
                if count > 2: # end with n
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

