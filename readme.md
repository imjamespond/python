```bash
uv venv --python 3.10
uv pip install -U langchain langchain-openai langchain-ollama langchain-mcp-adapters
uv pip install -U langchain_text_splitters faiss-cpu #embed
uv pip install -U "autogen-agentchat" "autogen-ext[openai]"
uv pip show langchain  
```