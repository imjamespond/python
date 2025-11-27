import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 4096+2048
START = int(os.getenv("START", 0)) # start from n+1
END = int(os.getenv("END", 99)) # end with n

class ChapterProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=256,
            separators=["\n\n", "\n", "。", "！", "？"]
        )

    def process_novel_by_chapters(self, novel_text):
          """按章分割小说文本"""
          # 假设章节以"第X章"开头
          chapters = self._split_by_chapters(novel_text)
          
          chapter_chunks = []
          for i, chapter_content in enumerate(chapters):
              if i < START:
                  continue
              if i > END:
                  break
              chunks = self.text_splitter.split_text(chapter_content)
              for j, chunk in enumerate(chunks):
                  chapter_chunks.append(chunk)
                  print(i,j,"chunk",len(chunk))

          return chapter_chunks
      
    def _split_by_chapters(self, text):
        # pattern = r'第[零一二三四五六七八九十百千\d]+章[^\n]*\n'
        # chapters = re.split(pattern, text)
        # return [chap for chap in chapters if chap.strip()]

        # 用括号把“章节标题”捕获下来，使其在 split 结果中保留
        pattern = r'(第[零一二三四五六七八九十百千\d]+章\s+[^\n]*\n)'
        parts = re.split(pattern, text)
        chapters = []
        # parts 的结构类似: ["前言", "第1章...", "内容1", "第2章...", "内容2", ...]
        for i in range(1, len(parts), 2):
            title = parts[i]
            content = parts[i+1] if i+1 < len(parts) else ""
            chapters.append(title + content)
            # print(title)

        return [c for c in chapters if c.strip()]
