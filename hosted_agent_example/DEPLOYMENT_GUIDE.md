# Hosted Agent Deployment Guide

This guide walks you through deploying a hosted agent to Azure AI Foundry using the Python SDK.

## Prerequisites

Before deploying, ensure you have:

1. **Azure Container Registry (ACR) with your agent image**
   ```bash
   # Build and push your Docker image
   docker build -t my-hosted-agent:v1 .
   az acr login --name aqmlacr001
   docker tag my-hosted-agent:v1 aqmlacr001.azurecr.io/my-hosted-agent:v1
   docker push aqmlacr001.azurecr.io/my-hosted-agent:v1
   ```

2. **ACR Permissions configured**
   - Your Azure AI Foundry project's managed identity needs the `Container Registry Repository Reader` role on the ACR
   - Find your project's managed identity in the Azure Portal:
     1. Go to your AI Foundry project resource
     2. Navigate to **Identity** → **System assigned**
     3. Copy the **Object (principal) ID**
   - Assign the role in ACR:
     ```bash
     # Get the managed identity principal ID
     PRINCIPAL_ID="<your-managed-identity-object-id>"
     
     # Assign the role
     az role assignment create \
       --assignee $PRINCIPAL_ID \
       --role "AcrPull" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/<rg-name>/providers/Microsoft.ContainerRegistry/registries/aqmlacr001"
     ```

3. **Azure AI Projects SDK installed**
   ```bash
   pip install azure-ai-projects azure-identity
   ```

4. **Azure CLI authentication**
   ```bash
   az login
   ```

## Deployment Steps

### 1. Deploy the Agent

Run the deployment script:

```bash
python deploy_simple.py
```

This script will:
- Connect to your Azure AI Foundry project
- Create a hosted agent version with your container image
- Configure CPU, memory, and environment variables
- Initiate the deployment

### 2. Monitor Deployment

The deployment happens in the background. You can:

**Option A: Check via Azure Portal**
1. Go to [https://ai.azure.com](https://ai.azure.com)
2. Navigate to your project → **Agents**
3. Find your agent and check the deployment status
4. Click "view deployment logs" if there are issues

**Option B: Check via Python script**
```bash
python check_deployment.py
```

### 3. Test the Agent

Once deployed, test the agent using the OpenAI SDK:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"

client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
agent = client.agents.retrieve(agent_name="my-hosted-agent")

openai_client = client.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "What's the weather in Seattle?"}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}}
)

print(response.output_text)
```

## Configuration Details

The agent is deployed with:

- **CPU**: 1 core
- **Memory**: 2Gi
- **Protocol**: Responses API v1
- **Environment Variables**:
  - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
  - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`: Model deployment name (e.g., gpt-5-mini)
  - `AZURE_OPENAI_API_VERSION`: API version (e.g., 2025-04-01-preview)

## Troubleshooting

### Common Issues

1. **SubscriptionIsNotRegistered (400)**
   - Register the required resource provider
   - Solution: `az provider register --namespace Microsoft.CognitiveServices`

2. **InvalidAcrPullCredentials (401)**
   - Managed identity doesn't have ACR access
   - Solution: Assign the `AcrPull` or `Container Registry Repository Reader` role

3. **AcrImageNotFound (404)**
   - Container image doesn't exist or wrong name/tag
   - Solution: Verify image exists: `az acr repository show-tags --name aqmlacr001 --repository my-hosted-agent`

4. **RegistryNotFound (400/404)**
   - ACR name is incorrect or not accessible
   - Solution: Check ACR name and network settings

## Managing the Agent

### Update Agent (Create New Version)

To update the agent with a new container image or configuration:

```python
agent = client.agents.create_version(
    agent_name="my-hosted-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[...],
        cpu="2",  # Updated
        memory="4Gi",  # Updated
        image="aqmlacr001.azurecr.io/my-hosted-agent:v2",  # New version
        environment_variables={...}
    )
)
```

### Delete Agent

```python
client.agents.delete_agent(agent_name="my-hosted-agent")
```

## Learn More

- [Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry)
- [Azure AI Projects SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme)
- [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)
