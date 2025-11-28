"""AG-UI Multi-Agent Server with Specialized Agents.

This server demonstrates a multi-agent system where:
- OrchestratorAgent: Routes requests to specialized agents
- ResearchAgent: Handles web search and current information
- WeatherAgent: Handles weather and location queries
- DataAgent: Handles calculations and data processing

Agents can hand off tasks to each other for specialized handling.
"""

import os
from typing import Annotated, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent, ai_function, transfer_to_agent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
import httpx
from tavily import TavilyClient


# ========================================
# Tool Definitions
# ========================================

@ai_function
def get_weather(
    location: Annotated[str, Field(description="The city name, e.g., 'Paris' or 'Toronto'")],
) -> str:
    """Get the current weather for a location."""
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured."
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        return f"Weather in {location}: {description}, {temp}°C (feels like {feels_like}°C), humidity {humidity}%, wind {wind_speed} m/s"
    except Exception as e:
        return f"Error getting weather: {str(e)}"


@ai_function
def web_search(
    query: Annotated[str, Field(description="The search query")],
    max_results: Annotated[int, Field(description="Maximum number of results")] = 5,
) -> dict[str, Any]:
    """Search the web for current information."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return {"error": "Tavily API key not configured."}
    
    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query=query, max_results=max_results)
        
        results = []
        for result in response.get("results", []):
            results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
            })
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results,
        }
    except Exception as e:
        return {"error": f"Error performing web search: {str(e)}"}


@ai_function
def calculate(
    expression: Annotated[str, Field(description="Mathematical expression to evaluate")],
) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@ai_function
def analyze_data(
    data: Annotated[str, Field(description="Data or statistics to analyze")],
) -> str:
    """Analyze data, find patterns, or provide statistical insights."""
    # Simplified data analysis - in production, use pandas, numpy, etc.
    return f"Data analysis: {data}\n\nAnalysis: This would involve statistical computations, trend analysis, and insights generation."


# ========================================
# Specialized Agents
# ========================================

# Read required configuration
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

if not endpoint or not deployment_name:
    raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME required")

# Create chat client
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    deployment_name=deployment_name,
)

# ResearchAgent - Specialized in web search and current information
research_agent = ChatAgent(
    name="ResearchAgent",
    instructions="""You are a research specialist with expertise in finding and analyzing current information.

Your capabilities:
- Search the web for latest news, trends, and information
- Provide well-sourced, up-to-date answers
- Cite your sources and explain findings clearly

When you receive a query:
1. Use web_search to find current information
2. Analyze and synthesize the results
3. Provide a comprehensive answer with sources

Be thorough, accurate, and always cite where information comes from.""",
    chat_client=chat_client,
    tools=[web_search],
)

# WeatherAgent - Specialized in weather and location information
weather_agent = ChatAgent(
    name="WeatherAgent",
    instructions="""You are a weather and location specialist.

Your capabilities:
- Provide current weather conditions for any location
- Explain weather patterns and forecasts
- Give location-specific advice based on weather

When you receive a weather query:
1. Use get_weather to fetch current conditions
2. Provide a clear, conversational explanation
3. Add helpful context (e.g., "Great weather for outdoor activities!")

Be friendly and helpful with weather information.""",
    chat_client=chat_client,
    tools=[get_weather],
)

# DataAgent - Specialized in calculations and data analysis
data_agent = ChatAgent(
    name="DataAgent",
    instructions="""You are a data and mathematics specialist.

Your capabilities:
- Perform mathematical calculations
- Analyze data and find patterns
- Provide statistical insights

When you receive a calculation or data query:
1. Use calculate for mathematical operations
2. Use analyze_data for data interpretation
3. Explain your work step-by-step
4. Provide clear, accurate results

Be precise and thorough in your analysis.""",
    chat_client=chat_client,
    tools=[calculate, analyze_data],
)

# OrchestratorAgent - Routes requests to specialists
orchestrator_agent = ChatAgent(
    name="OrchestratorAgent",
    instructions="""You are an intelligent orchestrator that routes user requests to specialized agents.

Available specialists:
- ResearchAgent: Web search, current events, news, general information lookup
- WeatherAgent: Weather conditions, forecasts, location-based weather info
- DataAgent: Calculations, math operations, data analysis, statistics

Your job:
1. Analyze the user's request
2. For specialized queries, use transfer functions to hand off to the right agent
3. For simple queries, use tools directly

Transfer guidelines:
- Complex weather analysis → transfer_to_weather_agent()
- Research tasks requiring multiple sources → transfer_to_research_agent()
- Complex calculations or data analysis → transfer_to_data_agent()
- Simple tool calls → Handle yourself

Be friendly and explain when you're transferring to a specialist.""",
    chat_client=chat_client,
    tools=[get_weather, web_search, calculate, analyze_data],
)


# ========================================
# Transfer Functions (Agent Handoffs)
# ========================================

@ai_function
def transfer_to_research_agent() -> str:
    """Transfer the conversation to the Research Agent for web search and analysis tasks.
    
    Use this when the user needs:
    - Current news or events
    - In-depth research on a topic
    - Multiple source verification
    - Fact-checking
    """
    transfer_to_agent(research_agent)
    return "Transferring to ResearchAgent..."


@ai_function
def transfer_to_weather_agent() -> str:
    """Transfer the conversation to the Weather Agent for weather and location queries.
    
    Use this when the user needs:
    - Detailed weather analysis
    - Weather forecasts
    - Location-specific conditions
    - Weather-related advice
    """
    transfer_to_agent(weather_agent)
    return "Transferring to WeatherAgent..."


@ai_function
def transfer_to_data_agent() -> str:
    """Transfer the conversation to the Data Agent for calculations and analysis.
    
    Use this when the user needs:
    - Complex mathematical calculations
    - Data analysis and interpretation
    - Statistical insights
    - Pattern recognition in data
    """
    transfer_to_agent(data_agent)
    return "Transferring to DataAgent..."


# Add transfer functions to orchestrator
orchestrator_agent.tools.extend([
    transfer_to_research_agent,
    transfer_to_weather_agent,
    transfer_to_data_agent,
])


# ========================================
# Server Configuration
# ========================================

app = FastAPI(title="AG-UI Multi-Agent Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the orchestrator agent as the main endpoint
# In a more advanced setup, you could have separate endpoints for each agent
add_agent_framework_fastapi_endpoint(app, orchestrator_agent, "/")


if __name__ == "__main__":
    import uvicorn

    print("\n🚀 Starting AG-UI Multi-Agent Server...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment_name}")
    print("\n👥 Available Agents:")
    print("   - OrchestratorAgent: Main coordinator")
    print("   - ResearchAgent: Web search & analysis")
    print("   - WeatherAgent: Weather & location info")
    print("   - DataAgent: Calculations & data analysis")
    print(f"\n🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
