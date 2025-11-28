"""AG-UI Server with Magentic Orchestration Pattern.

Note: This is a simplified demonstration showing the conceptual approach.
The full Magentic orchestration API is still evolving in agent-framework.

For now, we demonstrate intelligent multi-agent coordination where different
specialized agents handle different aspects of complex queries.
"""

import os
import sys
import io
import base64
from typing import Annotated
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import DefaultAzureCredential, AzureCliCredential
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
import httpx
from tavily import TavilyClient
import os

# Determine which credential to use based on environment
# In Azure Container Apps, use DefaultAzureCredential (managed identity)
# In local development, use AzureCliCredential
def get_azure_credential():
    """Get the appropriate Azure credential based on environment."""
    if os.getenv("WEBSITE_INSTANCE_ID") or os.getenv("CONTAINER_APP_NAME"):
        # Running in Azure (App Service or Container Apps)
        print("🔐 Using DefaultAzureCredential (Managed Identity)")
        return DefaultAzureCredential()
    else:
        # Running locally
        print("🔐 Using AzureCliCredential (Local Development)")
        return AzureCliCredential()

# Global storage for images
image_storage = {}


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
        icon = data["weather"][0]["icon"]
        
        return f"""🌤️ **Weather in {location}**

**Temperature:** {temp}°C (feels like {feels_like}°C)
**Conditions:** {description.title()}
**Humidity:** {humidity}%
**Wind Speed:** {wind_speed} m/s

[WEATHER_ICON]https://openweathermap.org/img/wn/{icon}@2x.png[/WEATHER_ICON]"""
    except Exception as e:
        return f"Error getting weather: {str(e)}"


@ai_function
def web_search(
    query: Annotated[str, Field(description="The search query")],
    max_results: Annotated[int, Field(description="Maximum number of results")] = 5,
) -> str:
    """Search the web for current information."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Tavily API key not configured."
    
    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query=query, max_results=max_results)
        
        result_text = f"🔍 **Web Search Results for:** {query}\n\n"
        
        for idx, result in enumerate(response.get("results", []), 1):
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")
            
            result_text += f"**{idx}. {title}**\n"
            result_text += f"{content}\n"
            result_text += f"[LINK]{url}[/LINK]\n\n"
        
        return result_text
    except Exception as e:
        return f"Error performing web search: {str(e)}"


@ai_function
def calculate(
    expression: Annotated[str, Field(description="Mathematical expression to evaluate")],
) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"""🔢 **Calculation**

**Expression:** `{expression}`
**Result:** `{result}`

[CALC_RESULT]{result}[/CALC_RESULT]"""
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


@ai_function
def execute_python_code(
    code: Annotated[str, Field(description="Python code to execute for data analysis or visualization")],
    description: Annotated[str, Field(description="Brief description of what the code does")] = "",
) -> str:
    """Execute Python code for data analytics and visualization."""
    try:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        exec_globals = {"__builtins__": __builtins__}
        
        try:
            import numpy as np
            import pandas as pd
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            exec_globals.update({
                "np": np, "numpy": np,
                "pd": pd, "pandas": pd,
                "plt": plt, "matplotlib": matplotlib,
                "sns": sns, "seaborn": sns,
            })
        except ImportError:
            pass
        
        exec(code, exec_globals)
        
        output = sys.stdout.getvalue()
        errors = sys.stderr.getvalue()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        images = []
        if 'plt' in exec_globals:
            try:
                fig_nums = plt.get_fignums()
                for fig_num in fig_nums:
                    fig = plt.figure(fig_num)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                    buf.seek(0)
                    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                    images.append(img_base64)
                    buf.close()
                plt.close('all')
            except Exception as e:
                errors += f"\nError capturing plot: {str(e)}"
        
        result = f"📊 **Code Execution Result**\n\n"
        
        if description:
            result += f"**Task:** {description}\n\n"
        
        if output:
            result += f"**Output:**\n```\n{output}\n```\n\n"
        
        if errors:
            result += f"**Warnings:**\n```\n{errors}\n```\n\n"
        
        # Store images and return references
        for idx, img_data in enumerate(images, 1):
            img_id = str(uuid.uuid4())
            image_storage[img_id] = img_data
            result += f"[IMAGE_ID]{img_id}[/IMAGE_ID]\n\n"
        
        if not output and not images and not errors:
            result += "Code executed successfully (no output).\n"
        
        return result
        
    except Exception as e:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        return f"❌ **Execution Error**\n\n```\n{str(e)}\n```"


# ============================================================================
# AZURE OPENAI CLIENT SETUP
# ============================================================================

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

if not endpoint or not deployment_name:
    raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME required")

chat_client = AzureOpenAIChatClient(
    credential=get_azure_credential(),
    endpoint=endpoint,
    deployment_name=deployment_name,
)


# ============================================================================
# ORCHESTRATOR AGENT (Simplified Magentic-Style Coordination)
# ============================================================================

# Note: Full Magentic API with StandardMagenticManager is still evolving.
# This demonstrates intelligent multi-agent coordination concepts.

orchestrator_agent = ChatAgent(
    chat_client=chat_client,
    model="gpt-4.1-mini",
    name="OrchestratorAgent",
    description="Intelligent orchestrator coordinating specialized capabilities for weather, research, and data analysis",
    instructions="""You are an intelligent orchestrator that coordinates different specialized capabilities:

**Your Capabilities**:

1. **Weather Information** (via get_weather)
   - Real-time weather data for any location
   - Temperature, conditions, humidity, wind, etc.

2. **Web Research** (via web_search)  
   - Current information, news, trends
   - Up-to-date facts from the web

3. **Mathematical Calculations** (via calculate)
   - Evaluate mathematical expressions
   - Quick computations

4. **Data Analysis & Visualization** (via execute_python_code)
   - Create charts, plots, visualizations with matplotlib
   - Data analytics with numpy, pandas, seaborn
   - Complex data processing

**Multi-Step Coordination**:

When queries require multiple capabilities, coordinate them intelligently:

Example: "Research weather in Paris and London, then compare them in a chart"
1. get_weather("Paris")
2. get_weather("London")
3. execute_python_code to create comparison visualization

Example: "Find latest AI trends and visualize adoption rates"
1. web_search for AI trends
2. execute_python_code to create charts from data

Example: "What's the weather in Tokyo and can you plot the temperature trend?"
1. get_weather("Tokyo")
2. execute_python_code to visualize temperature

**Image Handling - CRITICAL INSTRUCTIONS**:
🚨 When execute_python_code returns [IMAGE_ID]...[/IMAGE_ID] markers:
- You MUST copy the ENTIRE marker with ALL its content character-by-character
- NEVER write just "[IMAGE_ID]" - you must include the full [IMAGE_ID]uuid[/IMAGE_ID]
- Do NOT modify, truncate, summarize, or paraphrase the UUID
- Do NOT say "here's the image" without including the actual marker
- The [IMAGE_ID] marker contains a UUID that must be preserved exactly
- Example: If you receive [IMAGE_ID]abc-123[/IMAGE_ID], include that EXACT text

**Rich Content Markers - PRESERVE EXACTLY**:
- [WEATHER_ICON]...data...[/WEATHER_ICON] from get_weather
- [LINK]...data...[/LINK] from web_search  
- [CALC_RESULT]...data...[/CALC_RESULT] from calculate
- [IMAGE_ID]...uuid...[/IMAGE_ID] from execute_python_code

**Personality**:
- Be conversational and friendly
- Explain what you're doing as you work
- Show your coordination process
- Present results clearly with rich formatting

Remember: You're demonstrating Magentic-style orchestration - dynamically coordinating
specialized capabilities to solve complex, multi-step queries!""",
    tools=[get_weather, web_search, calculate, execute_python_code],
)

print("✅ Orchestrator agent created (Magentic-style coordination)")
print("   Coordinates: weather, research, calculations, visualizations")




# ========================================
# FastAPI Server
# ========================================

app = FastAPI(title="AG-UI Magentic Orchestration Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Image retrieval endpoint
@app.get("/images/{image_id}")
async def get_image(image_id: str):
    """Retrieve a generated image by ID."""
    from fastapi.responses import Response
    if image_id in image_storage:
        import base64
        img_bytes = base64.b64decode(image_storage[image_id])
        return Response(content=img_bytes, media_type="image/png")
    return {"error": "Image not found"}, 404

# Register the orchestrator agent as the main AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, orchestrator_agent, "/")


if __name__ == "__main__":
    import uvicorn

    print("\n🎯 Starting AG-UI Server with Magentic-Style Orchestration...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment_name}")
    print("\n🧠 Orchestrator coordinates:")
    print("   - Weather queries (OpenWeatherMap API)")
    print("   - Web research (Tavily API)")
    print("   - Mathematical calculations")
    print("   - Data analysis & visualizations (matplotlib, pandas, numpy)")
    print("\n💡 Try multi-step queries like:")
    print("   'Research weather in Paris and London, then create a comparison chart'")
    print("   'Find latest AI trends and visualize adoption rates'")
    print(f"\n🚀 Starting server on http://127.0.0.1:8888")
    print("   Open http://localhost:3000 in your browser for the UI\n")

    uvicorn.run(app, host="127.0.0.1", port=8888)
    print(f"\n🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
