import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model


load_dotenv()


async def fetch_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()
        await page.goto(url)

        content = await page.content()

        await browser.close()

        return content

async def run_agent():

    client = MultiServerMCPClient(
    {
        "bright_data": {
             "command": "npx",
            "args": ["@brightdata/mcp"],
            "env": {
                "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
             
            },
            "transport": "stdio",
        },
        
    }
    )
    tools = await client.get_tools()
    model=init_chat_model(
        model="openai:gpt-4.1",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    agent = create_agent(model=model,tools=tools)
    agent = create_agent(model=model, tools=tools)

    agent_response = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": "You are a web search agent with access to brightdata tool to get the data"},
            {"role": "user", "content": "is us-israel vs iran war on going?"}
        ]
    })
   
    print(agent_response["messages"][-1].content)
    



if __name__=="__main__":
    asyncio.run(run_agent())
## this is demo
