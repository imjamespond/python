
import re
import sys
import asyncio

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
import agent_tools
import models
import tmp

LLM_JSON=models.LLM_ZP
LLM_TOOLS=models.LLM_GM
CHUNK_SIZE = 4096
START = 0 # start from n+1 
END = 10 # end with n

# ---------- Step 1: 小说分片 ----------


# ---------- Step 2: AI分析 ----------

def analyze_chunk(text_chunk):
    print(len(text_chunk))
    messages = [
    SystemMessage(content="你是一个小说分析器，提取人物、主要事件和核心关系。"),
    HumanMessage(content=f"""
请分析以下小说片段：
{text_chunk}

提取核心内容，并以严格 JSON 格式输出，仅包含以下字段：

- characters: 主要人物列表（每个对象包含）：
  - name: 人物姓名（说明："我"、"小李"等指代均统一视为其全名 **李耀**）
  - description: 1-2 句关键身份或性格描述（仅限关键人物）

- events: 主要事件列表（每个对象包含）：
  - name: 10字以内描述
  - description: 20字内简述过程（含时间、地点等） 
  - characters: 参与该事件的全部人物姓名列表

- relationships: 核心关系列表（每个对象包含）：
  - source: 人物姓名
  - target: 人物姓名
  - type: 关系类型（如朋友、敌人、亲属、合作、因果、影响、参与等）

要求：
- 仅输出纯 JSON，不得包含说明文字或注释。
- 严格基于片段内容，不作任何超出文本的推断。
- 忽略次要细节，仅保留最核心要素。
    """)
]
    # TODO: 事件名称不唯一，所以不能有事件物件节点，人物相对少名称唯一

    # response = llm.invoke(messages)
    # content = response.content
    # return content
    full = None 
    for chunk in LLM_JSON.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")
    print("\noutput json done!")
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
        if tool.name in ['add_to_neo4j']
    ]
    # print(selected_tools)
    graph = create_agent(
        LLM_TOOLS,
        selected_tools,
        system_prompt = """将JSON传给add_to_neo4j。
"""
,
    )
    inputs = {"messages": [{"role": "user", "content": json_data}]}
    try:
        async for chunk in graph.astream(inputs, stream_mode="messages"):
            print(chunk)
            await asyncio.sleep(15)
    except Exception as e:
        print("工具调用出错:", e)
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
                    if count > START: # start from n+1 
                      yield chapter_title, "\n".join(current_chapter)
                    current_chapter = []
                
                chapter_title = line
             
                count += 1
                if count > END: # end with n
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

