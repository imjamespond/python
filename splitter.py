from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 4096
START = 31 # start from n
END = 50 # end with n

class ChapterProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=200,
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
              if i >= END:
                  break
              chunks = self.text_splitter.split_text(chapter_content)
              for j, chunk in enumerate(chunks):
                  chapter_chunks.append(chunk)
                  print(i,j,"chunk",len(chunk))

          return chapter_chunks
      
    def _split_by_chapters(self, text):
        import re
        pattern = r'第[零一二三四五六七八九十百千\d]+章[^\n]*\n'
        chapters = re.split(pattern, text)
        return [chap for chap in chapters if chap.strip()]



