import { writeToNeo4j } from "./neo4j.js";

const testData = {
  characters: [
    { name: "李耀", description: "三十出头公交车司机，公司最年轻，单身。" },
    { name: "老吴", description: "车队队长，湖北人，老奸巨猾。" },
    { name: "老唐", description: "同事，告知李耀造纸厂路线事故。" },
  ],
  events: [
    { name: "紧急会议", description: "周日公司，老吴召集讨论加开造纸厂夜班车。", characters: ["李耀", "老吴"] },
    { name: "指定李耀", description: "会议中老吴强安排李耀开夜班，加700元补助。", characters: ["李耀", "老吴"] },
    { name: "老唐警告", description: "食堂晚饭，老唐告知三任司机拉车冲水库事故。", characters: ["李耀", "老唐"] },
    { name: "启动出车", description: "晚10:30，李耀启动2386车，见门卫惊恐。", characters: ["李耀"] },
  ],
  relationships: [
    { source: "老吴", target: "李耀", type: "领导安排" },
    { source: "老唐", target: "李耀", type: "朋友" },
    { source: "老吴", target: "李耀", type: "影响" },
  ],
};

writeToNeo4j(testData)
  .then((res) => console.log("测试结果：", res))
  .catch((err) => console.error("测试异常：", err));
