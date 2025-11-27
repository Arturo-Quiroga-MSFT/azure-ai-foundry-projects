"""AG-UI server example with Azure AI Foundry.

This server uses Azure AI Foundry (formerly Azure AI Studio) inference endpoints
instead of Azure OpenAI. This is useful for:
- Using models deployed in Azure AI Foundry projects
- Accessing models from the Azure AI model catalog
- Unified inference API across different model providers
"""

import os

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from fastapi import FastAPI

# Read required configuration from environment variables
endpoint = os.environ.get("AZURE_AI_ENDPOINT")
api_key = os.environ.get("AZURE_AI_API_KEY")  # Optional, can use managed identity instead

if not endpoint:
    raise ValueError("AZURE_AI_ENDPOINT environment variable is required")

# Create Azure AI inference client
# Option 1: Use API key if provided
if api_key:
    inference_client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )
    auth_method = "API Key"
# Option 2: Use managed identity/DefaultAzureCredential
else:
    inference_client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    )
    auth_method = "Managed Identity/DefaultAzureCredential"

# Create Azure AI chat client wrapper
chat_client = AzureAIChatClient(client=inference_client)

# Create the AI agent with basic instructions
agent = ChatAgent(
    name="AGUIAssistant",
    instructions="You are a helpful assistant.",
    chat_client=chat_client,
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server Demo - Azure AI")

# Register the AG-UI endpoint at root path
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print("\n🚀 Starting AG-UI Server with Azure AI Foundry...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🔐 Auth: {auth_method}")
    print(f"🌐 Server URL: http://127.0.0.1:8888/\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
