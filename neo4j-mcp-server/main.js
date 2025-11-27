import { z } from "zod";
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";
import { writeToNeo4j, queryNeo4j } from "./neo4j.js";
import { appendObjAsJsonLineAsync } from "./jsondata.js";

const server = new McpServer({
  name: "neo4j-mcp-server",
  version: "1.0.0",
});

server.registerTool(
  "add_to_neo4j",
  {
    title: "add_to_neo4j",
    description: "将数据写入 Neo4j",
    inputSchema: z.object({
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
            description: z.string(),
            characters: z.array(z.string()).default([]),
          })
        )
        .optional(),
      relationships: z
        .array(
          z.object({
            source: z.string(),
            target: z.string(),
            type: z.string(),
          })
        )
        .optional(),
    }),
    outputSchema: z.object({ type: z.string(), text: z.string() }), // langgraph对格式严格要求
  },
  async (data) => {
    console.log("add_to_neo4j", data);
    await appendObjAsJsonLineAsync(data)
    return await writeToNeo4j(data);
  }
);

server.registerTool(
  "query_neo4j",
  {
    title: "query neo4j",
    description: "执行 cypher 查询",
    inputSchema: z.object({
      cypher: z.string(),
    }),
    outputSchema: z.object({ type: z.string(), text: z.string() }), // langgraph对格式严格要求
  },
  async (data) => {
    console.log("query_neo4j", data);
    return await queryNeo4j(data);
  }
);

server.registerResource(
  "greeting",
  new ResourceTemplate("greeting://{name}", { list: undefined }),
  {
    title: "Greeting Resource",
    description: "Dynamic greeting generator",
  },
  async (uri, { name }) => ({
    contents: [
      {
        uri: uri.href,
        text: `Hello, ${name}!`,
      },
    ],
  })
);

// 注册工具
// server.tool(createNeo4jTool());

// 启动 MCP Server
// server.listen();

const app = express();
app.use(express.json()); // Middleware to parse JSON request bodies
app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined, // You can provide a custom session ID generator if needed
    enableJsonResponse: true, // Enables JSON responses
  });
  // Ensure the transport is closed when the response stream ends
  res.on("close", () => {
    transport.close();
  });
  // Connect the MCP server to the transport
  await server.connect(transport);
  // Handle the incoming HTTP request with the transport
  await transport.handleRequest(req, res, req.body);
});

const port = parseInt(process.env.PORT || "3000");
app
  .listen(port, () => {
    console.log(`MCP Server running on http://localhost:${port}/mcp`);
  })
  .on("error", (error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
