# AG-UI and CopilotKit Integration with Azure AI Foundry

> **Building Next-Generation Agentic Applications with Rich UI Interactions**

## 🎯 Overview

This document explores how **AG-UI** (Agent-User Interaction Protocol) and **CopilotKit** enable you to build compelling, user-friendly AI applications that leverage Azure AI Foundry, Foundry Agent Service, and Microsoft Agent Framework.

## 📋 Table of Contents

- [What is AG-UI?](#what-is-ag-ui)
- [What is CopilotKit?](#what-is-copilotkit)
- [Why Use These Tools?](#why-use-these-tools)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Implementation Examples](#implementation-examples)
- [Getting Started](#getting-started)

---

## 🔍 What is AG-UI?

**AG-UI (Agent-User Interaction Protocol)** is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications.

### Core Capabilities

1. **Streaming Chat**: Real-time token and event streaming for responsive interactions
2. **Multimodality**: Support for files, images, audio, transcripts with annotations
3. **Generative UI**: Render model output as dynamic, typed components
4. **Shared State**: Bidirectional state synchronization between agent and app
5. **Human-in-the-Loop**: Pause, approve, edit, or retry operations
6. **Backend Tool Rendering**: Execute tools on backend with streamed results
7. **Frontend Tool Calls**: Handoffs to frontend-executed actions

### The AI Protocol Landscape

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  MCP (Model Context Protocol)                       │
│  → Connects agents to tools and context             │
│                                                      │
│  A2A (Agent-to-Agent)                               │
│  → Connects agents to other agents                  │
│                                                      │
│  AG-UI (Agent-User Interaction)                     │
│  → Connects agents to users via applications        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Supported Agent Frameworks

| Framework | Status | Type |
|-----------|--------|------|
| **Microsoft Agent Framework** | ✅ Supported | 1st Party |
| LangGraph | ✅ Supported | Partnership |
| CrewAI | ✅ Supported | Partnership |
| Google ADK | ✅ Supported | 1st Party |
| Mastra | ✅ Supported | 1st Party |
| Pydantic AI | ✅ Supported | 1st Party |
| LlamaIndex | ✅ Supported | 1st Party |

---

## 🚀 What is CopilotKit?

**CopilotKit** is a React UI framework and infrastructure platform for building in-app AI copilots, chatbots, and agents with production-ready components.

### Key Features

1. **Pre-built UI Components**: Customizable chat interfaces, popups, sidebars
2. **Headless APIs**: Full control with `useCopilotChat`, `useCopilotAction`
3. **Framework Agnostic**: Works with React, Next.js, AG-UI integrations
4. **LangGraph Integration**: Co-agents with state sharing and generative UI
5. **Human-in-the-Loop**: Built-in approval workflows with `renderAndWaitForResponse`
6. **Agent State Streaming**: Intermediate state updates during execution
7. **Production Ready**: Security, prompt injection protection, scalability

### CopilotKit + AG-UI

CopilotKit provides **first-class AG-UI support**, meaning you can:
- Connect to any AG-UI-compatible agent backend
- Use rich UI components for agent interactions
- Leverage streaming, state management, and approvals out-of-the-box
- Build with React while backend uses Python, .NET, or any AG-UI server

---

## 💡 Why Use These Tools?

### Traditional Approach vs. AG-UI + CopilotKit

#### Without AG-UI/CopilotKit
```python
# Manual WebSocket handling
# Custom event parsing
# DIY state synchronization
# Build UI from scratch
# Handle streaming manually
# Implement approval flows
```

#### With AG-UI + CopilotKit
```python
# ✅ Standard protocol
# ✅ Auto event handling
# ✅ Built-in state sync
# ✅ Production UI components
# ✅ Streaming included
# ✅ Approval workflows ready
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Rapid Development** | Minutes to integrate vs. days building from scratch |
| **Standardization** | One protocol works across all agent frameworks |
| **Rich Interactions** | Pre-built components for chat, approvals, generative UI |
| **Production Ready** | Security, error handling, scalability built-in |
| **Future Proof** | Standards-based approach, wide ecosystem support |
| **Developer Experience** | Focus on agent logic, not UI plumbing |

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Web/Mobile)                   │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │         CopilotKit React Components              │     │
│  │                                                  │     │
│  │  • <CopilotPopup />                             │     │
│  │  • useCopilotChat()                             │     │
│  │  • useCopilotAction()                           │     │
│  │  • useCoAgent()                                 │     │
│  └──────────────────────────────────────────────────┘     │
│                         │                                   │
│                         │ AG-UI Protocol (SSE/WebSocket)   │
│                         ▼                                   │
└─────────────────────────────────────────────────────────────┘
                         │
                         │
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Python/FastAPI)                 │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │         AG-UI Server (FastAPI)                   │     │
│  │                                                  │     │
│  │  add_agent_framework_fastapi_endpoint(          │     │
│  │      app=app,                                   │     │
│  │      agent=my_agent,                            │     │
│  │      path="/agent"                              │     │
│  │  )                                              │     │
│  └──────────────────────────────────────────────────┘     │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────┐     │
│  │      Microsoft Agent Framework Agent             │     │
│  │                                                  │     │
│  │  • ChatAgent                                    │     │
│  │  • Tools (@ai_function)                         │     │
│  │  • State Management                             │     │
│  │  • Approval Workflows                           │     │
│  └──────────────────────────────────────────────────┘     │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────┐     │
│  │         Azure AI Services                        │     │
│  │                                                  │     │
│  │  • Azure OpenAI (GPT-4o)                        │     │
│  │  • Azure AI Foundry                             │     │
│  │  • Code Interpreter                             │     │
│  │  • Azure Identity                               │     │
│  └──────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input → CopilotKit Component → AG-UI Protocol → FastAPI Server
                                                            ↓
                                                    Agent Framework
                                                            ↓
                                                    Azure OpenAI
                                                            ↓
Agent Response ← CopilotKit Rendering ← AG-UI Events ← Stream Back
```

---

## ✨ Key Features

### 1. Streaming Chat
**Real-time responses with token streaming**

```python
# Server (Python)
@ai_function
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny, 22°C"

agent = ChatAgent(
    name="WeatherAgent",
    instructions="You are a weather assistant",
    chat_client=AzureOpenAIChatClient(credential=AzureCliCredential()),
    tools=[get_weather]
)

add_agent_framework_fastapi_endpoint(app, agent, "/weather")
```

```tsx
// Client (React + CopilotKit)
<CopilotPopup
  instructions="You are a weather assistant"
  labels={{ title: "Weather Assistant" }}
/>
```

### 2. Backend Tool Rendering
**Execute complex operations on backend, stream results to UI**

```python
@ai_function
def analyze_data(dataset: str) -> dict:
    """Analyze financial data and return insights"""
    # Complex analysis here
    return {
        "revenue_trend": "increasing",
        "growth_rate": 15.3,
        "forecast": [...]
    }

agent = ChatAgent(
    name="DataAnalyst",
    tools=[analyze_data],
    chat_client=azure_client
)
```

```tsx
// Automatically rendered in CopilotKit UI
const { visibleMessages } = useCopilotChat();
```

### 3. Human-in-the-Loop (Approval Workflows)
**Request user approval for sensitive operations**

```python
@ai_function(approval_mode="always_require")
def transfer_money(from_account: str, to_account: str, amount: float) -> str:
    """Transfer money between accounts"""
    return f"Transferred ${amount} from {from_account} to {to_account}"

wrapped_agent = AgentFrameworkAgent(
    agent=agent,
    require_confirmation=True
)
```

```tsx
// CopilotKit auto-renders approval UI
useCopilotAction({
  name: "transfer_money",
  renderAndWaitForResponse: ({ args, respond }) => (
    <ApprovalDialog
      message={`Transfer $${args.amount}?`}
      onApprove={() => respond({ approved: true })}
      onCancel={() => respond({ approved: false })}
    />
  )
});
```

### 4. Shared State Management
**Bidirectional state sync between agent and UI**

```python
# Server: Define state schema
recipe_agent = AgentFrameworkAgent(
    agent=agent,
    state_schema={
        "recipe": {"type": "object", "description": "Current recipe"}
    },
    predict_state_config={
        "recipe": {"tool": "update_recipe", "tool_argument": "recipe"}
    }
)
```

```tsx
// Client: Access synchronized state
const { agentState } = useCoAgent({
  name: "recipe_agent",
  initialState: { recipe: null }
});

// Render based on agent state
<RecipeCard recipe={agentState.recipe} />
```

### 5. Generative UI
**Dynamically render components based on agent output**

```python
@ai_function
def create_chart(data: dict) -> dict:
    """Generate visualization data"""
    return {
        "type": "line_chart",
        "data": [...],
        "config": {...}
    }
```

```tsx
// Auto-render custom components
useCopilotAction({
  name: "create_chart",
  render: ({ args }) => <ChartComponent data={args.data} />
});
```

### 6. Multi-Agent Orchestration
**Compose multiple specialized agents**

```python
# Research Agent
research_agent = ChatAgent(
    name="ResearchAgent",
    tools=[web_search, fetch_data]
)

# Coder Agent
coder_agent = ChatAgent(
    name="CoderAgent",
    tools=[execute_code, generate_code]
)

# Orchestrator
orchestrator = ChatAgent(
    name="Orchestrator",
    agents=[research_agent, coder_agent]
)
```

```tsx
// CopilotKit handles multi-agent coordination
const { agentState } = useCoAgent({ name: "orchestrator" });
```

---

## 🎨 Use Cases

### 1. **Financial Analysis Dashboard**
- **Frontend**: CopilotKit chat + visualization components
- **Backend**: AG-UI server with data analysis agents
- **Features**: Real-time insights, chart generation, trend forecasting
- **Tools**: pandas, plotly, Azure OpenAI code interpreter

### 2. **Customer Support Assistant**
- **Frontend**: CopilotKit popup embedded in product
- **Backend**: AG-UI server with ticket management tools
- **Features**: Answer questions, create tickets, escalate issues
- **Tools**: CRM integration, knowledge base search

### 3. **Content Creation Studio**
- **Frontend**: React editor with CopilotKit sidebar
- **Backend**: Multi-agent system (research, writing, editing)
- **Features**: Research topics, generate drafts, suggest improvements
- **Tools**: Web search, content generation, style checking

### 4. **Travel Booking Agent**
- **Frontend**: CopilotKit chat interface
- **Backend**: AG-UI server with booking tools
- **Features**: Search flights, compare hotels, book reservations
- **Tools**: Travel APIs, payment processing (with approval)

### 5. **Code Review Assistant**
- **Frontend**: VS Code extension with CopilotKit
- **Backend**: AG-UI server with code analysis agents
- **Features**: Review code, suggest fixes, run tests
- **Tools**: Static analysis, test execution, git integration

---

## 📝 Implementation Examples

### Example 1: Basic AG-UI Server with Azure AI Foundry

```python
# server.py
import os
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI

# Configure Azure OpenAI
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]

chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    deployment_name=deployment
)

# Create agent
agent = ChatAgent(
    name="AssistantAgent",
    instructions="You are a helpful AI assistant",
    chat_client=chat_client
)

# Create FastAPI app with AG-UI endpoint
app = FastAPI(title="My AG-UI Server")
add_agent_framework_fastapi_endpoint(app, agent, "/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
```

### Example 2: CopilotKit Client

```tsx
// App.tsx
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function App() {
  return (
    <CopilotKit runtimeUrl="http://localhost:8888/agent">
      <YourApp />
      <CopilotPopup
        instructions="You are a helpful AI assistant"
        labels={{
          title: "AI Assistant",
          initial: "How can I help you today?"
        }}
      />
    </CopilotKit>
  );
}
```

### Example 3: Agent with Tools and Approvals

```python
# advanced_server.py
from typing import Annotated
from agent_framework import ChatAgent, ai_function
from agent_framework_ag_ui import AgentFrameworkAgent
from pydantic import Field

@ai_function
def search_products(query: Annotated[str, Field(description="Search query")]) -> list:
    """Search for products"""
    # Implementation here
    return [{"name": "Product 1", "price": 29.99}]

@ai_function(approval_mode="always_require")
def place_order(
    product_id: Annotated[str, Field(description="Product ID")],
    quantity: Annotated[int, Field(description="Quantity")]
) -> str:
    """Place an order (requires approval)"""
    return f"Order placed: {quantity}x product {product_id}"

agent = ChatAgent(
    name="ShoppingAgent",
    instructions="Help users shop for products",
    chat_client=azure_client,
    tools=[search_products, place_order]
)

# Enable human-in-the-loop
wrapped_agent = AgentFrameworkAgent(
    agent=agent,
    require_confirmation=True
)

add_agent_framework_fastapi_endpoint(app, wrapped_agent, "/shopping")
```

```tsx
// ShoppingApp.tsx
import { useCopilotAction } from "@copilotkit/react-core";

function ShoppingApp() {
  useCopilotAction({
    name: "place_order",
    renderAndWaitForResponse: ({ args, respond }) => (
      <div className="approval-dialog">
        <h3>Confirm Order</h3>
        <p>Quantity: {args.quantity}</p>
        <p>Product: {args.product_id}</p>
        <button onClick={() => respond({ approved: true })}>
          Confirm
        </button>
        <button onClick={() => respond({ approved: false })}>
          Cancel
        </button>
      </div>
    )
  });

  return <CopilotPopup />;
}
```

### Example 4: State Management with Generative UI

```python
# state_server.py
@ai_function
def update_dashboard(
    metrics: Annotated[dict, Field(description="Dashboard metrics")]
) -> dict:
    """Update dashboard with new metrics"""
    return metrics

agent = ChatAgent(
    name="DashboardAgent",
    tools=[update_dashboard],
    chat_client=azure_client
)

dashboard_agent = AgentFrameworkAgent(
    agent=agent,
    state_schema={
        "dashboard": {"type": "object", "description": "Dashboard state"}
    },
    predict_state_config={
        "dashboard": {"tool": "update_dashboard", "tool_argument": "metrics"}
    }
)
```

```tsx
// Dashboard.tsx
import { useCoAgent } from "@copilotkit/react-core";

function Dashboard() {
  const { agentState } = useCoAgent({
    name: "DashboardAgent",
    initialState: { dashboard: null }
  });

  return (
    <div>
      {agentState.dashboard && (
        <MetricsDisplay metrics={agentState.dashboard} />
      )}
      <CopilotSidebar />
    </div>
  );
}
```

---

## 🚀 Getting Started

### Prerequisites

1. **Azure Account** with AI Foundry access
2. **Azure OpenAI** deployment (e.g., gpt-4o)
3. **Python 3.10+** and **Node.js 18+**
4. **Azure CLI** authenticated (`az login`)

### Step 1: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install agent-framework agent-framework-ag-ui
pip install azure-identity fastapi uvicorn
```

### Step 2: Configure Environment

```bash
# .env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-id
```

### Step 3: Create AG-UI Server

```python
# server.py (see Example 1 above)
```

### Step 4: Run Server

```bash
python server.py
# Server runs at http://localhost:8888
```

### Step 5: Create React App

```bash
# Create Next.js app
npx create-next-app@latest my-copilot-app
cd my-copilot-app

# Install CopilotKit
npm install @copilotkit/react-core @copilotkit/react-ui
```

### Step 6: Add CopilotKit

```tsx
// app/page.tsx (see Example 2 above)
```

### Step 7: Test

```bash
npm run dev
# Open http://localhost:3000
```

### Step 8: Deploy

#### Backend (Azure App Service)
```bash
# Using Azure Developer CLI
azd init
azd up
```

#### Frontend (Azure Static Web Apps)
```bash
# Connect GitHub repo
az staticwebapp create \
  --name my-copilot-app \
  --resource-group my-rg \
  --source https://github.com/you/repo
```

---

## 📚 Additional Resources

### Documentation
- [AG-UI Protocol Docs](https://docs.ag-ui.com/introduction)
- [CopilotKit Docs](https://docs.copilotkit.ai)
- [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework)
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry)

### Examples
- [AG-UI Dojo](https://dojo.ag-ui.com) - Interactive demos
- [CopilotKit Examples](https://github.com/CopilotKit/CopilotKit/tree/main/examples)
- [Agent Framework Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples)

### Community
- [AG-UI Discord](https://discord.gg/Jd3FzfdJa8)
- [CopilotKit Discord](https://discord.gg/6dffbvGU3D)
- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)

---

## 🎯 Next Steps

1. **Explore AG-UI Dojo**: See live examples at [dojo.ag-ui.com](https://dojo.ag-ui.com/microsoft-agent-framework-python)
2. **Build Your First Agent**: Follow the getting started guide above
3. **Add Custom Tools**: Integrate with your existing APIs and services
4. **Deploy to Azure**: Use Azure App Service + Static Web Apps
5. **Integrate with Foundry**: Connect to Azure AI Foundry Agent Service
6. **Enable Observability**: Add Application Insights for monitoring
7. **Implement Security**: Add authentication, rate limiting, RBAC

---

## 🌟 Conclusion

**AG-UI + CopilotKit + Azure AI Foundry** provides a powerful, standardized stack for building next-generation agentic applications:

- ✅ **Rapid Development**: Pre-built components and protocol
- ✅ **Rich Interactions**: Streaming, approvals, generative UI
- ✅ **Production Ready**: Security, scalability, observability
- ✅ **Azure Native**: Seamless integration with Azure AI services
- ✅ **Future Proof**: Standards-based, ecosystem-supported

Start building compelling AI experiences today! 🚀
