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
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
import httpx
from tavily import TavilyClient


# ========================================
# Backend Function Tools
# ========================================

@ai_function
def get_weather(
    location: Annotated[str, Field(description="The city name, e.g., 'Paris' or 'Toronto'")],
) -> str:
    """Get the current weather for a location.
    
    Use this tool when the user asks about weather conditions, temperature,
    or climate in a specific location.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured. Please add OPENWEATHER_API_KEY to .env file."
    
    try:
        # Call OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        
        return f"The weather in {location} is {description} with a temperature of {temp}°C (feels like {feels_like}°C). Humidity: {humidity}%."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"City '{location}' not found. Please check the spelling."
        return f"Error fetching weather: {str(e)}"
    except Exception as e:
        return f"Error getting weather data: {str(e)}"


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

@ai_function
def web_search(
    query: Annotated[str, Field(description="The search query to look up on the web")],
    max_results: Annotated[int, Field(description="Maximum number of results to return")] = 5,
) -> dict[str, Any]:
    """Search the web for current information.
    
    Use this tool when the user asks about:
    - Current events, news, or recent developments
    - Information that may have changed recently
    - Topics that require up-to-date information
    - General web searches
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return {"error": "Tavily API key not configured. Please add TAVILY_API_KEY to .env file."}
    
    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query=query, max_results=max_results)
        
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
                "score": result.get("score"),
            })
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"error": f"Error performing web search: {str(e)}"}

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
- get_weather: For real-time weather information from OpenWeatherMap
- search_restaurants: For finding dining options
- calculate: For mathematical operations
- get_current_time: For time information in any timezone
- web_search: For current events, news, and up-to-date information from the web

Always use tools when the user asks about these topics. Provide natural,
conversational responses that incorporate the tool results. When using web_search,
summarize the key findings and cite sources.""",
    chat_client=chat_client,
    tools=[get_weather, search_restaurants, calculate, get_current_time, web_search],
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server with Backend Tools")

# Add CORS middleware to allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print("\n🚀 Starting AG-UI Server with Backend Tools...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment_name}")
    print(f"🔧 Tools: get_weather (OpenWeatherMap), search_restaurants, calculate, get_current_time, web_search (Tavily)")
    print(f"🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
