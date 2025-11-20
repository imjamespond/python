import { writeToNeo4j } from "./neo4j.js";

const testData = {
        "characters": [
                {
                        "name": "李耀",
                        "description": "三十出头，公交车司机，自力更生，无女友"
                },
                {
                        "name": "老吴",
                        "description": "车队队长，湖北人，老奸巨猾，无利不起早"
                },
                {
                        "name": "老唐",
                        "description": "李耀同事，神秘兮兮，提醒李耀造纸厂路线危险"
                }
        ],
        "events": [
                {
                        "name": "李耀被电话吵醒",
                        "description": "李耀周日轮休被老吴电话叫醒开会",
                        "characters": ["李耀", "老吴"]
                },
                {
                        "name": "老吴宣布加车",
                        "description": "老吴宣布市里要求加开到造纸厂夜班",
                        "characters": ["老吴", "李耀", "其他司机"]
                },
                {
                        "name": "李耀被安排夜班",
                        "description": "李耀被老吴安排开造纸厂夜班并加薪",
                        "characters": ["李耀", "老吴"]
                },
                {
                        "name": "老唐提醒李耀",
                        "description": "老唐提醒李耀造纸厂路线十年前事故频发",
                        "characters": ["李耀", "老唐"]
                },
                {
                        "name": "李耀出车",
                        "description": "李耀晚上十点半开车前往造纸厂",
                        "characters": ["李耀"]
                }
        ],
        "relationships": [
                {
                        "source": "李耀",
                        "target": "老吴",
                        "type": "上下级"
                },
                {
                        "source": "李耀",
                        "target": "老唐",
                        "type": "朋友"
                },
                {
                        "source": "老吴",
                        "target": "其他司机",
                        "type": "上下级"
                },
                {
                        "source": "老吴",
                        "target": "李耀",
                        "type": "影响"
                }
        ]
}

writeToNeo4j(testData)
  .then((res) => console.log("测试结果：", res))
  .catch((err) => console.error("测试异常：", err));
