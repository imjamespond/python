
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
        SystemMessage(content="你是一个小说分析器，提取人物、事件和关系。"),
        HumanMessage(content=f"""
请分析以下小说片段：
{text_chunk}

请以严格 JSON 格式输出，包括以下字段：

1. characters: 人物列表，每个对象包含：
    - name: 人物名字
    - description: 简短描述或性格特征

2. events: 事件列表，每个对象包含：
    - description: 事件描述
    - time: 事件发生的时间（如果文中未明确可写 null）
    - location: 事件发生的地点（如果文中未明确可写 null）
    - participants: 参与事件的人物名字列表

3. relationships: 人物之间的关系，每个对象包含：
    - source: 人物名字
    - target: 人物名字
    - type: 关系类型（如朋友、敌人、亲属、合作等）
    - event: 关联的事件描述（如果适用）

请严格按照 JSON 格式输出，不要添加额外文本。
""")
    ]
    # response = llm.invoke(messages)
    # content = response.content
    # return content
    full = None 
    for chunk in models.LLM1.stream(messages):
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
        models.LLM2,
        selected_tools,
        system_prompt= """你是一个记忆管理助手，负责处理记忆的创建、更新和搜索。

工作流程：
1. 当用户要求创建新记忆时，你必须先使用 search_memories 工具搜索是否已存在类似记忆
2. 如果搜索结果显示记忆不存在，再使用 create_memory 工具创建新记忆
3. 如果记忆已存在，考虑使用 update_memory 工具更新现有记忆
4. 对于其他操作（更新记忆、搜索记忆、创建连接等），按需直接使用相应工具

重要规则：
- 在创建任何新记忆之前，必须先进行搜索
- 不要假设记忆不存在，总是先验证
- 保持记忆内容的准确性和一致性

请根据用户请求选择适当的工具并按正确顺序执行。""",
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
                if count > 2: 
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

