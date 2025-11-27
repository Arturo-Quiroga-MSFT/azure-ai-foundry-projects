"""AG-UI client with tool event display.

This enhanced client displays tool calls and results in real-time,
showing when the agent uses backend tools and what results it receives.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent, FunctionCallContent, FunctionResultContent
from agent_framework_ag_ui import AGUIChatClient


async def main():
    """Main client loop with tool event display."""
    # Get server URL from environment or use default
    server_url = os.environ.get("AGUI_SERVER_URL", "http://127.0.0.1:8888/")
    print(f"🔌 Connecting to AG-UI server at: {server_url}\n")

    # Create AG-UI chat client that connects to the server
    chat_client = AGUIChatClient(endpoint=server_url)

    # Create agent with the chat client
    agent = ChatAgent(
        name="ClientAgent",
        chat_client=chat_client,
        instructions="You are a helpful assistant.",
    )

    # Get a thread for conversation continuity
    thread = agent.get_new_thread()

    print("💬 AG-UI Client - Interactive Chat with Tool Display")
    print("=" * 60)
    print("Type your messages and press Enter.")
    print("Type ':q' or 'quit' to exit.")
    print("\nTry asking about:")
    print("  - Weather: 'What's the weather in Paris?'")
    print("  - Restaurants: 'Find Italian restaurants in London'")
    print("  - Math: 'Calculate 123 * 456'")
    print("  - Time: 'What time is it in Tokyo?'\n")

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
            
            current_tool_name = None
            accumulated_args = ""
            
            async for update in agent.run_stream(message, thread=thread):
                # Display text content
                if update.text:
                    print(f"\033[96m{update.text}\033[0m", end="", flush=True)

                # Display tool calls and results
                for content in update.contents:
                    if isinstance(content, FunctionCallContent):
                        # Tool call started or updated
                        if current_tool_name != content.name:
                            # New tool call
                            current_tool_name = content.name
                            accumulated_args = ""
                            print(f"\n\n  \033[95m🔧 Calling tool: {content.name}\033[0m")
                        
                        # Accumulate arguments (they stream in chunks)
                        if content.arguments:
                            accumulated_args += str(content.arguments)
                        
                    elif isinstance(content, FunctionResultContent):
                        # Display accumulated arguments before result
                        if accumulated_args:
                            print(f"  \033[95m📋 Arguments: {accumulated_args}\033[0m")
                        
                        print(f"  \033[93m⏳ Executed\033[0m")
                        
                        if content.exception:
                            print(f"  \033[91m❌ Error: {content.exception}\033[0m\n")
                        else:
                            # Format result nicely
                            result_str = str(content.result)
                            if len(result_str) > 200:
                                result_str = result_str[:200] + "..."
                            print(f"  \033[92m✅ Result: {result_str}\033[0m\n")
                        
                        # Reset for next tool call
                        current_tool_name = None
                        accumulated_args = ""
                        
                        print("\033[1;32mAssistant:\033[0m ", end="", flush=True)

            print("\n")

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n\033[91m❌ An error occurred: {e}\033[0m")


if __name__ == "__main__":
    asyncio.run(main())
