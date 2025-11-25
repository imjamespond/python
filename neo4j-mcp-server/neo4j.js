import neo4j from "neo4j-driver";

// 创建 Neo4j 驱动
function initNeo4j() {
  // const driver = neo4j.driver("bolt://192.168.8.201:7687", neo4j.auth.basic("neo4j", "your-password"));
  const driver = neo4j.driver(
    process.env.NEO4J_URI,
    neo4j.auth.basic(process.env.NEO4J_USERNAME, process.env.NEO4J_PASSWORD)
  );
  const session = driver.session();
  return [
    session,
    async () => {
      await session.close();
      await driver.close();
    },
  ];
}
/**
 * 将结构化的角色、事件和关系数据写入 Neo4j 图数据库。
 *
 * @param {Object} data - 包含角色、事件和关系的数据对象。
 * @param {Array<{ name: string, description: string }>} data.characters - 角色列表。
 * @param {Array<{ name: string, description: string, characters: string[] }>|undefined} data.events - 事件列表，每个事件关联一组角色名称。
 * @param {Array<{ source: string, target: string, type: string }>|undefined} data.relationships - 角色之间的关系列表。
 */
export async function writeToNeo4j(data) {
  if (!Array.isArray(data.characters) || !data.characters.length > 0) {
    const result = {
      type: "text",
      text: "数据为空，跳过执行",
    };
    return {
      content: [result],
      structuredContent: result,
    };
  }

  const [session, close] = initNeo4j();

  try {
    await session.executeWrite(async (tx) => {
      /** --- 写入角色 --- **/
      for (const character of data.characters) {
        await tx.run(
          `
          MERGE (p:person {name: $name})
          SET p.description = substring( coalesce(p.description, '') + ' ' + coalesce($description, ''), 0, 100)
          `,
          character
        );
      }

      /** --- 写入事件 & 角色参与关系 --- **/
      if (Array.isArray(data.events) && data.events.length > 0) {
        for (const event of data.events) {
          await tx.run(
            `
          OPTIONAL MATCH (prev:event)
          WITH prev ORDER BY prev.seq DESC LIMIT 1
          WITH prev, coalesce(prev.seq + 1, 1) AS newSeq
          
          CREATE (e:event {name: $name, description: $description, seq: newSeq})

          WITH prev, e
          WHERE prev IS NOT NULL
          CREATE (prev)-[:NEXT]->(e)

          WITH e
          UNWIND $characters AS charName
          OPTIONAL MATCH (p:person {name: charName})
          WITH e, p
          WHERE p IS NOT NULL
          MERGE (p)-[:PARTICIPATED_IN]->(e)
          `,
            event
          );
        }
      }

      /** --- 写入自定义角色关系 --- **/
      if (Array.isArray(data.relationships) && data.relationships.length > 0) {
        for (const rel of data.relationships) {
          await tx.run(
            `
            OPTIONAL MATCH (source:person {name: $source})
            OPTIONAL MATCH (target:person {name: $target})
            WITH source, target
            WHERE source IS NOT NULL AND target IS NOT NULL
            MERGE (source)-[r:RELATION]->(target)
            ON CREATE SET r.type = $type
            `,
            rel
          );
        }
      }
    });

    const result = {
      type: "text",
      text: "成功写入 Neo4j",
    };

    return {
      content: [result],
      structuredContent: result,
    };
  } catch (err) {
    console.error(err);
    const result = {
      type: "text",
      text: err.message,
    };
    return {
      content: [result],
      structuredContent: result,
    };
  } finally {
    await close();
  }
}

export async function queryNeo4j(data) {
  const [session, close] = initNeo4j();

  try {
    const result = await session.executeRead((tx) => tx.run(data.cypher));
    const textOutput =
      result.records.map((record) => JSON.stringify(record.toObject(), null, 2)).join("\n") || "No results";

    const structuredContent = {
      type: "text",
      text: textOutput,
    };

    return {
      content: [structuredContent],
      structuredContent,
    };
  } catch (error) {
    console.error(error);
    const result = {
      type: "text",
      text: err.message,
    };
    return {
      content: [result],
      structuredContent: result,
    };
  } finally {
    await close();
  }
}
