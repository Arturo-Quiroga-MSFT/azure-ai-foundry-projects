"""AG-UI server example with Azure OpenAI.

This server hosts an AI agent accessible via HTTP using the AG-UI protocol.
It uses FastAPI for HTTP handling and streams responses via Server-Sent Events (SSE).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI

# Read required configuration from environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

if not endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
if not deployment_name:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME environment variable is required")

# Create Azure OpenAI chat client with CLI credential authentication
chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    deployment_name=deployment_name,
)

# Create the AI agent with basic instructions
agent = ChatAgent(
    name="AGUIAssistant",
    instructions="You are a helpful assistant.",
    chat_client=chat_client,
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server Demo")

# Register the AG-UI endpoint at root path
# This automatically handles SSE streaming and request/response conversion
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print("\n🚀 Starting AG-UI Server...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment_name}")
    print(f"🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
