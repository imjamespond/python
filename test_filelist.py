
if __name__ == '__main__':
  with open('../test-yolo/output_file.txt', 'r', encoding='utf-8') as f:
      for i, line in enumerate(f, start=1):          # 逐行流式读取，内存友好
          path = line.strip()  # 去掉换行符和首尾空白
          print(path, f"img{i}.jpg")