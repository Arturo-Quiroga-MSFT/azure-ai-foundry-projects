"""AG-UI client with frontend tool rendering.

This client demonstrates frontend tools - functions that execute on the client side
but are orchestrated by the server-side agent. The agent decides when to call these
tools, but they execute locally with access to client-specific resources.

Frontend tools are useful for:
- Accessing local device information (GPS, sensors)
- Reading client-side storage or preferences
- Performing UI operations
- Interacting with device-specific features
"""

import asyncio
import os
import json
from typing import Annotated, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent, FunctionCallContent, FunctionResultContent, ai_function
from agent_framework_ag_ui import AGUIChatClient
from pydantic import Field


# ========================================
# Frontend Function Tools (Client-Side)
# ========================================

@ai_function
def get_user_location() -> dict[str, Any]:
    """Get the user's current GPS location.
    
    Returns the user's latitude, longitude, and approximate city.
    Use this when the user asks about their location or needs location-based services.
    """
    try:
        # Option 1: IP-based geolocation (simple, works everywhere)
        import requests
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "accuracy_meters": 1000.0,  # IP-based is less accurate
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country_name"),
                "method": "IP-based geolocation",
            }
    except Exception as e:
        print(f"⚠️  IP geolocation failed: {e}")
    
    # Fallback: simulated location for Toronto
    return {
        "latitude": 43.6532,
        "longitude": -79.3832,
        "accuracy_meters": 10.0,
        "city": "Toronto",
        "province": "Ontario",
        "country": "Canada",
        "method": "fallback (simulated)",
    }


@ai_function
def read_local_preferences() -> dict[str, Any]:
    """Read user preferences from local storage.
    
    Returns user's saved preferences like theme, language, notifications, etc.
    Use this when you need to know the user's personal settings.
    """
    # Simulated local storage - in production, would read from actual local storage
    return {
        "theme": "dark",
        "language": "en",
        "notifications_enabled": True,
        "preferred_temperature_unit": "celsius",
        "preferred_currency": "CAD",
        "timezone": "America/Toronto",
    }


@ai_function
def get_device_info() -> dict[str, Any]:
    """Get information about the user's device.
    
    Returns device type, OS, screen size, battery level, etc.
    Use this when context about the user's device is relevant.
    """
    import platform
    
    # Get actual device information
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


@ai_function
def show_notification(
    title: Annotated[str, Field(description="Notification title")],
    message: Annotated[str, Field(description="Notification message")],
    urgency: Annotated[str, Field(description="Urgency level: low, normal, high")] = "normal",
) -> str:
    """Display a notification to the user.
    
    Shows a desktop/system notification with the given title and message.
    Use this when you need to alert the user about something important.
    """
    # Simulated notification - in production, would use actual notification system
    urgency_emoji = {"low": "ℹ️", "normal": "📢", "high": "⚠️"}
    emoji = urgency_emoji.get(urgency, "📢")
    
    print(f"\n{emoji} NOTIFICATION [{urgency.upper()}]")
    print(f"   Title: {title}")
    print(f"   Message: {message}\n")
    
    return f"Notification displayed: {title}"


# ========================================
# Tool Registry (Maps names to functions)
# ========================================

FRONTEND_TOOLS = {
    "get_user_location": get_user_location,
    "read_local_preferences": read_local_preferences,
    "get_device_info": get_device_info,
    "show_notification": show_notification,
}


async def main():
    """Main client loop with frontend tools."""
    # Get server URL from environment or use default
    server_url = os.environ.get("AGUI_SERVER_URL", "http://127.0.0.1:8888/")
    print(f"🔌 Connecting to AG-UI server at: {server_url}\n")

    # Create AG-UI chat client
    chat_client = AGUIChatClient(endpoint=server_url)

    # Create agent with the chat client AND frontend tools
    agent = ChatAgent(
        name="FrontendToolClient",
        chat_client=chat_client,
        instructions="You are a helpful assistant.",
        tools=list(FRONTEND_TOOLS.values()),  # Register frontend tools with the agent
    )

    # Get a thread for conversation continuity
    thread = agent.get_new_thread()

    print("💬 AG-UI Client - Frontend Tools Demo")
    print("=" * 60)
    print("Type your messages and press Enter.")
    print("Type ':q' or 'quit' to exit.")
    print("\nTry asking about:")
    print("  - Location: 'Where am I?' or 'What's my current location?'")
    print("  - Preferences: 'What are my preferences?'")
    print("  - Device: 'What device am I using?'")
    print("  - Notifications: 'Remind me to take a break'\n")

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

                # Display tool calls and execute frontend tools
                for content in update.contents:
                    if isinstance(content, FunctionCallContent):
                        # Tool call started or updated
                        if current_tool_name != content.name:
                            # New tool call
                            current_tool_name = content.name
                            accumulated_args = ""
                            print(f"\n\n  \033[95m🔧 Frontend Tool: {content.name}\033[0m")
                        
                        # Accumulate arguments (they stream in chunks)
                        if content.arguments:
                            accumulated_args += str(content.arguments)
                        
                    elif isinstance(content, FunctionResultContent):
                        # Display accumulated arguments
                        if accumulated_args:
                            try:
                                args_dict = json.loads(accumulated_args)
                                print(f"  \033[95m📋 Arguments: {args_dict}\033[0m")
                            except:
                                print(f"  \033[95m📋 Arguments: {accumulated_args}\033[0m")
                        
                        print(f"  \033[93m⏳ Executing locally...\033[0m")
                        
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
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
