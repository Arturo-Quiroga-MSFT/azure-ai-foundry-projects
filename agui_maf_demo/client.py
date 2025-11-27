"""AG-UI client example.

This client connects to an AG-UI server and enables interactive chat
with streaming responses displayed in real-time.
"""

import asyncio
import os

from agent_framework import ChatAgent
from agent_framework_ag_ui import AGUIChatClient


async def main():
    """Main client loop with interactive chat."""
    # Get server URL from environment or use default
    server_url = os.environ.get("AGUI_SERVER_URL", "http://127.0.0.1:8888/")
    print(f"🔌 Connecting to AG-UI server at: {server_url}\n")

    # Create AG-UI chat client that connects to the server
    chat_client = AGUIChatClient(server_url=server_url)

    # Create agent with the chat client
    agent = ChatAgent(
        name="ClientAgent",
        chat_client=chat_client,
        instructions="You are a helpful assistant.",
    )

    # Get a thread for conversation continuity
    thread = agent.get_new_thread()

    print("💬 AG-UI Client - Interactive Chat")
    print("=" * 50)
    print("Type your messages and press Enter.")
    print("Type ':q' or 'quit' to exit.\n")

    try:
        while True:
            # Get user input
            message = input("\n\033[1;34mUser:\033[0m ")
            if not message.strip():
                print("\033[91m⚠️  Request cannot be empty.\033[0m")
                continue

            if message.lower() in (":q", "quit"):
                print("\n👋 Goodbye!")
                break

            # Stream the agent response
            print("\n\033[1;32mAssistant:\033[0m ", end="", flush=True)
            async for update in agent.run_stream(message, thread=thread):
                # Print text content as it streams
                if update.text:
                    print(f"\033[96m{update.text}\033[0m", end="", flush=True)

            print("\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n\033[91m❌ An error occurred: {e}\033[0m")


if __name__ == "__main__":
    asyncio.run(main())
