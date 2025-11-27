"""Hosted Agent Implementation for Azure AI Foundry.

This module implements a hosted agent using LangGraph and Azure OpenAI,
following the official Azure AI Agent Server pattern.
"""

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from azure.ai.agentserver.langgraph import from_langgraph
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables
load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using wttr.in API.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string describing the current weather
    """
    import requests
    try:
        # Use wttr.in API for real weather data
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t", timeout=5)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Could not fetch weather for {city}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression.
    
    Args:
        expression: A mathematical expression as a string (e.g., "2 + 2", "10 * 5")
        
    Returns:
        The result of the calculation as a string
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# Define available tools
tools = [get_weather, calculator]

# Initialize Azure OpenAI model with managed identity authentication
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-5-mini")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

print(f"Connecting to: {azure_endpoint}")
print(f"Deployment: {deployment_name}")
print(f"API Version: {api_version}")

# Use API key if provided, otherwise use DefaultAzureCredential (service principal)
if api_key:
    model = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        model=deployment_name,
        api_version=api_version,
        api_key=api_key
    )
else:
    # Use service principal credentials from environment variables
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, 
        "https://cognitiveservices.azure.com/.default"
    )
    model = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        model=deployment_name,
        api_version=api_version,
        azure_ad_token_provider=token_provider
    )

# Create the LangGraph agent
agent = create_react_agent(model, tools)

if __name__ == "__main__":
    # Host the agent on http://localhost:8088
    print("Starting Hosted Agent on http://localhost:8088")
    print(f"Model: {deployment_name}")
    print(f"Available tools: {', '.join([t.name for t in tools])}")
    print("\nTest with:")
    print('curl -X POST http://localhost:8088/responses \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"agent": {"name": "local_agent", "type": "agent_reference"}, "stream": false, "input": "What is the weather in Seattle?"}\'')
    
    from_langgraph(agent).run()
