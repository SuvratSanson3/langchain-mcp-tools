import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

# Initialize the llm
load_dotenv("key.env")
groq_api_key = os.getenv("chatbot_api_key")
llm_model = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# Define a main function
async def main():

    # create a langchain mcp client
    client = MultiServerMCPClient(
        # {
        #     "mcp_tools":{
        #         "command": "python",
        #         "args": ["mcp_server.py"],
        #         "transport": "stdio",
        #     }
        # }

        {
        "mcp_tools": {
            "transport": "sse",
            "url": "http://127.0.0.1:8000/sse",
            }
        }
    )

    # Fetching the mcp tools present in the server
    tools = await client.get_tools()
    agent = create_react_agent(llm_model, tools)

    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() in {"exit", "quit"}:
            break
        result = await agent.ainvoke({"messages":query})
        response = result["messages"][-1].content
        print("\nResponse:", response)

if __name__ == "__main__":
    asyncio.run(main())