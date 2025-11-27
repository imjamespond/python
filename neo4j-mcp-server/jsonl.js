// 使用 import 导入 Node.js 内置模块（ESM 风格）
import fs from "fs";
import fsPromises from "fs/promises";
import path from "path";
import { createReadStream } from "fs";
import { createInterface } from "readline";

// 文件路径
// const FILE_PATH = path.join(import.meta.url.substring(7), '..', 'jsondata.jsonl');
// 更安全的写法（推荐）：
const __dirname = new URL(".", import.meta.url).pathname;
const FILE_PATH = path.join(__dirname, "data.jsonl");

// 同步追加一行 JSON
export function appendObjAsJsonLine(obj) {
  const jsonLine = JSON.stringify(obj) + "\n";
  fs.appendFileSync(FILE_PATH, jsonLine, "utf8");
}

// 异步追加（推荐用于性能）
export async function appendObjAsJsonLineAsync(obj) {
  const jsonLine = JSON.stringify(obj) + "\n";
  await fsPromises.appendFile(FILE_PATH, jsonLine, "utf8");
}

/**
 * 逐行读取并解析 JSONL 文件
 */
export async function* readJsonLines() {
  const fileStream = createReadStream(FILE_PATH);
  const rl = createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    if (line.trim() === "") continue;
    try {
      const obj = JSON.parse(line);
      yield obj
    } catch (err) {
      console.error("Invalid JSON line:", line, err);
    }
  }
}

