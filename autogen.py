import asyncio
import json
import os
import time
from typing import Dict, List

# Agent/Team APIs
from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.tools import AgentTool
# from autogen_agentchat.teams import SelectorGroupChat
# from autogen_agentchat.conditions import MaxMessageTermination
# from autogen_agentchat.ui import Console
# from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage

import agent_tools
import autogen_helper
import json_tool
import splitter

PROMPT_PERSON = os.getenv("PROMPT_PERSON") or ""
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))


# ================================
# Agents：每个 AssistantAgent 接收 model_client 实例
# ================================
# 为每个 agent 创建（或共享）model_client。通常可复用同一个 client。
event_extractor_model_client = autogen_helper.extractor_model_client()
event_analyzer_model_client = autogen_helper.analyze_model_client()

# 1. Event Extractor Agent
event_extractor = AssistantAgent(
    name="EVENT_EXTRACTOR",
    system_message=(
        """
你是事件抽取器。输入是一章小说文本。提取最主要的事件，不要超过5个。
请严格输出一个 JSON Map，包含以下字段：
- chapter: 章节信息 string
- characters: 主要人物列表（每个对象包含）：
  - name: 人物名称
  - description: 人物描述（1句）string
- events: 主要事件列表（每个对象包含）：
  - name: 事件简短名称
  - summary: 事件简要总结（1-2句） string
确保 JSON 有效，不要有额外文字。
"""
    ),
    model_client=event_extractor_model_client,
    description="负责从小说章节中抽取事件列表。",
    model_client_stream=True
)

# 2. Event Analyzer Agent（改进系统提示以满足你的需求）
event_analyzer = AssistantAgent(
    name="EVENT_ANALYZER",
    system_message="""你是剧情事件深度分析师。
输入包括：原文全文 + 一个具体事件（包含 name, summary, first_sentence）。
请针对该单个事件，结合原文上下文，输出一个 JSON 对象，包含以下字段：
- name: 原事件名称 string
- first_sentence: 提及该事件在原文的第一句 string
- relationships: 涉及的主要人物和物件的关系列表（每个对象包含）：
  - source: 人物名称 string
  - target: 人物名称 string
  - type: 关系类型，用一个词表示：朋友，敌人等 string
- what: 事件过程。详述事件起因，说清该事件由什么引起，然后是事件经过，类型string
- when: 原文明确提及事件发生时间（如果原文未明确，可推断或写 '未知'），类型string
- where: 原文明确提及事件发生主要地点，单个（如果原文未明确，可写 '未知'），类型string
严格返回 JSON，不要有额外解释。""",
    model_client=event_analyzer_model_client,
    description="负责对单个事件进行深度分析。",
    model_client_stream=True
)

# 由于只有一个参与者，selector_func 不再需要
# def selector_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]):
#     if len(messages) == 1:
#         # 第一次必须事件抽取
#         return "EVENT_EXTRACTOR"


async def analyze_chapter(chapter_text: str):
    data = await extract_events(chapter_text)
    await asyncio.sleep(RATE_LIMIT)

    if not data:
        print("本章节未抽取到任何事件，跳过分析。")
        return

    all_events = data["events"]
    for i, event in enumerate(all_events):
        print(f"\n🔄 正在处理第 {i+1}/{len(all_events)} 个事件...")

        analysis_result = await analyze_single_event(chapter_text, event)
        event.update(analysis_result)

        print("\n--- 当前事件分析结果 ---")
        print(json.dumps(event, indent=2, ensure_ascii=False))
        print("------------------------\n")

        if i < len(all_events) - 1:
            print(f"⏳ 等待 {RATE_LIMIT} 秒后处理下一个事件...")
            await asyncio.sleep(RATE_LIMIT)

    return data

    # team = SelectorGroupChat(
    #     participants=[event_analyzer],
    #     termination_condition=MaxMessageTermination(max_messages=100),
    #     allow_repeated_speaker=True,
    #     model_client=_shared_model_client,
    #     model_client_streaming=True,
    #     selector_func=selector_func,
    #     # max_turns=30
    # )

    # team = RoundRobinGroupChat(
    #     participants=[coordinator, event_extractor, event_analyzer],
    #     termination_condition=MaxMessageTermination(max_messages=100),
    # )

    # async for message in team.run_stream(
    #     task=f"请开始分析。小说原文：\n{chapter_text} "
    # ):
    #     source = message.source if hasattr(message, "source") else "Unknown"
    #     content = message.content if hasattr(
    #         message, "content") else str(message)
    #     type = message.type if hasattr(message, "type") else "Unknown"
    #     if type == "TextMessage":
    #         print(f"\n[{source}]-[{type}]: {content}")
    #     else:
    #         # 使用 \r 回到行首
    #         print(f"\r{source}: "+content.replace('\n',
    #               ' ').replace('\r', ' '), end="")

    # print("最终分析结果：")
    # await Console(stream)


async def extract_events(chapter_text: str) -> List[Dict]:
    """使用 event_extractor agent 流式抽取所有事件。"""
    print("--- 开始抽取事件 ---")
    task = (f"请从以下小说章节中抽取事件列表：\n{chapter_text}"
            f"{PROMPT_PERSON}")

    final_message_content = ""
    # 使用 run_stream 进行流式调用
    stream = event_extractor.run_stream(task=task)

    # 实时打印流式输出并拼接完整内容
    print("\n[event_extractor]: ", end="", flush=True)
    async for message in stream:
        source = message.source if hasattr(
            message, "source") else ""
        content = message.content if hasattr(
            message, "content") else ""
        type = message.type if hasattr(message, "type") else ""
        if type == "TextMessage" and source == "EVENT_EXTRACTOR":
            print(f"\n[{source}]-[{type}]: {content}")
            final_message_content += content
        else:
            print(f"\r[{source}]-[{type}]", content[:100].replace(
                '\n', ''), end="", flush=True)

    print("\n--- 事件抽取完成 ---")
    try:
        data = json_tool.getJSON(final_message_content)
        events = data["events"]
        if not isinstance(events, list):
            print(f"⚠️ 警告：抽取器未返回有效的JSON数组。返回内容：{final_message_content}")
            return []
        print(f"✅ 成功抽取 {len(events)} 个事件。")
        return data
    except json.JSONDecodeError:
        print(f"❌ 错误：无法解析抽取器返回的JSON。返回内容：{final_message_content}")
        return []


async def analyze_single_event(chapter_text: str, event: Dict) -> Dict:
    """使用 event_analyzer agent 流式分析单个事件。"""
    print(f"\n--- 开始分析事件: {event.get('name', '未知事件')} ---")

    task = (
        f"小说原文全文：\n{chapter_text}\n\n"
        f"请深度分析以下这个具体事件：\n{json.dumps(event, ensure_ascii=False)}"
        f"{PROMPT_PERSON}"
    )

    final_analysis_content = ""
    # 使用 run_stream 进行流式调用
    stream = event_analyzer.run_stream(task=task)

    # 实时打印流式输出并拼接完整内容
    print(f"\n[event_analyzer]: ", end="", flush=True)
    async for message in stream:
        source = message.source if hasattr(
            message, "source") else ""
        content = message.content if hasattr(
            message, "content") else str(message)
        type = message.type if hasattr(message, "type") else ""
        if type == "TextMessage" and source == "EVENT_ANALYZER":
            print(f"\n[{source}]-[{type}]: {content}")
            final_analysis_content += content
        else:
            print(f"\r[{source}]-[{type}]", content[:100].replace(
                '\n', ''), end="", flush=True)

    print(f"\n--- 事件 '{event.get('name')}' 分析完成 ---")
    try:
        analysis = json_tool.getJSON(final_analysis_content)
        return analysis
    except json.JSONDecodeError:
        print(f"❌ 错误：无法解析分析器返回的JSON。返回内容：{final_analysis_content}")
        return {"error": "JSONDecodeError", "raw_content": final_analysis_content}


async def process_novel_by_chapter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    cp = splitter.ChapterProcessor()
    chapters = cp.process_novel_by_chapters(text)

    for idx, chapter in enumerate(chapters):
        retries = 0
        result = None
        while retries < 3:
            try:
                result = await analyze_chapter(chapter)
                break
            except Exception as e:
                retries += 1
                print(f"❌ analyze_chapter 第 {retries} 次失败：{e}")
                if retries < 3:
                    time.sleep(5)
                else:
                    raise RuntimeError("连续失败三次")

        if result:
            print(f"章节 {idx} 完成")
            await send_to_mcp(result)
            time.sleep(RATE_LIMIT)


async def send_to_mcp(json_data):
    print("send_to_mcp")

    all_tools = await agent_tools.client.get_tools()
    selected_tools = [
        tool for tool in all_tools
        if tool.name in ['add_to_neo4j']
    ]

    rs = await selected_tools[0].ainvoke(json_data)
    print('mcp result', rs)


async def main() -> None:
    await process_novel_by_chapter("input.txt")

asyncio.run(main())
