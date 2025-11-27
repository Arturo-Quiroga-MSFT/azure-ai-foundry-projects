"""AG-UI server with configurable Azure provider support.

This server supports both Azure OpenAI and Azure AI Foundry, selectable via
environment variable. This allows you to:
- Switch between providers without code changes
- Compare behavior across different Azure AI services
- Deploy the same code to different environments
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import ChatAgent
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from fastapi import FastAPI

# Provider selection
ProviderType = Literal["azure-openai", "azure-ai"]
provider: ProviderType = os.environ.get("AZURE_PROVIDER", "azure-openai")  # type: ignore

print(f"\n🔧 Configuring provider: {provider}")

if provider == "azure-openai":
    # Azure OpenAI Configuration
    from agent_framework.azure import AzureOpenAIChatClient
    from azure.identity import AzureCliCredential
    
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        raise ValueError(
            "For Azure OpenAI, set: AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME"
        )
    
    chat_client = AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        endpoint=endpoint,
        deployment_name=deployment_name,
    )
    
    model_info = f"Azure OpenAI - {deployment_name}"
    endpoint_info = endpoint

elif provider == "azure-ai":
    # Azure AI Foundry Configuration
    from agent_framework.azure import AzureAIChatClient
    from azure.ai.inference import ChatCompletionsClient
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential
    
    endpoint = os.environ.get("AZURE_AI_ENDPOINT")
    api_key = os.environ.get("AZURE_AI_API_KEY")
    
    if not endpoint:
        raise ValueError("For Azure AI, set: AZURE_AI_ENDPOINT")
    
    # Use API key or managed identity
    if api_key:
        inference_client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        auth_method = "API Key"
    else:
        inference_client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        auth_method = "Managed Identity"
    
    chat_client = AzureAIChatClient(client=inference_client)
    
    model_info = f"Azure AI Foundry ({auth_method})"
    endpoint_info = endpoint

else:
    raise ValueError(
        f"Unknown provider: {provider}. Use 'azure-openai' or 'azure-ai'"
    )

# Create the AI agent (same code for both providers!)
agent = ChatAgent(
    name="AGUIAssistant",
    instructions="You are a helpful assistant.",
    chat_client=chat_client,
)

# Create FastAPI app
app = FastAPI(title=f"AG-UI Server - {provider}")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print(f"\n🚀 Starting AG-UI Server...")
    print(f"🤖 Provider: {model_info}")
    print(f"📡 Endpoint: {endpoint_info}")
    print(f"🌐 Server URL: http://127.0.0.1:8888/\n")
    print("💡 Switch providers with: export AZURE_PROVIDER=azure-openai|azure-ai\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8888)
