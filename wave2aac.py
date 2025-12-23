import glob
import re
import os
import shutil
import subprocess
from pathlib import Path

"""
  环境变量
"""
start = int(os.getenv("START", 1))

end_env = os.getenv("END")
end = int(end_env) if end_env is not None else None

base_dir = Path(os.getenv("DIR", ""))

ffmpeg = os.getenv("FFMPEG")
if not ffmpeg:
    raise RuntimeError("FFMPEG environment variable is not set")
if not shutil.which(ffmpeg):
    raise RuntimeError(f"ffmpeg not found: {ffmpeg}")



"""
  获取文件列表
"""
pattern = re.compile(r"gen(\d+)-(\d+)-(\d+)\.wav")

files = []
for f in glob.glob(str(base_dir / "gen*-*-*.wav")):
    m = pattern.match(Path(f).name)
    if not m:
        continue

    n, m_, x = map(int, m.groups())

    if start <= n and (end is None or n <= end):
        files.append((n, m_, x, f))

# 按 n, m, x 排序
files.sort(key=lambda t: (t[0], t[1], t[2]))

# 生成 ffmpeg concat 文件
with open("list.txt", "w", encoding="utf-8") as f:
    for _, _, _, fname in files:
        f.write(f"file '{fname}'\n")


"""
  合并
"""
# 调用 ffmpeg 合并成 AAC
subprocess.run([
    ffmpeg,
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", "list.txt",
    "-c:a", "aac",
    "-b:a", "64k",
    "output.aac"
], check=True)
