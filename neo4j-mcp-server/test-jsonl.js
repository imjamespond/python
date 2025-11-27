import { appendObjAsJsonLineAsync, readJsonLines } from "./jsondata.js";

// 示例使用
async function main() {
  // 写入几条数据
  await appendObjAsJsonLineAsync({ id: 1, name: "Alice" });
  await appendObjAsJsonLineAsync({ id: 2, name: "Bob" });
  await appendObjAsJsonLineAsync({ id: 3, name: "Charlie", active: true });

  console.log("--- Reading back ---");
  for await (const data of readJsonLines()) {
    console.log(data); // 串行处理（也可改成并发）
  }
}

// 运行主函数
main().catch(console.error);
