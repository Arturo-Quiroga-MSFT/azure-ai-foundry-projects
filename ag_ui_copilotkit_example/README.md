# AG-UI + CopilotKit Financial Analysis Example

> **A production-ready example of building agentic applications with AG-UI protocol, CopilotKit UI, and Azure AI Foundry**

## 🎯 What This Example Demonstrates

This project showcases how to build a **Financial Analysis AI Agent** with:

- **Backend**: AG-UI server using Microsoft Agent Framework + Azure OpenAI
- **Frontend**: React app with CopilotKit for rich agent interactions
- **Features**: Real-time streaming, tool execution, human-in-the-loop approvals, state management
- **Deployment**: Azure App Service (backend) + Azure Static Web Apps (frontend)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (React + CopilotKit)                         │
│  ─────────────────────────────────                     │
│  • Chat interface with streaming                        │
│  • Real-time chart rendering                            │
│  • Approval workflows for sensitive operations          │
│  • State-synchronized dashboard                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ AG-UI Protocol (HTTP + SSE)
                      ▼
┌─────────────────────────────────────────────────────────┐
│  Backend (Python + FastAPI + AG-UI)                    │
│  ────────────────────────────────────                   │
│  • AG-UI endpoint serving agents                        │
│  • Financial analysis tools                             │
│  • Azure OpenAI integration                             │
│  • Code interpreter for data analysis                   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ Azure SDK
                      ▼
┌─────────────────────────────────────────────────────────┐
│  Azure AI Services                                      │
│  ──────────────────                                     │
│  • Azure OpenAI (GPT-4o)                               │
│  • Azure AI Foundry                                     │
│  • Application Insights                                 │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
ag_ui_copilotkit_example/
├── backend/                    # Python AG-UI Server
│   ├── agents/                # Agent implementations
│   │   ├── __init__.py
│   │   ├── financial_analyst.py    # Main financial agent
│   │   └── tools.py           # AI functions (tools)
│   ├── server.py              # FastAPI app with AG-UI
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
│
├── frontend/                  # React + CopilotKit Client
│   ├── src/
│   │   ├── components/
│   │   │   ├── FinancialDashboard.tsx
│   │   │   ├── ChartRenderer.tsx
│   │   │   └── ApprovalDialog.tsx
│   │   ├── hooks/
│   │   │   └── useFinancialAgent.ts
│   │   ├── App.tsx           # Main app with CopilotKit
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── deployment/               # Deployment configs
│   ├── backend.dockerfile
│   ├── azure.yaml           # Azure Developer CLI
│   └── deploy.sh
│
└── README.md                # This file
```

## 🚀 Features

### 1. **Streaming Financial Analysis**
- Real-time token streaming for instant feedback
- Progressive rendering of analysis results
- Live updates during long-running computations

### 2. **Intelligent Tool Execution**
- **analyze_revenue**: Trend analysis and forecasting
- **generate_chart**: Create visualizations (line, bar, pie)
- **calculate_kpi**: Compute financial metrics
- **export_report**: Generate PDF reports (requires approval)

### 3. **Human-in-the-Loop Approvals**
- Approval required for sensitive operations
- Custom approval UI rendered in CopilotKit
- User can approve, reject, or modify parameters

### 4. **Shared State Management**
- Dashboard state synchronized between agent and UI
- Real-time updates as agent modifies data
- JSON Patch for efficient state deltas

### 5. **Generative UI**
- Dynamic chart rendering based on agent output
- Custom component rendering for structured data
- Seamless integration with React components

## 🛠️ Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Azure subscription with:
  - Azure OpenAI resource (gpt-4o deployed)
  - Azure AI Foundry project (optional)
- Azure CLI (`az login` completed)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure credentials

# Run server
python server.py
```

Server runs at `http://localhost:8888`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure backend URL (optional, defaults to localhost:8888)
echo "VITE_AGUI_SERVER_URL=http://localhost:8888/agent" > .env

# Run development server
npm run dev
```

App runs at `http://localhost:5173`

## 🧪 Testing

### Test Backend Directly

```bash
# With curl
curl -X POST http://localhost:8888/agent \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Analyze Q4 revenue"}]}'

# With Python client
cd backend
python test_client.py
```

### Test Frontend

1. Open `http://localhost:5173`
2. Click the chat icon
3. Try queries like:
   - "Analyze revenue trends for Q4"
   - "Create a line chart showing monthly growth"
   - "Generate a financial report" (will trigger approval)

## 📊 Example Interactions

### Example 1: Revenue Analysis

```
User: Analyze our Q4 2024 revenue performance

Agent: I'll analyze your Q4 revenue data...
[Streams live as analysis runs]

Results:
• Total Revenue: $2.45M (+18% YoY)
• Average Monthly Growth: 12.3%
• Strongest Month: December ($950K)
• Trend: Strong upward trajectory
• Forecast Q1 2025: $2.8M
```

### Example 2: Chart Generation

```
User: Create a line chart showing monthly revenue

Agent: [Generates chart data]
[CopilotKit renders interactive chart component]

[Beautiful line chart appears with:
 - X-axis: Months (Oct, Nov, Dec)
 - Y-axis: Revenue ($K)
 - Trend line showing growth]
```

### Example 3: Report Export (Approval Required)

```
User: Export this analysis as a PDF report

Agent: [Requests approval]

[Approval Dialog Appears:]
┌─────────────────────────────────────┐
│  Confirm Report Export              │
│                                     │
│  Export financial analysis as PDF?  │
│  File: Q4_2024_Report.pdf          │
│                                     │
│  [Approve]  [Cancel]               │
└─────────────────────────────────────┘

User: [Clicks Approve]

Agent: ✅ Report exported successfully!
Download: Q4_2024_Report.pdf
```

## 🔧 Configuration

### Backend Configuration (.env)

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# Azure AI Foundry (optional)
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-id

# Server Settings
HOST=0.0.0.0
PORT=8888
LOG_LEVEL=INFO

# CORS (for development)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration (.env)

```bash
# AG-UI Server URL
VITE_AGUI_SERVER_URL=http://localhost:8888/agent

# Optional: Enable debug mode
VITE_DEBUG=true
```

## 🚢 Deployment

### Option 1: Azure Developer CLI (Recommended)

```bash
# Initialize
azd init

# Deploy both backend and frontend
azd up

# Get endpoints
azd show
```

### Option 2: Manual Deployment

#### Backend to Azure App Service

```bash
cd backend

# Login to Azure
az login

# Create resource group
az group create --name rg-agui-example --location eastus2

# Create App Service plan
az appservice plan create \
  --name plan-agui-backend \
  --resource-group rg-agui-example \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --name app-agui-backend \
  --resource-group rg-agui-example \
  --plan plan-agui-backend \
  --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set \
  --name app-agui-backend \
  --resource-group rg-agui-example \
  --settings \
    AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
    AZURE_OPENAI_DEPLOYMENT_NAME="$AZURE_OPENAI_DEPLOYMENT_NAME"

# Deploy code
az webapp up \
  --name app-agui-backend \
  --resource-group rg-agui-example
```

#### Frontend to Azure Static Web Apps

```bash
cd frontend

# Build
npm run build

# Create Static Web App
az staticwebapp create \
  --name swa-agui-frontend \
  --resource-group rg-agui-example \
  --source . \
  --location eastus2 \
  --branch main \
  --app-location "frontend" \
  --output-location "dist"
```

## 📚 Learn More

### AG-UI Resources
- [AG-UI Protocol Documentation](https://docs.ag-ui.com/introduction)
- [AG-UI Dojo (Live Examples)](https://dojo.ag-ui.com/microsoft-agent-framework-python)
- [AG-UI GitHub](https://github.com/ag-ui-protocol/ag-ui)

### CopilotKit Resources
- [CopilotKit Documentation](https://docs.copilotkit.ai)
- [CopilotKit Examples](https://github.com/CopilotKit/CopilotKit/tree/main/examples)
- [CopilotKit Discord](https://discord.gg/6dffbvGU3D)

### Microsoft Agent Framework
- [Agent Framework Documentation](https://learn.microsoft.com/agent-framework)
- [AG-UI Integration Guide](https://learn.microsoft.com/agent-framework/integrations/ag-ui)
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry)

## 🐛 Troubleshooting

### Backend Issues

**Server won't start**
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check environment variables
python -c "import os; print(os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

**Authentication errors**
```bash
# Re-login to Azure
az login

# Check credentials
az account show
```

### Frontend Issues

**Can't connect to backend**
- Check `VITE_AGUI_SERVER_URL` in `.env`
- Verify backend is running: `curl http://localhost:8888/health`
- Check browser console for CORS errors

**CopilotKit not loading**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Contributing

Contributions welcome! This example demonstrates best practices for:
- AG-UI protocol implementation
- CopilotKit integration
- Azure AI Foundry usage
- Production deployment patterns

## 📄 License

MIT License - see LICENSE file for details

## 🌟 Next Steps

1. **Customize Agents**: Modify `agents/financial_analyst.py` for your use case
2. **Add Tools**: Create new `@ai_function` decorated functions in `agents/tools.py`
3. **Enhance UI**: Add custom components in `frontend/src/components/`
4. **Deploy**: Use `azd up` for production deployment
5. **Monitor**: Enable Application Insights for observability
6. **Scale**: Configure autoscaling in Azure App Service

Happy building! 🚀
