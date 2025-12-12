import { readJsonLines } from "./jsonl.ts";
import { writeToNeo4j, writeToNeo4jInputSchema } from "./neo4j.ts";

// 示例使用
async function main() {
  for await (const data of readJsonLines()) {
    console.log(data); // 串行处理（也可改成并发）
    await writeToNeo4j(writeToNeo4jInputSchema.parse(data));
  }
}

// 运行主函数
main().catch(console.error);
