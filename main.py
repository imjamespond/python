import os
import sys
import asyncio
import time

from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
import agent_tools
import json_tool
import models

# CHUNK_SIZE = 4096
# START = 0 # start from n+1 
# END = 20 # end with n

# ---------- Step 1: 小说分片 ----------


# ---------- Step 2: AI分析 ----------
def analyze_chunk(text_chunk):
    title=text_chunk.split('\n')[0][:20] 
    print("\nanalyze_chunk", title)
    messages = [
    SystemMessage(content="你是一个小说分析器，提取人物、主要事件和核心关系。"),
    HumanMessage(content=f"""
请分析以下小说片段：
{text_chunk}

提取核心内容，并**严格以 JSON 字符串格式**输出，类型为Map，仅包含以下字段：

- chapter: 章节编号，不要标题（如“第一章，第二章，第三章…”）,类型为string。

- characters: 主要人物列表（每个对象包含）：
  - name: 人物名称{models.PROMPT_PERSON}
  - description: 关键身份，性格，背景描述

- events: 主要事件列表（每个对象包含）：
  - name: 10字以内描述
  - description: 概括事件。要求：1，每个事件必须以其在原文中的第一句话作为开头并以……结束(不超过30字)；2，接着完整说明事件的时间、地点、起因与经过(200字内)。
  - characters: 参与该事件的全部人物名称列表

- relationships: 核心关系列表（每个对象包含）：
  - source: 人物名称
  - target: 人物名称
  - type: 关系类型（如朋友、敌人、亲属、合作、因果、影响、参与等）

要求：
- 你必须只返回纯 JSON，不允许出现任何 Markdown、代码块、反引号或额外说明。输出必须可被 JSON 解析器直接解析。
- 严格基于片段内容，不作任何超出文本的推断。
- 忽略次要细节，仅保留最核心要素。
""")]
    # TODO: 事件名称不唯一，所以不能有事件物件节点，人物相对少名称唯一

    # response = llm.invoke(messages)
    # content = response.content
    # return content
    full = None 
    for chunk in models.LLM_TEXT.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")
    print("\nanalyze_chunk done!", title )
    return full.text

# ---------- Step 3: 调用 MCP Server ----------
async def send_to_mcp(json_data):
    print("send_to_mcp", len(json_data))

    # 获取工具并创建代理
    all_tools = await agent_tools.client.get_tools()
    # print(f"所有可用工具: {[tool.name for tool in all_tools]}")
    selected_tools = [
        tool for tool in all_tools 
        if tool.name in ['add_to_neo4j']
    ]
    # print(selected_tools)

    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:

        try:
            if os.getenv("USE_TOOLS_CALL"):
              graph = create_agent(
                  models.LLM_TOOLS,
                  selected_tools,
                  system_prompt = """将JSON传给add_to_neo4j。""",
              )
              inputs = {"messages": [{"role": "user", "content": json_data}]}
              async for chunk in graph.astream(inputs, stream_mode="messages"):
                  print(chunk)
                  await asyncio.sleep(10)

            else:
              rs = await selected_tools[0].ainvoke(json_tool.getJSON(json_data))
              print('mcp result',rs)
              if rs != "ok": 
                  raise RuntimeError(rs)

            break  # 成功则跳出重试循环
        
        except Exception as e:
            print("send_to_mcp 出错:", e)
            retry_count += 1
            if retry_count < max_retries:
                print(f"send_to_mcp 等待 5 秒后重试...")
                time.sleep(5)  # 同步sleep
            else:
                raise RuntimeError("send_to_mcp 达到最大重试次数")
                
        # rs = await asyncio.create_task(graph.ainvoke(inputs,stream_mode="messages")) 
        # print(rs)

# ---------- Step 4: 主流程 ----------
import splitter
def process_novel_by_chapter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
      text = f.read()
      cp = splitter.ChapterProcessor()
      chunks = cp.process_novel_by_chapters(text)

      # debug chunks
      # return 
    
      for i, chunk in enumerate(chunks):
        max_retries = 3
        retry_count = 0
        analysis = None

        while retry_count < max_retries:
            try:
                analysis = analyze_chunk(chunk)  # 上面定义的分析函数
                break  # 成功则跳出重试循环
            except Exception as e:
                retry_count += 1
                print(f"analyze_chunk 第 {retry_count} 次尝试失败: {e}")
                if retry_count < max_retries:
                    print(f"analyze_chunk 等待 5 秒后重试...")
                    time.sleep(5)  # 同步sleep
                else:
                    raise RuntimeError("analyze_chunk 达到最大重试次数")

        if analysis:
            asyncio.run(send_to_mcp(analysis))  # 上面定义的 MCP 发送函数
            time.sleep(10)
            print(f"{i} done")
    # for chapter_title, chapter_text in chapter_stream(file_path):
    #     if len(chapter_text) > CHUNK_SIZE + 2000:
    #       chunks = []
    #       # 分块策略：每1000字
    #       for i in range(0, len(chapter_text), CHUNK_SIZE):
    #           chunk = chapter_text[i:i+CHUNK_SIZE]
    #           chunks.append(chunk)
    #     else:
    #       chunks = [chapter_text]
        
    #     # 然后处理 chunks 列表
    #     print(f"处理章节：{chapter_title}, chunks: {len(chunks)}")
    #     for chunk in chunks:
    #       analysis = analyze_chunk(chunk)  # 上面定义的分析函数
    #       if analysis:
    #           result = asyncio.run(send_to_mcp(analysis))  # 上面定义的 MCP 发送函数
    #           asyncio.sleep(10)
    #           print(f"MCP 返回：{result}")



# def chapter_stream(file_path):
#     """
#     按章节流式读取小说，每次返回一个章节文本。
#     假设章节以 '第X章' 开头
#     """
#     chapter_pattern = re.compile(r'(第.*章.*)')
#     current_chapter = []
#     chapter_title = None
#     count = 0
#     with open(file_path, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue  # 跳过空行
#             match = chapter_pattern.match(line)
#             if match:
                
#                 # 遇到新章节，先返回上一章
#                 if current_chapter:
#                     if count > START: # start from n+1 
#                       yield chapter_title, "\n".join(current_chapter)
#                     current_chapter = []
                
#                 chapter_title = line
             
#                 count += 1
#                 if count > END: # end with n
#                   break

#             else:
#                 current_chapter.append(line)
#         # 返回最后一章
#         if current_chapter:
#             yield chapter_title, "\n".join(current_chapter)

# ---------- 示例 ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供小说文件路径作为第一个参数")
        sys.exit(1)
    file_path = sys.argv[1]
    process_novel_by_chapter(file_path)
    # import tmp
    # asyncio.run(send_to_mcp(tmp.JSON))

