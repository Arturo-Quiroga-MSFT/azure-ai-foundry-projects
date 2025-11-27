# 🚀 Quick Start Guide: AG-UI + CopilotKit Financial Analysis

> **Get your agentic financial analysis app running in 10 minutes!**

## Prerequisites Checklist

- [ ] Python 3.10 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] Azure subscription with Azure OpenAI access
- [ ] Azure OpenAI deployment (gpt-4o or gpt-4o-mini)
- [ ] Azure CLI installed and logged in (`az login`)

## Step 1: Configure Azure OpenAI (5 minutes)

### 1.1 Get Your Azure OpenAI Endpoint

```bash
# Login to Azure
az login

# List your Azure OpenAI resources
az cognitiveservices account list --query "[?kind=='OpenAI'].{Name:name,Endpoint:properties.endpoint,ResourceGroup:resourceGroup}" -o table

# Get your endpoint (looks like https://your-resource.openai.azure.com/)
ENDPOINT=$(az cognitiveservices account show \
  --name YOUR_OPENAI_RESOURCE_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --query properties.endpoint -o tsv)

echo "Your endpoint: $ENDPOINT"
```

### 1.2 Get Your Deployment Name

```bash
# List your deployments
az cognitiveservices account deployment list \
  --name YOUR_OPENAI_RESOURCE_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --query "[].{Name:name,Model:properties.model.name,Version:properties.model.version}" -o table

# Choose a deployment (e.g., gpt-4o)
DEPLOYMENT_NAME="gpt-4o"
```

### 1.3 Verify Access

```bash
# Ensure you have the right role assignment
az role assignment list \
  --scope /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/YOUR_OPENAI_RESOURCE_NAME \
  --query "[?principalName=='YOUR_EMAIL@domain.com'].roleDefinitionName" -o table

# You should see "Cognitive Services OpenAI User" or "Cognitive Services OpenAI Contributor"
```

## Step 2: Setup Backend (3 minutes)

### 2.1 Navigate and Create Virtual Environment

```bash
cd ag_ui_copilotkit_example/backend

# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 2.2 Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import agent_framework; print('✅ Agent Framework installed')"
python -c "import agent_framework_ag_ui; print('✅ AG-UI installed')"
python -c "import fastapi; print('✅ FastAPI installed')"
```

### 2.3 Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your values
# Option 1: Use nano/vim
nano .env

# Option 2: Use sed (replace with your values)
sed -i '' "s|AZURE_OPENAI_ENDPOINT=|AZURE_OPENAI_ENDPOINT=${ENDPOINT}|" .env
sed -i '' "s|AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o|AZURE_OPENAI_DEPLOYMENT_NAME=${DEPLOYMENT_NAME}|" .env
```

Your `.env` should look like:
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
HOST=0.0.0.0
PORT=8888
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 2.4 Test Backend

```bash
# Start the server
python server.py

# You should see:
# ✅ Financial Analysis Agent registered at /agent
# ✅ AG-UI protocol endpoint ready for connections
# INFO:     Uvicorn running on http://0.0.0.0:8888
```

Keep this terminal open. In a new terminal, test the server:

```bash
# Test health endpoint
curl http://localhost:8888/health

# Expected response:
# {"status":"healthy","service":"ag-ui-financial-analysis","version":"1.0.0","agent":"FinancialAnalyst"}

# Test AG-UI endpoint
curl -X POST http://localhost:8888/agent \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

## Step 3: Setup Frontend (2 minutes)

### 3.1 Open New Terminal and Navigate

```bash
# Open a new terminal
cd ag_ui_copilotkit_example/frontend
```

### 3.2 Install Dependencies

```bash
# Install Node packages
npm install

# Verify installation
npm list @copilotkit/react-core @copilotkit/react-ui
```

### 3.3 Configure Backend URL (optional)

```bash
# Create .env file if you need to override the default
echo "VITE_AGUI_SERVER_URL=http://localhost:8888/agent" > .env
```

### 3.4 Start Frontend

```bash
# Start development server
npm run dev

# You should see:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose
```

## Step 4: Test the Application (1 minute)

### 4.1 Open in Browser

1. Open `http://localhost:5173`
2. You should see the Financial Analysis AI interface
3. Click the chat icon in the bottom right corner

### 4.2 Try Example Queries

**Test 1: Simple Greeting**
```
You: Hello!
Agent: Hello! I'm your AI financial analyst...
```

**Test 2: Revenue Analysis**
```
You: Analyze Q4 2024 revenue trends
Agent: [Streams analysis with data and insights]
```

**Test 3: Chart Generation**
```
You: Create a line chart showing monthly revenue
Agent: [Generates and renders chart in dashboard]
```

**Test 4: Approval Workflow**
```
You: Export a financial report as PDF
Agent: [Shows approval dialog]
[You click "Approve"]
Agent: ✅ Report exported successfully!
```

## Common Issues and Solutions

### Issue 1: "Import agent_framework could not be resolved"

**Solution:**
```bash
# Make sure you're in the virtual environment
which python  # Should show path to venv/bin/python

# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Issue 2: "Authentication failed" from Azure OpenAI

**Solution:**
```bash
# Re-login to Azure
az login

# Check your identity
az account show

# Verify you have the right role
az role assignment list --assignee YOUR_EMAIL@domain.com
```

### Issue 3: "CORS error" in browser

**Solution:**
```bash
# Backend .env file, add your frontend URL
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Restart the backend server
```

### Issue 4: Backend won't start

**Solution:**
```bash
# Check if port 8888 is already in use
lsof -i :8888
# Or on Windows:
netstat -ano | findstr :8888

# Kill the process or use a different port
PORT=8889 python server.py
```

### Issue 5: Frontend won't connect to backend

**Solution:**
```bash
# Check backend is running
curl http://localhost:8888/health

# Check frontend environment
cat frontend/.env

# Verify proxy in vite.config.ts
# Should have:
# proxy: {
#   '/agent': {
#     target: 'http://localhost:8888',
#     changeOrigin: true,
#   }
# }
```

## Architecture Overview

```
┌─────────────────────────────────────┐
│  Browser (localhost:5173)           │
│  ├── React + CopilotKit            │
│  ├── Chat Interface                 │
│  └── Dashboard Components           │
└────────────┬────────────────────────┘
             │
             │ AG-UI Protocol (HTTP + SSE)
             │
┌────────────▼────────────────────────┐
│  Backend Server (localhost:8888)    │
│  ├── FastAPI + AG-UI Endpoint      │
│  ├── Microsoft Agent Framework      │
│  └── Financial Analysis Agent       │
└────────────┬────────────────────────┘
             │
             │ Azure SDK
             │
┌────────────▼────────────────────────┐
│  Azure OpenAI Service               │
│  └── GPT-4o Model                   │
└─────────────────────────────────────┘
```

## Next Steps

### 1. Customize the Agent

Edit `backend/agents/tools.py` to add your own tools:

```python
@ai_function
def my_custom_tool(param: str) -> dict:
    """Your custom business logic"""
    return {"result": "..."}
```

### 2. Add More UI Components

Edit `frontend/src/components/` to add custom visualizations:

```tsx
export function MyCustomComponent({ data }: Props) {
  return <div>...</div>;
}
```

### 3. Deploy to Azure

```bash
# Install Azure Developer CLI
brew install azure/azd/azd  # macOS
# Or download from: https://aka.ms/azd

# Initialize and deploy
azd init
azd up
```

### 4. Enable Observability

```bash
# Add Application Insights
pip install azure-monitor-opentelemetry

# Configure in server.py
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor(connection_string="YOUR_CONNECTION_STRING")
```

## Useful Commands

### Backend

```bash
# Run server
python server.py

# Run with reload (for development)
uvicorn server:app --reload --port 8888

# Check logs
tail -f logs/server.log

# Test agent directly
python -m agents.financial_analyst
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Both

```bash
# Start both servers (requires two terminals)
# Terminal 1:
cd backend && python server.py

# Terminal 2:
cd frontend && npm run dev
```

## Learning Resources

- [AG-UI Protocol](https://docs.ag-ui.com)
- [CopilotKit Documentation](https://docs.copilotkit.ai)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework)
- [Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai)

## Support

- Issues: File on GitHub
- Discord: AG-UI Community - [discord.gg/Jd3FzfdJa8](https://discord.gg/Jd3FzfdJa8)
- Discord: CopilotKit - [discord.gg/6dffbvGU3D](https://discord.gg/6dffbvGU3D)

---

**🎉 Congratulations!** You now have a working agentic financial analysis application powered by AG-UI, CopilotKit, and Azure AI Foundry!
