# FOUNDRY-Nov-2025 Project Documentation

**Last Updated:** November 26, 2025  
**Status:** Active Development

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Hosted Agent Investigation](#hosted-agent-investigation)
4. [AI Data Analyst Copilot](#ai-data-analyst-copilot)
5. [Key Findings & Decisions](#key-findings--decisions)
6. [Setup Instructions](#setup-instructions)
7. [Next Steps](#next-steps)
8. [Resources](#resources)

---

## 🎯 Project Overview

This repository contains two main projects exploring Azure AI Foundry capabilities:

### 1. **Hosted Agent Deployment** (`hosted_agent_example/`)
Investigation into deploying containerized agents to Azure AI Foundry using LangGraph framework.

**Objective:** Deploy a hosted (containerized) agent to Azure AI Foundry with custom tools.

**Status:** ⚠️ **Blocked** - Python SDK support not yet available

**Key Discovery:** The documented Python SDK approach using `ImageBasedHostedAgentDefinition` does not exist in any current version of `azure-ai-projects` (tested up to 1.1.0b4).

### 2. **AI Data Analyst Copilot** (`data_analyst_copilot/`)
Multi-agent system using Magentic-One orchestration for comprehensive data analysis.

**Objective:** Build an AI-powered financial analysis system with revenue forecasting capabilities.

**Status:** ✅ **Ready for Development** - Complete implementation with sample data

---

## 📁 Repository Structure

```
FOUNDRY-Nov-2025/
├── README.md                               # This documentation
├── AZURE_AI_FOUNDRY_PERMISSIONS_FIX.md    # Azure permissions troubleshooting
├── DECLARATIVE_VS_HOSTED_AGENTS.md        # Agent types comparison
│
├── hosted_agent_example/                   # Hosted Agent Project
│   ├── README.md
│   ├── agent_implementation.py             # LangGraph agent with tools
│   ├── agent.yaml                          # Agent configuration for azd
│   ├── azure.yaml                          # Azure project config
│   ├── Dockerfile                          # Container definition
│   ├── requirements.txt                    # Python dependencies
│   ├── deploy_simple.py                    # Deployment script (azd instructions)
│   ├── check_deployment.py                 # Agent status checker
│   ├── test_agent.py                       # Local testing
│   ├── test_deployed_agent.py             # Test deployed agent
│   ├── DEPLOYMENT_GUIDE.md                 # Comprehensive deployment docs
│   ├── QUICK_START.md                      # Quick start guide
│   ├── SDK_STATUS.md                       # SDK limitations documentation
│   ├── IMPLEMENTATION_SUMMARY.md           # Implementation details
│   ├── GITHUB_ISSUE.md                     # Issue template for SDK team
│   └── next-steps.md                       # Original next steps
│
└── data_analyst_copilot/                   # AI Data Analyst Project
    ├── README.md                           # Comprehensive project docs
    ├── requirements.txt                    # Dependencies
    ├── config.py                           # Configuration management
    ├── .env.example                        # Environment template
    ├── copilot.py                          # Main DataAnalystCopilot class
    ├── main.py                             # CLI entry point
    ├── .gitignore                          # Git ignore rules
    │
    ├── agents/                             # Specialized Agents
    │   ├── __init__.py
    │   ├── research_agent.py               # 🔍 Data discovery & loading
    │   ├── coder_agent.py                  # 💻 Code generation & execution
    │   ├── visualization_agent.py          # 📊 Chart creation
    │   ├── insights_agent.py               # 🧠 Result interpretation
    │   └── report_agent.py                 # 📝 Report synthesis
    │
    ├── examples/                           # Usage Examples
    │   ├── basic_analysis.py               # Simple analysis workflow
    │   ├── with_plan_review.py            # Human-in-the-loop example
    │   ├── streaming_demo.py               # Real-time streaming demo
    │   ├── financial_analysis.py           # 💰 Comprehensive financial analysis
    │   ├── quick_financial_kpi.py         # 📊 Quick KPI dashboard
    │   │
    │   └── sample_data/                    # Sample Datasets
    │       ├── README.md                   # Data documentation
    │       ├── revenue_data.csv            # 11 months of revenue data
    │       └── quarterly_metrics.csv       # 8 quarters of business metrics
    │
    └── outputs/                            # Generated Reports & Charts
        └── .gitkeep
```

---

## 🔍 Hosted Agent Investigation

### Background

Azure AI Foundry supports two types of agents:

1. **Declarative Agents** (Prompt-based)
   - Created via portal UI or Python SDK
   - No custom code/containers
   - Configurable with built-in tools

2. **Hosted Agents** (Containerized)
   - Custom code execution (LangGraph, etc.)
   - Docker container deployment
   - Full control over logic and tools
   - **Portal creation: NOT supported**
   - **Python SDK: NOT yet available**

### Investigation Timeline

#### Initial Approach
Attempted to deploy hosted agent using Python SDK based on Microsoft documentation examples.

#### Discovery
```python
from azure.ai.projects.models import ImageBasedHostedAgentDefinition
# ImportError: cannot import name 'ImageBasedHostedAgentDefinition'
```

**Finding:** The documented class does not exist in any released SDK version.

#### Versions Tested
- `azure-ai-projects==1.0.0b12` ❌
- `azure-ai-projects==1.1.0b4` ❌ (latest beta)

#### CHANGELOG Investigation
Reviewed the complete changelog for azure-ai-projects package:
- No mention of `ImageBasedHostedAgentDefinition`
- No mention of hosted agent support
- No container/Docker-related features

**Source:** https://github.com/Azure/azure-sdk-for-python/blob/release/azure-ai-projects/1.1.0b4/sdk/ai/azure-ai-projects/CHANGELOG.md

### Current Status

**✅ Working Method:** Azure Developer CLI (azd)
```bash
azd ai agent init --project-id <PROJECT_RESOURCE_ID>
azd ai agent init -m agent.yaml
azd up
```

**❌ Not Available:**
- Python SDK (`ImageBasedHostedAgentDefinition`)
- Azure Portal UI (no hosted agent creation option)
- Azure CLI (`az cognitiveservices agent`)

### GitHub Issue Filed

**Issue #44194** opened on Azure/azure-sdk-for-python repository

**Title:** [Feature Request] ImageBasedHostedAgentDefinition support for deploying hosted agents in azure-ai-projects

**Status:** Acknowledged by Microsoft team
- SDK support is being developed internally
- No specific timeline provided
- Documentation will be updated when feature is available
- Continue using `azd` for now

**Link:** https://github.com/Azure/azure-sdk-for-python/issues/44194

### Implementation Details

#### Agent Implementation
- **Framework:** LangGraph
- **Tools:** Weather API, Calculator
- **Model:** gpt-4o-mini (Azure OpenAI)
- **Container:** Python 3.11 slim base

#### Files Created
1. `agent_implementation.py` - LangGraph agent with custom tools
2. `Dockerfile` - Container definition
3. `agent.yaml` - Agent configuration for azd
4. `requirements.txt` - Dependencies
5. Multiple documentation files

#### Documentation Created
- `DEPLOYMENT_GUIDE.md` - Step-by-step azd deployment
- `SDK_STATUS.md` - SDK limitations and workarounds
- `QUICK_START.md` - Quick reference
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `GITHUB_ISSUE.md` - Issue template for SDK team

### Lessons Learned

1. **Documentation ≠ Implementation**
   - Microsoft docs show code that doesn't exist yet
   - Always verify SDK capabilities before committing to approach

2. **Portal UI Limitations**
   - Portal only supports declarative agents
   - Hosted agents must be deployed via azd
   - Portal can only VIEW/TEST after azd deployment

3. **SDK Development Lag**
   - Preview features may not have SDK support immediately
   - CLI tools (azd) often available before SDK
   - Check changelogs before assuming feature availability

4. **Alternative Approaches**
   - When SDK blocked, investigate CLI alternatives
   - azd provides full hosted agent capabilities
   - Can wrap azd commands in Python for automation

---

## 🤖 AI Data Analyst Copilot

### Overview

Multi-agent system using **Magentic-One orchestration** for comprehensive data analysis with focus on financial analysis and revenue forecasting.

### Architecture

```
User Query → Magentic Manager → [Dynamic Agent Selection]
                                 ↓
                    ┌────────────┴────────────┐
                    │                         │
            Research Agent              Coder Agent
            (Data Loading)         (Code Execution)
                    │                         │
            Visualization Agent      Insights Agent
            (Charts & Graphs)      (Interpretation)
                    │                         │
                    └────────────┬────────────┘
                                 ↓
                          Report Agent
                        (Final Synthesis)
                                 ↓
                      Comprehensive Report
```

### Specialized Agents

#### 1. 🔍 Research Agent
- **Model:** gpt-4o-search-preview (with search capabilities)
- **Purpose:** Find and load datasets
- **Capabilities:**
  - Search for relevant data
  - Load CSV, JSON, Excel, Parquet files
  - Provide data overview and statistics
  - Identify data quality issues
  
#### 2. 💻 Coder Agent
- **Model:** gpt-4o
- **Tools:** Hosted Code Interpreter
- **Purpose:** Write and execute analysis code
- **Capabilities:**
  - Data preprocessing and cleaning
  - Statistical calculations
  - Feature engineering
  - Execute Python code in sandbox
  - Handle errors and debugging

#### 3. 📊 Visualization Agent
- **Model:** gpt-4o
- **Tools:** Hosted Code Interpreter
- **Purpose:** Create charts and visualizations
- **Capabilities:**
  - Matplotlib/Seaborn charts
  - Plotly interactive visualizations
  - Publication-quality figures
  - Multiple chart types (line, bar, scatter, heatmap, etc.)

#### 4. 🧠 Insights Agent
- **Model:** gpt-4o
- **Purpose:** Interpret results and provide recommendations
- **Capabilities:**
  - Pattern identification
  - Trend analysis
  - Business context interpretation
  - Actionable recommendations
  - Risk assessment

#### 5. 📝 Report Agent
- **Model:** gpt-4o
- **Purpose:** Synthesize final comprehensive report
- **Capabilities:**
  - Executive summary generation
  - Structured report creation
  - Markdown formatting
  - Professional documentation

### Key Features

#### Magentic-One Orchestration
- **Dynamic Coordination:** Manager selects agents based on task needs
- **Iterative Refinement:** Multiple rounds of agent collaboration
- **Progress Tracking:** Detects stalls and adapts workflow
- **Flexible Collaboration:** Agents called in any order as needed

#### Human-in-the-Loop
- Optional plan review before execution
- Approve, reject, or modify analysis plans
- Interactive decision points
- Greater control over analysis approach

#### Real-time Streaming
- Watch agent collaboration live
- See code execution as it happens
- Monitor progress through workflow
- Event callbacks for custom handling

#### Configuration Options
| Setting | Default | Description |
|---------|---------|-------------|
| `max_round_count` | 15 | Maximum collaboration rounds |
| `max_stall_count` | 3 | Rounds without progress before reset |
| `max_reset_count` | 2 | Maximum plan resets allowed |
| `enable_plan_review` | False | Enable human plan approval |
| `streaming_mode` | True | Stream agent outputs in real-time |
| `output_directory` | `./outputs` | Directory for generated files |

### Financial Analysis Use Case

#### Sample Data Provided

**1. revenue_data.csv** (55 records)
- **Time Period:** January - November 2024 (11 months)
- **Categories:** Electronics, Clothing, Home & Garden
- **Regions:** North America, Europe
- **Metrics:**
  - Revenue (monthly trends showing growth)
  - Units Sold
  - Cost of Goods (40% of revenue)
  - Marketing Spend
  - Customer Acquisition

**Key Patterns in Data:**
- Revenue grows ~94% from January to November
- Electronics is highest revenue category
- Seasonality evident (growth throughout year)
- North America slightly ahead of Europe

**2. quarterly_metrics.csv** (8 records)
- **Time Period:** Q1 2023 - Q4 2024 (2 years)
- **Metrics:**
  - Total Revenue (steady growth)
  - Operating Costs
  - Net Profit (30% margin maintained)
  - Profit Margin
  - Market Share (growing from 12.3% to 16.5%)
  - Customer Lifetime Value (increasing)
  - Churn Rate (decreasing from 8.5% to 6.1%)

#### Analysis Capabilities

**Trend Analysis:**
- Month-over-month (MoM) growth rates
- Year-over-year (YoY) comparisons
- Seasonality detection
- Moving averages
- Trend extrapolation

**Profitability Analysis:**
- Gross profit margins by category
- Marketing ROI calculations
- Customer Acquisition Cost (CAC) trends
- Customer Lifetime Value (CLV) analysis
- Product-region profitability matrix

**Forecasting:**
- Time series models (ARIMA, exponential smoothing)
- 6-month revenue projections
- Confidence intervals (95%)
- Scenario analysis
- Risk assessment

**Visualizations Generated:**
1. Revenue trend with moving average
2. Revenue by category (stacked area)
3. Regional comparison (grouped bars)
4. Profit margin trends
5. Revenue forecast with confidence bands
6. Marketing ROI by category
7. Customer acquisition cost trends
8. Correlation heatmap of metrics

**Strategic Outputs:**
- Growth opportunity identification
- Risk factor assessment
- Budget allocation recommendations
- Pricing strategy suggestions
- Market expansion priorities
- Expected ROI calculations

#### Usage Examples

**1. Comprehensive Financial Analysis**
```bash
python examples/financial_analysis.py
```

Features:
- Full historical trend analysis
- Complete profitability breakdown
- 6-month revenue forecast
- 8+ professional visualizations
- Strategic recommendations
- Executive summary
- Human plan review enabled
- Runtime: ~5-10 minutes

**2. Quick KPI Dashboard**
```bash
python examples/quick_financial_kpi.py
```

Features:
- Essential KPIs only
- Fast execution (no plan review)
- Dashboard-style output
- Quick win identification
- Runtime: ~2-3 minutes

**3. Custom Analysis**
```bash
python main.py "Analyze revenue trends and forecast Q1 2025"
```

Interactive mode with custom queries.

### Technology Stack

**Agent Framework:**
- Microsoft Agent Framework (Magentic-One)
- Alternative: AutoGen with Magentic-One support

**AI Models:**
- Orchestrator: gpt-4o
- Research: gpt-4o-search-preview
- Coder: gpt-4o
- Insights: gpt-4o

**Data Analysis:**
- pandas: Data manipulation
- numpy: Numerical operations
- scipy: Statistical tests
- matplotlib/seaborn: Visualizations
- plotly: Interactive charts

**Azure Integration:**
- azure-ai-projects (client)
- azure-identity (authentication)
- azure-core

**Configuration:**
- pydantic: Settings management
- python-dotenv: Environment variables

### Setup Requirements

1. **Azure AI Foundry Project**
   - Project endpoint URL
   - Deployed models (gpt-4o, gpt-4o-search-preview)
   - Code interpreter tool configured

2. **Azure Credentials**
   - Subscription ID
   - Resource Group
   - Authentication configured

3. **Python Environment**
   - Python 3.10+
   - Virtual environment recommended
   - Dependencies from requirements.txt

4. **Environment Variables**
   ```bash
   AZURE_AI_PROJECT_ENDPOINT=https://...
   AZURE_SUBSCRIPTION_ID=...
   AZURE_RESOURCE_GROUP=...
   ```

---

## 🔑 Key Findings & Decisions

### Finding 1: Hosted Agent SDK Gap
**Issue:** Documentation shows SDK code that doesn't exist.

**Impact:** Cannot deploy hosted agents programmatically via Python SDK.

**Decision:** Use Azure Developer CLI (azd) as workaround until SDK support is added.

**Tracked:** GitHub issue #44194 filed with Microsoft team.

### Finding 2: Portal Limitations
**Issue:** Azure AI Foundry portal cannot create hosted agents.

**Impact:** All hosted agent deployment must go through azd CLI.

**Decision:** Updated documentation to clarify portal can only VIEW/TEST hosted agents after azd deployment.

### Finding 3: Magentic-One Power
**Opportunity:** Magentic-One orchestration provides superior multi-agent coordination.

**Benefits:**
- Dynamic agent selection
- Iterative refinement
- Progress tracking
- Flexible collaboration

**Decision:** Build AI Data Analyst Copilot using Magentic-One for financial analysis use case.

### Finding 4: Financial Analysis Demand
**Insight:** Revenue forecasting and trend analysis are high-value use cases.

**Benefits:**
- Automatable monthly reporting
- Data-driven decision making
- Strategic planning support
- ROI analysis

**Decision:** Create comprehensive financial analysis example with real sample data.

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Azure subscription
- Azure AI Foundry project created
- Git

### Hosted Agent Example Setup

1. **Clone repository**
   ```bash
   cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/hosted_agent_example
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Review documentation**
   ```bash
   cat SDK_STATUS.md
   cat DEPLOYMENT_GUIDE.md
   ```

4. **Deploy using azd** (when ready)
   ```bash
   # Follow DEPLOYMENT_GUIDE.md
   azd ai agent init --project-id <PROJECT_RESOURCE_ID>
   azd ai agent init -m agent.yaml
   azd up
   ```

### Data Analyst Copilot Setup

1. **Navigate to project**
   ```bash
   cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/data_analyst_copilot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

5. **Verify sample data**
   ```bash
   ls examples/sample_data/
   # Should see: revenue_data.csv, quarterly_metrics.csv
   ```

6. **Run financial analysis example**
   ```bash
   python examples/financial_analysis.py
   ```

---

## 📝 Next Steps

### Immediate (Week 1)

1. **Configure Azure AI Foundry**
   - [ ] Verify project endpoint
   - [ ] Deploy required models (gpt-4o, gpt-4o-search-preview)
   - [ ] Configure code interpreter tool
   - [ ] Test authentication

2. **Test Data Analyst Copilot**
   - [ ] Run quick KPI dashboard example
   - [ ] Run comprehensive financial analysis
   - [ ] Review generated reports and charts
   - [ ] Verify all agents working correctly

3. **Customize for Your Data**
   - [ ] Prepare your financial data in CSV format
   - [ ] Update column references in queries
   - [ ] Adjust analysis parameters
   - [ ] Test with real data

### Short-term (Month 1)

1. **Production Deployment**
   - [ ] Set up production Azure environment
   - [ ] Configure CI/CD pipeline
   - [ ] Implement error handling and logging
   - [ ] Set up monitoring and alerts

2. **Feature Enhancements**
   - [ ] Add more specialized agents (ML, forecasting)
   - [ ] Integrate with data sources (APIs, databases)
   - [ ] Create dashboard for regular reporting
   - [ ] Build web interface (optional)

3. **Hosted Agent Deployment**
   - [ ] Monitor GitHub issue #44194 for SDK updates
   - [ ] When SDK available, migrate from azd to Python SDK
   - [ ] Test hosted agent deployment workflow
   - [ ] Deploy production hosted agent

### Long-term (Quarter 1)

1. **Scale and Optimize**
   - [ ] Optimize agent performance
   - [ ] Reduce token usage
   - [ ] Implement caching strategies
   - [ ] Scale to handle more concurrent requests

2. **Advanced Analytics**
   - [ ] Add ML model training capabilities
   - [ ] Implement anomaly detection
   - [ ] Build predictive models
   - [ ] Create what-if scenario analysis

3. **Enterprise Features**
   - [ ] Multi-tenant support
   - [ ] Role-based access control
   - [ ] Audit logging
   - [ ] Compliance reporting

---

## 📚 Resources

### Official Documentation

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Hosted Agents Concepts](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Magentic-One Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/magentic)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/)

### GitHub Repositories

- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)
- [Issue #44194 - Hosted Agent SDK Support](https://github.com/Azure/azure-sdk-for-python/issues/44194)

### Package Documentation

- [azure-ai-projects PyPI](https://pypi.org/project/azure-ai-projects/)
- [azure-ai-projects CHANGELOG](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/CHANGELOG.md)

### Related Technologies

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [AutoGen](https://github.com/microsoft/autogen)
- [Magentic-One (AutoGen)](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html)

---

## 📞 Support & Contact

### Issues & Questions

- **Hosted Agent SDK:** Monitor GitHub issue #44194
- **Data Analyst Copilot:** Create issues in this repository
- **Azure AI Foundry:** Azure Support Portal

### Maintainers

- Microsoft Agent Framework Team: @dargilco, @trangevi, @glharper, @nick863, @howieleung

---

## 📄 License

See individual project directories for license information.

---

## 🔄 Document History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-26 | 1.0 | Initial documentation covering hosted agent investigation and AI Data Analyst Copilot |

---

**End of Documentation**
