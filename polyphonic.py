import splitter
import asyncio
import os
import time
import json

from langchain_core.messages import HumanMessage, SystemMessage
import models

PROMPT_POLYPHONIC = os.getenv("PROMPT_POLYPHONIC", "")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))

result_list = []


# ---------- Step 1: 小说分片 ----------


# ---------- Step 2: AI分析 ---------- ZHIPU 可以
def analyze_chunk(text_chunk):
    title = text_chunk.split('\n')[0][:20]
    print("\nanalyze_chunk", title)

    LLM_TEXT = models.get_llm_text()

    messages = [
        SystemMessage(content=f"""
你是一名中文多音字分析器。
按以下匹配规则找出相关词语，不要输出不匹配的词语！若出现的是单字，则输出其所在的最小有意义短语。
  查找规则：{PROMPT_POLYPHONIC}
每行输出一个词语，最多20个，禁止输出任何样例格式以外的内容！
样例格式：
原词1
原词2
...
"""),

        HumanMessage(content=text_chunk)
    ]
    full = None
    for chunk in LLM_TEXT.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")

    print("\n===找出多音词===")
    time.sleep(RATE_LIMIT)

    messages2 = [
        SystemMessage(content=f""" 
你是一名中文多音字分析器。
要求：
- 替换格式：将词语中的多音字替换为对应的拼音（带数字声调）如：`银行`的行读hang2，替换后：银hang2
- 匹配规则：{PROMPT_POLYPHONIC}
- 输出格式为严格的标准JSON数组：
  [
    ["原词1", "替换后1"],
    ["原词2", "替换后2"]
  ]

注意：
- 仅输出符合匹配规则多音词的结果
- 每个条目必须是二维数组，对应原词与替换结果
- 禁止输出任何非JSON内容（包括Markdown、反引号、解释文字等）
- 确保所有输出均可被标准JSON解析器直接解析 """),
        HumanMessage(content=full.text)
    ]
    full2 = None
    for chunk in LLM_TEXT.stream(messages2):
        full2 = chunk if full2 is None else full2 + chunk
        print(chunk.text, end="")

    print("\nanalyze_chunk done!", title)
    return full2.text


# ---------- Step 4: 主流程 ----------


def process_novel_by_chapter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        cp = splitter.ChapterProcessor(chunk_overlap=128)
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
                time.sleep(RATE_LIMIT)
                print(f"{i} done")

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)

# ---------- Step 3: handle ----------


async def handle(json_data):
    print("handle", len(json_data))
    try:
        # 解析JSON字符串
        parsed_data = json.loads(json_data.replace("```json\n", "").replace(
            "```\n", "").replace("```", "").strip())

        # 将解析后的数据添加到列表中
        result_list.extend(parsed_data)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")


def replace_with_json(text):
    with open('output.json', 'r', encoding='utf-8') as f:
        list = json.load(f)
        for original, replacement in list:
            text = text.replace(original, replacement)
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(text)


# ---------- 示例 ----------
if __name__ == "__main__":

    if os.path.exists('output.json'):
        replace_with_json()
    else:
        process_novel_by_chapter("input.txt")
