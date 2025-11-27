# Quick Start: Deploy Hosted Agent to Azure AI Foundry

## What We've Set Up

You now have a complete hosted agent deployment solution with:

1. ✅ **Agent Implementation** (`agent_implementation.py`)
   - LangGraph-based agent with weather and calculator tools
   - Azure OpenAI integration
   - Hosted agent server adapter

2. ✅ **Deployment Script** (`deploy_simple.py`)
   - Programmatic deployment using Azure AI Projects SDK
   - Creates agent version with container image
   - Configures resources and environment variables

3. ✅ **Helper Scripts**
   - `check_deployment.py` - Check agent status
   - `test_deployed_agent.py` - Test the deployed agent
   - `test_agent.py` - Test locally before deployment

4. ✅ **Documentation**
   - `DEPLOYMENT_GUIDE.md` - Comprehensive deployment guide
   - `README.md` - Updated with SDK deployment workflow

## Quick Deploy in 3 Steps

### Step 1: Build and Push Container

```bash
# Build the Docker image
docker build -t my-hosted-agent:v1 .

# Login to ACR
az acr login --name aqmlacr001

# Tag and push
docker tag my-hosted-agent:v1 aqmlacr001.azurecr.io/my-hosted-agent:v1
docker push aqmlacr001.azurecr.io/my-hosted-agent:v1
```

### Step 2: Configure ACR Permissions

```bash
# Get your project's managed identity Object ID from Azure Portal
# Go to: AI Foundry Project → Identity → System assigned → Copy Object (principal) ID

# Assign ACR pull role
az role assignment create \
  --assignee <MANAGED_IDENTITY_OBJECT_ID> \
  --role "AcrPull" \
  --scope /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RG_NAME>/providers/Microsoft.ContainerRegistry/registries/aqmlacr001
```

### Step 3: Deploy

```bash
# Ensure you're authenticated
az login

# Install dependencies if needed
pip install azure-ai-projects azure-identity

# Deploy the agent
python deploy_simple.py

# Check deployment status
python check_deployment.py

# Test it (once deployed)
python test_deployed_agent.py
```

## Expected Output

When you run `deploy_simple.py`, you should see:

```
Deploying hosted agent to Azure AI Foundry
Project: https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject
Image: aqmlacr001.azurecr.io/my-hosted-agent:v1
Agent: my-hosted-agent

Successfully connected to Azure AI Foundry!

Creating hosted agent version...

✅ Agent created successfully!
   Agent ID: <agent-id>
   Agent Name: my-hosted-agent
   Version: 1

📋 Next steps:
1. The agent deployment is being created in the background
2. Check the Azure AI Foundry portal for deployment status:
   https://ai.azure.com
3. Navigate to your project → Agents → my-hosted-agent

⚠️  Note: It may take several minutes for the container to be pulled and started
```

## Configuration Values

Update these in `deploy_simple.py` to match your environment:

```python
PROJECT_ENDPOINT = "https://aq-ai-foundry-sweden-central.services.ai.azure.com/api/projects/firstProject"
CONTAINER_IMAGE = "aqmlacr001.azurecr.io/my-hosted-agent:v1"
AGENT_NAME = "my-hosted-agent"
```

Environment variables passed to the container:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
- `AZURE_OPENAI_API_VERSION`

## Troubleshooting

### Authentication Error
```bash
az login
az account set --subscription <subscription-id>
```

### Container Image Not Found
```bash
# Verify image exists
az acr repository show-tags --name aqmlacr001 --repository my-hosted-agent
```

### ACR Permission Denied
- Ensure the managed identity has `AcrPull` role
- Wait a few minutes for RBAC changes to propagate

### Deployment Stuck
- Check the Azure portal for deployment logs
- Navigate to: Project → Agents → Your Agent → "view deployment logs"

## References

- 📚 [Official Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents?view=foundry)
- 📖 [Detailed Deployment Guide](./DEPLOYMENT_GUIDE.md)
- 🐙 [Azure Samples GitHub](https://github.com/Azure-Samples)

## What's Different from Declarative Agents?

This is a **hosted agent** (code-based), not a declarative agent (YAML-based):

| Aspect | Hosted Agent (This) | Declarative Agent |
|--------|---------------------|-------------------|
| Definition | Python code | YAML configuration |
| Deployment | Docker container | Portal UI |
| Tools | Custom Python tools | Built-in tools only |
| Frameworks | LangGraph, custom | N/A |
| Flexibility | Complete control | Limited to built-ins |
| Complexity | Higher | Lower |

The main reference document uses **hosted agents**, which is what we've implemented here.
