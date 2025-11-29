import splitter
import asyncio
import os
import time
import json

from langchain_core.messages import HumanMessage, SystemMessage
import models

PROMPT_POLYPHONIC = os.getenv("PROMPT_POLYPHONIC", "")
result_list = []


# ---------- Step 1: 小说分片 ----------


# ---------- Step 2: AI分析 ---------- ZHIPU 可以
def analyze_chunk(text_chunk):
    title = text_chunk.split('\n')[0][:20]
    print("\nanalyze_chunk", title)

    messages = [
        SystemMessage(content=f"""
你是一名中文多音字分析器。
按以下匹配规则找出相关词语，不要输出不匹配的词语和单字！
  查找规则：{PROMPT_POLYPHONIC}
每行一个词语输出，禁止输出任何样例格式以外的内容！
样例格式：
原词1
原词2
...
"""),

        HumanMessage(content=text_chunk)
    ]
    full = None
    for chunk in models.LLM_TEXT.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")

    print("\n===找出多音词===")
    time.sleep(10)

    messages2 = [
        SystemMessage(content=f""" 
你是一名中文多音字分析器。
要求：
- 替换格式：将词语中的多音字替换为对应的拼音（带数字声调）如：银行->银hang2
- 特殊优先匹配规则：{PROMPT_POLYPHONIC}
- 输出格式为严格的标准JSON数组：
  [
    ["原词1", "替换后1"],
    ["原词2", "替换后2"]
  ]

注意：
- 仅输出完整匹配多音词的结果，不修改非多音词
- 每个条目必须是二维数组，对应原词与替换结果
- 禁止输出任何非JSON内容（包括Markdown、反引号、解释文字等）
- 确保所有输出均可被标准JSON解析器直接解析 """),
        HumanMessage(content=full.text)
    ]
    full2 = None
    for chunk in models.LLM_TEXT.stream(messages2):
        full2 = chunk if full2 is None else full2 + chunk
        print(chunk.text, end="")

    print("\nanalyze_chunk done!", title)
    return full2.text


# ---------- Step 4: 主流程 ----------


def process_novel_by_chapter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        cp = splitter.ChapterProcessor(chunk_overlap=0)
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
                asyncio.run(handle(analysis))  # 上面定义的 MCP 发送函数
                time.sleep(10)
                print(f"{i} done")

        for original, replacement in result_list:
            text = text.replace(original, replacement)

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(text)


# ---------- Step 3: handle ----------
async def handle(json_data):
    print("handle", len(json_data))
    try:
        # 解析JSON字符串
        parsed_data = json.loads(json_data.replace("```json\n", "").replace("```\n", "").replace("```", "").strip())

        # 将解析后的数据添加到列表中
        result_list.extend(parsed_data)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

# ---------- 示例 ----------
if __name__ == "__main__":
    process_novel_by_chapter("input.txt")
