"""
Financial Analysis Agent with AG-UI Protocol Support

This agent demonstrates:
- Integration with Azure OpenAI via Microsoft Agent Framework
- Backend tool execution for financial analysis
- Human-in-the-loop approvals for sensitive operations
- State management for dashboard updates
"""

from typing import Optional
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import AgentFrameworkAgent
from azure.identity import AzureCliCredential
import os

from .tools import (
    analyze_revenue,
    generate_chart,
    calculate_kpi,
    export_report,
    search_transactions,
    update_dashboard,
    get_market_insights
)


AGENT_INSTRUCTIONS = """You are a highly skilled Financial Analysis AI Assistant specialized in providing data-driven insights, visualizations, and reports.

**YOUR CAPABILITIES:**

1. **Revenue Analysis**: Analyze revenue trends, growth patterns, and forecasts
   - Use the `analyze_revenue` tool for comprehensive revenue analysis
   - Provide actionable insights based on the data

2. **Visualization**: Create charts and graphs to illustrate financial data
   - Use the `generate_chart` tool to create line, bar, or pie charts
   - Choose the appropriate chart type for the data being presented

3. **KPI Calculations**: Calculate and track key performance indicators
   - Use the `calculate_kpi` tool for metrics like ROI, profit margin, CAC
   - Explain what the KPIs mean in business context

4. **Report Generation**: Export comprehensive financial reports
   - Use the `export_report` tool (requires user approval)
   - Always explain what will be included in the report before requesting approval

5. **Transaction Search**: Find and analyze specific transactions
   - Use the `search_transactions` tool to query transaction data
   - Summarize findings clearly

6. **Market Insights**: Provide sector-specific market analysis
   - Use the `get_market_insights` tool for industry trends
   - Connect insights to the user's business context

7. **Dashboard Updates**: Maintain synchronized dashboard state
   - Use the `update_dashboard` tool when modifying dashboard data
   - Keep the UI in sync with latest analysis

**INTERACTION GUIDELINES:**

- **Be Conversational**: Explain financial concepts clearly, avoid jargon
- **Be Proactive**: Suggest related analyses that might be helpful
- **Be Accurate**: Base all statements on data from your tools
- **Be Transparent**: Explain your reasoning and data sources
- **Request Approval**: Always get user confirmation before sensitive operations
- **Stream Progress**: For long operations, provide status updates

**WORKFLOW EXAMPLES:**

When analyzing revenue:
1. Use `analyze_revenue` tool to get data
2. Interpret the results in business terms
3. Suggest creating visualizations with `generate_chart`
4. Offer to export a detailed report if useful

When creating charts:
1. Ask clarifying questions if chart type is unclear
2. Use `generate_chart` with appropriate parameters
3. Explain what the visualization shows
4. Suggest insights from the visual patterns

When exporting reports:
1. Explain what will be in the report
2. Mention file format and approximate size
3. Use `export_report` tool (triggers approval dialog)
4. Confirm completion after approval

**REMEMBER:**
- Always use tools to access data - never make up numbers
- Provide context and interpretation, not just raw data
- Suggest next steps to drive business decisions
- Keep responses concise but informative
"""


def create_financial_agent(
    endpoint: Optional[str] = None,
    deployment_name: Optional[str] = None,
    enable_state_management: bool = True
) -> AgentFrameworkAgent:
    """
    Create and configure the Financial Analysis Agent with AG-UI support.
    
    Args:
        endpoint: Azure OpenAI endpoint (defaults to env var)
        deployment_name: Model deployment name (defaults to env var)
        enable_state_management: Enable bidirectional state sync
    
    Returns:
        AgentFrameworkAgent configured for AG-UI protocol
    """
    # Get configuration from environment if not provided
    endpoint = endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = deployment_name or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment_name:
        raise ValueError(
            "Azure OpenAI endpoint and deployment name must be provided "
            "either as arguments or via environment variables:\n"
            "  AZURE_OPENAI_ENDPOINT\n"
            "  AZURE_OPENAI_DEPLOYMENT_NAME"
        )
    
    # Create Azure OpenAI chat client with Azure CLI credentials
    chat_client = AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    
    # Create the base agent with all tools
    base_agent = ChatAgent(
        name="FinancialAnalyst",
        instructions=AGENT_INSTRUCTIONS,
        chat_client=chat_client,
        tools=[
            analyze_revenue,
            generate_chart,
            calculate_kpi,
            export_report,  # This tool requires approval
            search_transactions,
            update_dashboard,
            get_market_insights
        ]
    )
    
    # Wrap agent for AG-UI protocol support
    ag_ui_config = {
        "require_confirmation": True,  # Enable human-in-the-loop for approval_mode tools
        "name": "FinancialAnalyst",
        "description": "AI-powered financial analysis assistant with visualization and reporting capabilities"
    }
    
    # Add state management if enabled
    if enable_state_management:
        ag_ui_config["state_schema"] = {
            "dashboard": {
                "type": "object",
                "description": "Current dashboard state with metrics and visualizations"
            }
        }
        ag_ui_config["predict_state_config"] = {
            "dashboard": {
                "tool": "update_dashboard",
                "tool_argument": "dashboard_data"
            }
        }
    
    # Create AG-UI wrapped agent
    ag_ui_agent = AgentFrameworkAgent(
        agent=base_agent,
        **ag_ui_config
    )
    
    return ag_ui_agent


# Convenience function for direct agent creation
def get_agent() -> AgentFrameworkAgent:
    """Get pre-configured financial analysis agent."""
    return create_financial_agent()
