# Azure Container Apps Deployment Guide

## Overview
This guide walks through deploying the AG-UI Demo application (FastAPI backend + Next.js frontend) to Azure Container Apps using Azure Developer CLI (azd).

## Prerequisites

### 1. Required Tools
```bash
# Check if tools are installed
az --version          # Azure CLI
azd version          # Azure Developer CLI  
docker --version     # Docker
```

### 2. Install Missing Tools

**Azure CLI:**
```bash
# macOS
brew install azure-cli

# Or visit: https://docs.microsoft.com/cli/azure/install-azure-cli
```

**Azure Developer CLI:**
```bash
# macOS
brew install azd

# Or visit: https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd
```

**Docker:**
```bash
# macOS
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

### 3. Azure Login
```bash
# Login to Azure
az login
azd auth login

# Set your subscription
az account set --subscription <your-subscription-id>
```

## Deployment Steps

### Step 1: Initialize azd

```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo

# Initialize azd (if not already done)
azd init

# Follow prompts:
# - Environment name: (e.g., "agui-demo")
# - Subscription: Select your Azure subscription
# - Location: Select location (e.g., "swedencentral")
```

### Step 2: Configure Environment Variables

```bash
# Set Azure OpenAI configuration
azd env set AZURE_OPENAI_ENDPOINT "https://aq-ai-foundry-sweden-central.openai.azure.com/"
azd env set AZURE_OPENAI_DEPLOYMENT_NAME "gpt-4.1-mini"

# Set API keys (replace with your actual keys)
azd env set OPENWEATHER_API_KEY "your-openweathermap-api-key"
azd env set TAVILY_API_KEY "your-tavily-api-key"
```

### Step 3: Preview Deployment

```bash
# Preview what will be created
azd provision --preview
```

Review the output to see:
- Resource Group
- Container Apps Environment
- Container Registry
- Key Vault
- Log Analytics Workspace
- Application Insights
- Backend Container App (FastAPI)
- Frontend Container App (Next.js)
- Managed Identities and Role Assignments

### Step 4: Deploy to Azure

```bash
# Deploy infrastructure and applications
azd up
```

This command will:
1. Build Docker images for backend and frontend
2. Push images to Azure Container Registry
3. Provision all Azure resources via Bicep
4. Deploy container apps
5. Configure secrets in Key Vault
6. Set up monitoring

**Expected Duration:** 5-10 minutes

### Step 5: Verify Deployment

```bash
# Show deployment info
azd show

# Get frontend URL
azd env get-values | grep FRONTEND_URL
```

Visit the frontend URL in your browser to test the application.

### Step 6: Check Logs

```bash
# View backend logs
az containerapp logs show \
  --name azca-backend-<resource-token> \
  --resource-group rg-<env-name> \
  --follow

# View frontend logs
az containerapp logs show \
  --name azca-frontend-<resource-token> \
  --resource-group rg-<env-name> \
  --follow
```

## Testing the Deployment

### 1. Access the Application
Navigate to the FRONTEND_URL from the deployment output.

### 2. Test Sample Queries
Try these sample queries in the chat interface:
- "What's the weather in Paris?"
- "Plot a sine wave from 0 to 2π"
- "Research weather in Paris and London, then create a comparison chart"

### 3. Monitor in Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your resource group
3. Open Application Insights to view:
   - Request metrics
   - Performance data
   - Exceptions and errors
4. Check Container Apps for:
   - Replica count
   - CPU/Memory usage
   - Log streams

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Azure Container Apps Environment                            │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │ Frontend         │  HTTP   │ Backend          │        │
│  │ (Next.js)        │────────▶│ (FastAPI +       │        │
│  │ Port: 3000       │         │  Agent Framework)│        │
│  │ External Access  │         │ Port: 8888       │        │
│  └──────────────────┘         │ Internal Only    │        │
│                                └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                 │                        │
                 │                        │
          ┌──────▼────────┐      ┌───────▼────────┐
          │ Container     │      │ Key Vault      │
          │ Registry      │      │ (Secrets)      │
          └───────────────┘      └────────────────┘
                                          │
                 ┌────────────────────────┴─────────────┐
                 │                                      │
          ┌──────▼────────┐                   ┌────────▼──────┐
          │ Azure OpenAI  │                   │ External APIs │
          │ GPT-4.1-mini  │                   │ (Weather,     │
          └───────────────┘                   │  Tavily)      │
                                              └───────────────┘
```

## Troubleshooting

### Container App Won't Start
```bash
# Check container logs
az containerapp logs show --name <app-name> --resource-group <rg-name> --follow

# Common issues:
# 1. Port mismatch: Ensure targetPort (8888/3000) matches app listening port
# 2. Missing secrets: Verify Key Vault secrets are accessible
# 3. Image pull errors: Check ACR role assignments
```

### Backend Can't Connect to Azure OpenAI
```bash
# Verify environment variables
az containerapp show --name azca-backend-<token> --resource-group <rg-name> \
  --query properties.template.containers[0].env

# Test managed identity permissions
az role assignment list --assignee <managed-identity-principal-id>
```

### Frontend Can't Reach Backend
- Check BACKEND_URL environment variable in frontend
- Verify backend CORS policy allows frontend origin
- Ensure backend ingress is configured correctly

## Updating the Application

```bash
# Make code changes, then redeploy
azd deploy

# Or to rebuild infrastructure and redeploy:
azd up
```

## Cleaning Up

```bash
# Delete all Azure resources
azd down

# Optionally remove local azd environment
azd env list
azd env remove <env-name>
```

## Cost Estimation

With Consumption SKU and auto-scaling 0-10 replicas:
- **Minimal usage** (testing): $5-15/month
- **Moderate usage** (demos): $20-50/month
- **Active usage**: Scales with traffic

Container Apps charges:
- Active time: ~$0.000024/vCPU-second, ~$0.000003/GiB-second
- Idle time: Minimal charges when scaled to zero

## Next Steps

1. **Configure Custom Domain**: Add your domain to the frontend container app
2. **Enable Authentication**: Add Azure AD authentication
3. **Scale Configuration**: Adjust min/max replicas based on usage
4. **Monitoring Alerts**: Set up alerts in Application Insights
5. **CI/CD Pipeline**: Integrate with GitHub Actions using azd
6. **Cost Optimization**: Review usage and adjust SKUs

## Support

- **Azure Developer CLI**: https://learn.microsoft.com/azure/developer/azure-developer-cli
- **Container Apps**: https://learn.microsoft.com/azure/container-apps
- **Agent Framework**: https://github.com/microsoft/agent-framework
