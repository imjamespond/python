import asyncio
from autogen_agentchat.agents import AssistantAgent

import autogen_helper



async def main() -> None:
    model_client = autogen_helper.extractor_model_client()
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Say 'Hello World!'"))
    await model_client.close()

asyncio.run(main())
