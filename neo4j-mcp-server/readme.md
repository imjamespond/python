doc
https://modelcontextprotocol.io/specification/2025-06-18/server/tools
```
post 
http://localhost:3000/mcp
body
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
client must both accept
"accept": "text/event-stream,application/json;

```

start
`npm start`
flush jsondata
`npm run flush`