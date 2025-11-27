# Real Hosted Agent for Azure AI Foundry

This is a complete example of a **hosted agent** (not a declarative agent) built using LangGraph and deployed as a containerized application on Azure AI Foundry Agent Service.

## 🏗️ Architecture

```
User Request
    ↓
Azure AI Foundry Agent Service
    ↓
Docker Container (this agent)
    ↓
agent_implementation.py
    ├── LangGraph ReAct Agent
    ├── Azure OpenAI (gpt-4o)
    ├── Custom Tools (weather, calculator)
    └── Foundry MCP Tools
```

## 📋 Prerequisites

- Python 3.11+
- Docker Desktop
- Azure CLI
- Azure subscription with:
  - Azure AI Foundry project
  - Azure Container Registry (ACR)
  - Model deployment (gpt-4o or similar)
  - Azure AI User role on the project

## 🚀 Quick Start

### 1. Local Development and Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Azure credentials

# Run locally (hosts on http://localhost:8088)
python agent_implementation.py
```

### 2. Test Locally with cURL

```bash
# Test the agent
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {
          "role": "user",
          "content": "What is the weather in Seattle?"
        }
      ]
    }
  }'
```

### 3. Build Docker Container

```bash
# Build the Docker image
docker build -t my-hosted-agent:v1 .

# Test the container locally
docker run -p 8088:8088 \
  -e AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o \
  -e AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
  my-hosted-agent:v1
```

### 4. Push to Azure Container Registry

```bash
# Login to your ACR
az acr login --name myregistry

# Tag the image
docker tag my-hosted-agent:v1 myregistry.azurecr.io/my-hosted-agent:v1

# Push to ACR
docker push myregistry.azurecr.io/my-hosted-agent:v1
```

### 5. Configure ACR Permissions

```bash
# Get your project's managed identity
PROJECT_IDENTITY=$(az cognitiveservices account identity show \
  --name aq-ai-foundry-Sweden-Central \
  --resource-group AI-FOUNDRY-RG \
  --query principalId -o tsv)

# Grant ACR pull permissions
az role assignment create \
  --role "AcrPull" \
  --assignee $PROJECT_IDENTITY \
  --scope /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.ContainerRegistry/registries/myregistry
```

### 6. Deploy to Azure AI Foundry

**Option A: Using Azure AI Projects SDK (Recommended)**

```bash
# Install deployment dependencies
pip install azure-ai-projects azure-identity

# Run the deployment script
python deploy_simple.py
```

The script will:
- Connect to your Azure AI Foundry project
- Create a hosted agent version with your container image
- Configure resources (CPU, memory, environment variables)
- Initiate the deployment

Check deployment status:
```bash
python check_deployment.py
```

**Option B: Using Azure Developer CLI (azd)**

```bash
# Install azd if not already installed
curl -fsSL https://aka.ms/install-azd.sh | bash

# Initialize with AI Foundry template
azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic

# Configure for existing project
azd ai agent init --project-id /subscriptions/7a28b21e-0d3e-4435-a686-d92889d4ee96/resourceGroups/AI-FOUNDRY-RG/providers/Microsoft.CognitiveServices/accounts/aq-ai-foundry-Sweden-Central/projects/firstProject

# Deploy
azd up
```

### 7. Test the Deployed Agent

```bash
# Test with provided script
python test_deployed_agent.py
```

Or test manually:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import AgentReference

# Initialize client
client = AIProjectClient(
    endpoint="https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject",
    credential=DefaultAzureCredential()
)

# Get the agent
agent = client.agents.retrieve(agent_name="my-hosted-agent")

# Create conversation and send message
openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "What is the weather in Seattle?"}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}}
)

print(f"Agent response: {response.output_text}")
```

## 📖 Detailed Deployment Guide

For comprehensive deployment instructions, troubleshooting, and management:

👉 **See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**

## 🛠️ Helper Scripts

- `deploy_simple.py` - Deploy the hosted agent to Azure AI Foundry
- `check_deployment.py` - Check the status of a deployed agent
- `test_deployed_agent.py` - Test the deployed agent with sample queries
- `agent_implementation.py` - The agent implementation (runs in container)
- `test_agent.py` - Test the agent locally
```

## 🔧 Customization

### Adding Custom Tools

Edit `agent_implementation.py` and add more tools:

```python
from langchain_core.tools import tool

@tool
def your_custom_tool(param: str) -> str:
    """Description of what your tool does."""
    # Your implementation here
    return "result"

# Add to the custom_tools list in HostedAgent.__init__
self.custom_tools = [get_weather, calculate, your_custom_tool]
```

### Configuring the Model

Modify the model settings in `agent_implementation.py`:

```python
model = AzureChatOpenAI(
    model=self.deployment_name,
    temperature=0.7,  # Adjust creativity (0.0-1.0)
    max_tokens=1000,  # Max response length
    streaming=True    # Enable streaming responses
)
```

## 📊 Monitoring and Observability

### View Traces in Azure Portal

1. Go to your AI Foundry project
2. Navigate to **Traces** tab
3. Filter by agent name

### Local Tracing with AI Toolkit

1. Install AI Toolkit in VS Code
2. Start the collector
3. Set environment variable:
   ```bash
   export OTEL_EXPORTER_ENDPOINT=http://localhost:4318
   ```
4. Run your agent and view traces in AI Toolkit

## 🆚 Hosted Agent vs Declarative Agent

| Feature | This (Hosted) | Declarative |
|---------|---------------|-------------|
| Definition | Python code | YAML config |
| Deployment | Docker container | Portal UI |
| Customization | Unlimited | Limited to built-in tools |
| Complexity | High | Low |
| Frameworks | LangGraph, custom | Built-in only |
| Editing | Code + redeploy | Portal UI |

## 🐛 Troubleshooting

### Agent fails to start
- Check ACR permissions: Ensure managed identity has `AcrPull` role
- Verify image exists: `az acr repository show-tags --name myregistry --repository my-hosted-agent`
- Check environment variables in deployment configuration

### Authentication errors
- Ensure Azure AI User role is assigned
- Verify managed identity is configured
- Check `DefaultAzureCredential` can authenticate

### Can't connect to local agent
- Verify port 8088 is not in use: `lsof -i :8088`
- Check Docker container logs: `docker logs <container-id>`
- Ensure environment variables are set

## 📚 Resources

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Azure Container Registry](https://learn.microsoft.com/azure/container-registry/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)

## 🤝 Contributing

This is an example implementation. Modify it to suit your specific use case!

## 📄 License

MIT License - feel free to use and modify for your projects.
