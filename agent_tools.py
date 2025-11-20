from langchain_mcp_adapters.client import MultiServerMCPClient

# 配置多个MCP服务器
# https://docs.langchain.com/oss/python/langchain/mcp
client = MultiServerMCPClient(
    {
        # "neo4j-memory": {
        #     "transport": "stdio",  # 本地子进程通信
        #     "command": "npx",
        #     "args": ["-y", "@knowall-ai/mcp-neo4j-agent-memory"],
        #     "env": {
        #         "NEO4J_URI": "bolt://192.168.8.201:7687",
        #         "NEO4J_USERNAME": "neo4j",
        #         "NEO4J_PASSWORD": "your-password"
        #     }
        # }, 
        # "neo4j": {
        #     "transport": "stdio",  # 本地子进程通信
        #     "command": "uvx",
        #     "args": ["mcp-neo4j-memory@0.4.2"],
        #     "env": {
        #         "NEO4J_URI": "bolt://192.168.8.201:7687",
        #         "NEO4J_USERNAME": "neo4j",
        #         "NEO4J_PASSWORD": "your-password"
        #     }
        # }, 
        "my-mcp": {
            "url": "http://localhost:3000/mcp",
            "transport": "streamable_http",  
        }
    }
)
