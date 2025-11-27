"""AG-UI server with backend tool rendering.

This server demonstrates function tools executed on the backend.
The AI agent can call these tools to perform tasks like:
- Getting weather information
- Searching for restaurants
- Performing calculations

Tool calls and results are automatically streamed to the client.
"""

import os
from typing import Annotated, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI
from pydantic import Field


# ========================================
# Backend Function Tools
# ========================================

@ai_function
def get_weather(
    location: Annotated[str, Field(description="The city and country, e.g., 'Paris, France'")],
) -> str:
    """Get the current weather for a location.
    
    Use this tool when the user asks about weather conditions, temperature,
    or climate in a specific location.
    """
    # Simulated weather data - in production, call a real weather API
    weather_data = {
        "Paris, France": "sunny, 22°C",
        "London, UK": "cloudy, 15°C",
        "New York, USA": "rainy, 18°C",
        "Tokyo, Japan": "clear, 25°C",
        "Sydney, Australia": "partly cloudy, 20°C",
    }
    
    weather = weather_data.get(location, "sunny, 20°C")
    return f"The weather in {location} is {weather}."


@ai_function
def search_restaurants(
    location: Annotated[str, Field(description="The city to search in")],
    cuisine: Annotated[str, Field(description="Type of cuisine (e.g., Italian, Japanese, Mexican)")] = "any",
    max_results: Annotated[int, Field(description="Maximum number of results to return")] = 3,
) -> dict[str, Any]:
    """Search for restaurants in a specific location.
    
    Use this tool when the user wants to find restaurants, dining options,
    or food recommendations in a particular area.
    """
    # Simulated restaurant data
    restaurants = [
        {"name": "The Golden Fork", "cuisine": "Italian", "rating": 4.5, "price": "$$"},
        {"name": "Bella Italia", "cuisine": "Italian", "rating": 4.2, "price": "$$$"},
        {"name": "Sushi Master", "cuisine": "Japanese", "rating": 4.7, "price": "$$$"},
        {"name": "Taco Fiesta", "cuisine": "Mexican", "rating": 4.3, "price": "$"},
        {"name": "Spice Garden", "cuisine": "Indian", "rating": 4.6, "price": "$$"},
        {"name": "Green Leaf", "cuisine": "Vegetarian", "rating": 4.4, "price": "$$"},
    ]
    
    # Filter by cuisine if specified
    if cuisine.lower() != "any":
        filtered = [r for r in restaurants if cuisine.lower() in r["cuisine"].lower()]
    else:
        filtered = restaurants
    
    # Limit results
    filtered = filtered[:max_results]
    
    return {
        "location": location,
        "cuisine": cuisine,
        "count": len(filtered),
        "results": filtered,
    }


@ai_function
def calculate(
    expression: Annotated[str, Field(description="Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')")],
) -> str:
    """Perform mathematical calculations.
    
    Use this tool when the user asks for arithmetic operations, mathematical
    computations, or needs to calculate numbers.
    """
    try:
        # Safe evaluation of mathematical expressions
        # WARNING: In production, use a proper math parser library like numexpr
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@ai_function
def get_current_time(
    timezone: Annotated[str, Field(description="Timezone (e.g., 'UTC', 'America/New_York', 'Europe/Paris')")] = "UTC",
) -> str:
    """Get the current time in a specific timezone.
    
    Use this tool when the user asks about the current time, what time it is,
    or needs to know the time in a specific location.
    """
    from datetime import datetime
    import pytz
    
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        return f"Error getting time for timezone '{timezone}': {str(e)}"


# ========================================
# Server Configuration
# ========================================

# Read required configuration from environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

if not endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
if not deployment_name:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME environment variable is required")

# Create Azure OpenAI chat client
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    deployment_name=deployment_name,
)

# Create the AI agent with tools
agent = ChatAgent(
    name="ToolAssistant",
    instructions="""You are a helpful assistant with access to several tools.
    
Use the available tools when appropriate:
- get_weather: For weather information
- search_restaurants: For finding dining options
- calculate: For mathematical operations
- get_current_time: For time information

Always use tools when the user asks about these topics. Provide natural,
conversational responses that incorporate the tool results.""",
    chat_client=chat_client,
    tools=[get_weather, search_restaurants, calculate, get_current_time],
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server with Backend Tools")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print("\n🚀 Starting AG-UI Server with Backend Tools...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment_name}")
    print(f"🔧 Tools: get_weather, search_restaurants, calculate, get_current_time")
    print(f"🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
