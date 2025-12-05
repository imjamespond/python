import splitter
import asyncio
import os
import time
import json

from langchain_core.messages import HumanMessage, SystemMessage
import models
import json_tool


PROMPT_POLYPHONIC = os.getenv("PROMPT_POLYPHONIC", "")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))

result_list = []


# ---------- Step 1: 小说分片 ----------
""" 
CHUNK_SIZE=1024
TEMPERATURE=0
# 开启思考模式效果好，适合执行分析查找，不适合总结
deepseek-v3.1-terminus 7
kimi-k2-instruct-0905 6.5
meituan-longcat/LongCat-Flash-Chat-FP8 512 不错
gpt-oss-20b 512 不错 256 很好
gpt-5-nano  512 很好
bytedance/seed-oss-36b-instruct 512 效果好
x-ai/grok-4.1-fast:free 1024 很好,较慢
google-ai-studio/gemini-2.5-flash  512 多词还行
zai-org/GLM-4.5-Air 512 多出其它词,很慢
deepseek-ai/deepseek-r1-0528 巨慢，多词
GLM-4.5-Flash 512 还行,很慢
Qwen/Qwen3-4B  128 偶出错
Qwen/Qwen3-8B  192 还行
Qwen/Qwen3-14B 192 可以
Qwen/Qwen3-32B 192 较好
# 非思考模式分析查找效果差
Qwen/Qwen3-Next-80B-A3B-Instruct 512 漏词
deepseek-ai/DeepSeek-V3.2-Exp 512 尚可 1024 多出其它词
"""

# ---------- Step 2: AI分析 ---------- ZHIPU 可以
def analyze_chunk(text_chunk):
    print("analyze_chunk", len(text_chunk), text_chunk)
    print("===找出多音词===")

    LLM_TEXT = models.get_llm_text()

    messages = [
        SystemMessage(content=f"""
你是一名中文多音字分析器。
1. 根据给出上下文的意思按以下规则找出多音字，输出每个多音字在文本中构成的词汇或短语，禁止输出单字！
查找规则：{PROMPT_POLYPHONIC}
2. 没有多音字直接返回`无`！禁止输出原文中未出现的词语！
3. 拼音禁止带音标！而是其后用`1234`表示4个声调！如：银行, 行读hang2; 行走, 行读xing2。
4. 严格按样例格式输出，最多输出20行，禁止输出任何样例格式以外的内容！
样例格式:
{{原词语1}}, {{多音字}} 读 {{拼音}}
{{原词语2}}, {{多音字}} 读 {{拼音}}
...
"""),
        HumanMessage(content=text_chunk)
    ]
    full = None
    for chunk in LLM_TEXT.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")

    print("\n===输出===")
    # time.sleep(RATE_LIMIT)

    # LLM_TEXT = models.LLM_QWEN

    messages = [
        SystemMessage(content=f""" 
你是一名中文多音字分析器。
要求：
- 替换规则：
    * 按格式读取每行：{{原词}}, {{多音字}}读{{读音}}
    * 根据`读音`将`原词`中的多音字替换为拼音。如：银行，替换后：银hang2；行走，替换后：xing2走。
    * 只替换每行给出的`多音字`，禁止替换非`多音字`！
    * 没有内容，则输出空数组。
- 输出格式为严格的标准JSON数组：
  [
    [{{原词1}},{{替换后1}}],
    [{{原词2}},{{替换后2}}]
  ]
"""),
        HumanMessage(content=full.text)
    ]
    full = None
    for chunk in LLM_TEXT.stream(messages):
        full = chunk if full is None else full + chunk
        print(chunk.text, end="")

    print("\nanalyze_chunk done!", len(text_chunk))
    return full.text


# ---------- Step 4: 主流程 ----------


def process_novel(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        cp = splitter.ChapterProcessor(chunk_overlap=0)
        chunks = cp.process_novel(text)

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
        # 紧凑格式：每行一个顶层数组元素
        json_str = '[\n' + ',\n'.join(json.dumps(item, ensure_ascii=False) for item in result_list) + '\n]'
        f.write(json_str)
        # json.dump(result_list, f, ensure_ascii=False, indent=4)

# ---------- Step 3: handle ----------


async def handle(json_data):
    print("handle", len(json_data))
    try:
        # 解析JSON字符串
        parsed_data = json_tool.getJSON(json_data)

        # 将解析后的数据添加到列表中
        result_list.extend(parsed_data)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")



# ---------- 示例 ----------
if __name__ == "__main__":
    process_novel("input-polyphonic.txt")
