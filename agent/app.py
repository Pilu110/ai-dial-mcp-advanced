import asyncio
import json
import os

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role


async def main():
    # Create empty list for tools and dict for mapping tool names to clients
    tools = []
    tool_name_client_map = {}

    # Create UMS MCPClient
    ums_client = await CustomMCPClient.create("http://localhost:8006/mcp")
    ums_tools = await ums_client.get_tools()
    tools.extend(ums_tools)
    for tool in ums_tools:
        tool_name_client_map[tool["function"]["name"]] = ums_client

    # Create DIAL Client
    dial_client = DialClient(
        api_key=os.getenv("DIAL_API_KEY", ""),
        endpoint="https://ai-proxy.lab.epam.com",
        tools=tools,
        tool_name_client_map=tool_name_client_map
    )

    # Create system message with instructions for LLM
    messages = [
        Message(
            role=Role.SYSTEM,
            content="You are a helpful AI assistant that can help users manage users in the system using available tools. "
                    "Use the provided tools to search for users, create new users, update existing users, and delete users. "
                    "Always try to help the user complete their request using the available tools."
        )
    ]

    # Simple console chat
    while True:
        user_input = input("\n👤 You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        messages.append(Message(role=Role.USER, content=user_input))

        try:
            ai_response = await dial_client.get_completion(messages)
            messages.append(ai_response)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him