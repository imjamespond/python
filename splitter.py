import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 4096))
START = int(os.getenv("START", 1)) # start from n
END = int(os.getenv("END", 99)) # end with n

class ChapterProcessor:
    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,       # 默认值，可按需改
        chunk_overlap: int = 256      # 默认值，可按需改
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？"]
        )

    def process_novel_by_chapters(self, novel_text):
          """按章分割小说文本"""
          # 假设章节以"第X章"开头
          chapters = self._split_by_chapters(novel_text)
          
          chapter_chunks = []
          for i, chapter_content in enumerate(chapters):
              chunks = self.text_splitter.split_text(chapter_content)
              for j, chunk in enumerate(chunks):
                  chapter_chunks.append(chunk)
                  print(i,j,"chunk",len(chunk))

          return chapter_chunks
      
    def _split_by_chapters(self, text):
        # pattern = r'第[零一二三四五六七八九十百千\d]+章[^\n]*\n'
        # chapters = re.split(pattern, text)
        # return [chap for chap in chapters if chap.strip()]

        # 用括号把“章节标题”整体捕获，`?:`不单独捕获标题，使其在 split 结果中保留
        pattern = r'(第[零一二两三四五六七八九十百千\d]+[章回](?:[\t\f 　]+[^\n]*)?\n)'
        parts = re.split(pattern, text)
        chapters = []
        # # parts 的结构类似: ["前言", "第1章...", "内容1", "第2章...", "内容2", ...]
        # for i in range(1, len(parts), 2):
        #     title = parts[i]
        #     content = parts[i+1] if i+1 < len(parts) else ""
        #     chapters.append(title + content)
        #     # print(title)

        # 步长设为 10，因为每5章包含5个标题和5个内容，共10个元素
        # 从索引1开始，跳过可能存在的"前言"等非章节内容
        batch_num = int(os.getenv("BATCH_NUM", 2))
        step = batch_num * 2
        chapter_num = 0
        for i in range(1, len(parts), step):
            group_title = "" # 用于存储合并后的大章节标题
            group_content = "" # 用于存储合并后的所有内容

            # 循环5次，处理当前组内的每一章
            # j 的范围是 0, 2, 4, 6, 8 (相对于当前组的起始位置)
            for j in range(0, step, 2):
                title_index = i + j
                content_index = i + j + 1

                chapter_num += 1
                if chapter_num < START:
                    continue
                if chapter_num > END:
                    break
                  
                # 检查索引是否越界，防止在最后几章数量不足5时报错
                if title_index < len(parts):
                    title = parts[title_index].replace('\n', '') + "  "
                    group_title += title # 用 " / " 连接标题
                    print('title', title)
                    
                if content_index < len(parts):
                    group_content += parts[content_index]

            if chapter_num < START:
                continue
            if chapter_num > END:
                break
             
            # 将合并后的标题和内容组合成一个章节
            # 你可以自定义合并后的格式，这里用标题作为新标题，内容拼接
            final_chapter = f"{group_title}\n{group_content}"
            chapters.append(final_chapter)
            # print('final_chapter',final_chapter)

        return [c for c in chapters if c.strip()]
