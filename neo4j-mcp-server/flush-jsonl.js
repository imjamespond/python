import { readJsonLines } from "./jsonl.js";
import { writeToNeo4j } from "./neo4j.js";

// 示例使用
async function main() {
  for await (const data of readJsonLines()) {
    console.log(data); // 串行处理（也可改成并发）
    await writeToNeo4j(data);
  }
}

// 运行主函数
main().catch(console.error);
