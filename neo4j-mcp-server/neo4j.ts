import neo4j from "neo4j-driver";
import { z } from "zod";

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
  ] as const;
}

/**
 * 将结构化的角色、事件和关系数据写入 Neo4j 图数据库。
 */

export const writeToNeo4jInputSchema = z.object({
  chapter: z.string().nullish(),
  characters: z
    .array(
      z.object({
        name: z.string(),
        description: z.string(),
      })
    )
    .optional(),
  events: z
    .array(
      z.object({
        name: z.string(),
        description: z.string().default(""),
        summary: z.string().default(""),
        what: z.string().default(""),
        when: z.string().default(""),
        where: z.string().default(""),
        first_sentence: z.string().default(""),
        reference: z.string().default(""),
        characters: z.array(z.string()).default([]),
        relationships: z
          .array(
            z.object({
              source: z.string(),
              target: z.string(),
              type: z.string().nullish(),
            })
          )
          .optional(),
      })
    )
    .optional(),
  relationships: z
    .array(
      z.object({
        source: z.string(),
        target: z.string(),
        type: z.string().nullish(),
      })
    )
    .optional(),
});

type writeToNeo4jInputType = z.infer<typeof writeToNeo4jInputSchema>;

export async function writeToNeo4j(data: writeToNeo4jInputType) {
  const characters = data.characters;
  if (!Array.isArray(characters) || characters.length === 0) {
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

  const relationships = data.relationships || [];

  try {
    await session.executeWrite(async (tx) => {
      /** --- 写入角色 --- **/
      for (const character of characters) {
        await tx.run(
          `
          MERGE (p:person {name: $name})
          // SET p.description = substring( coalesce(p.description, '') + ' ' + coalesce($description, ''), 0, 100)
          // SET p.description = 
          // CASE 
          //   WHEN p.description IS NULL THEN [$description]
          //   ELSE p.description + [$description]
          // END
          SET p.description = 
            CASE 
              WHEN size(p.description) <= 5 OR p.description IS NULL
              THEN coalesce(p.description, []) + [$description]
              ELSE p.description
            END
          `,
          character
        );
      }

      /** --- 写入事件 & 角色参与关系 --- **/
      if (Array.isArray(data.events) && data.events.length > 0) {
        for (const event of data.events) {
          const characters = event.characters;
          if (event.relationships) {
            relationships?.push(...event.relationships);
            characters.push(
              ...Array.from(
                event.relationships.reduce((set, r) => {
                  set.add(r.source.trim());
                  set.add(r.target.trim());
                  return set;
                }, new Set<string>())
              )
            );
          }
          const parameters = { ...event, chapter: data.chapter };
          await tx.run(
            `
            OPTIONAL MATCH (prev:event)
            WITH prev ORDER BY prev.seq DESC LIMIT 1
            WITH prev, coalesce(prev.seq + 1, 1) AS newSeq

            CREATE (e:event {
              seq: newSeq,
              chapter: $chapter, name: $name, summary: $summary, description: $description,
              reference: $reference, first_sentence: $first_sentence,
              characters: $characters,
              what: $what, when: $when, where: $where
            })

            FOREACH (_ IN CASE WHEN prev IS NOT NULL THEN [1] ELSE [] END |
              CREATE (prev)-[:NEXT]->(e)
            )

            WITH e
            UNWIND $characters AS character
            MERGE (p:person {name: character})
            WITH e, p
            WHERE p IS NOT NULL
            MERGE (p)-[:PARTICIPATED_IN]->(e)
            `,
            parameters
          );
        }
      }
      ``;

      /** --- 写入自定义角色关系 --- **/
      if (relationships.length > 0) {
        for (const rel of relationships) {
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
      text: "ok",
    };

    return {
      content: [result],
      structuredContent: result,
    };
  } catch (error: any) {
    console.error(error);
    const result = {
      type: "text",
      text: error.message,
    };
    return {
      content: [result],
      structuredContent: result,
    };
  } finally {
    await close();
  }
}

/**
 * 查询 Neo4j 图数据库
 */

export const queryNeo4jInputSchema = z.object({
  cypher: z.string(),
});

type queryNeo4jInputType = z.infer<typeof queryNeo4jInputSchema>;

export async function queryNeo4j(data: queryNeo4jInputType) {
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
  } catch (error: any) {
    console.error(error);
    const result = {
      type: "text",
      text: error.message,
    };
    return {
      content: [result],
      structuredContent: result,
    };
  } finally {
    await close();
  }
}
