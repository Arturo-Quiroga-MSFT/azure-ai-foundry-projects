# AI Data Analyst Copilot

A multi-agent system powered by Magentic-One orchestration that takes natural language queries and performs comprehensive data analysis.

## Features

- 🔍 **Research Agent**: Finds and loads relevant datasets
- 💻 **Coder Agent**: Writes and executes Python code for analysis
- 📊 **Visualization Agent**: Creates charts and graphs
- 🧠 **Insights Agent**: Interprets results and provides recommendations
- 📝 **Report Agent**: Generates shareable analysis reports
- 👤 **Human-in-the-Loop**: Review and approve analysis plans before execution

## Architecture

The system uses Magentic orchestration with a manager that dynamically coordinates specialized agents:

```
User Query → Magentic Manager → [Selects Agents Dynamically]
                                 ↓
                    ┌────────────┴────────────┐
                    │                         │
            Research Agent              Coder Agent
                    │                         │
            Visualization Agent      Insights Agent
                    │                         │
                    └────────────┬────────────┘
                                 ↓
                          Report Agent
                                 ↓
                          Final Report
```

## Agents

### 1. Research Agent
- Searches for datasets
- Loads CSV, JSON, Excel files
- Provides data overview and statistics

### 2. Coder Agent
- Writes Python code for analysis
- Executes code using hosted code interpreter
- Handles data preprocessing and calculations

### 3. Visualization Agent
- Creates matplotlib/seaborn visualizations
- Generates interactive plots
- Exports charts as images

### 4. Insights Agent
- Interprets analysis results
- Identifies patterns and trends
- Provides actionable recommendations

### 5. Report Agent
- Synthesizes all findings
- Creates structured reports
- Generates executive summaries

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Azure AI Foundry**:
- Set up your Azure AI Foundry project
- Deploy required models (gpt-4o, gpt-4o-search-preview)
- Update configuration in `config.py`

3. **Set environment variables**:
```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-account.services.ai.azure.com/api/projects/your-project"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"
```

## Usage

### Basic Usage

```python
from data_analyst_copilot import DataAnalystCopilot

copilot = DataAnalystCopilot()

query = """
Analyze the sales data from the past quarter.
Calculate monthly revenue, identify top products,
and create visualizations showing trends.
"""

result = await copilot.analyze(query)
print(result)
```

### With Human-in-the-Loop

```python
copilot = DataAnalystCopilot(enable_plan_review=True)

# The copilot will pause and ask you to review the plan
# before executing the analysis
result = await copilot.analyze(query)
```

### Example Queries

1. **Sales Analysis**:
   ```
   Analyze sales_data.csv and identify the top 5 products by revenue.
   Create a bar chart and calculate growth rate month-over-month.
   ```

2. **Customer Segmentation**:
   ```
   Load customer data, segment by purchase behavior, and visualize
   the segments with scatter plots. Recommend marketing strategies.
   ```

3. **Financial Forecasting**:
   ```
   Analyze revenue trends, fit a time series model, and predict
   next quarter's revenue. Show confidence intervals.
   ```

## Project Structure

```
data_analyst_copilot/
├── README.md
├── requirements.txt
├── config.py                    # Configuration
├── main.py                      # Main entry point
├── copilot.py                   # DataAnalystCopilot class
├── agents/
│   ├── __init__.py
│   ├── research_agent.py        # Research agent
│   ├── coder_agent.py          # Coder agent
│   ├── visualization_agent.py   # Visualization agent
│   ├── insights_agent.py        # Insights agent
│   └── report_agent.py          # Report agent
├── examples/
│   ├── basic_analysis.py
│   ├── with_plan_review.py
│   └── sample_data/
│       ├── sales_data.csv
│       └── customer_data.csv
└── outputs/
    └── .gitkeep
```

## Examples

See the `examples/` directory for detailed examples:
- `basic_analysis.py` - Simple data analysis workflow
- `with_plan_review.py` - Analysis with human plan review
- `streaming_demo.py` - Real-time streaming of agent work

## Advanced Features

### Custom Agents

Add your own specialized agents:

```python
from agent_framework import ChatAgent

custom_agent = ChatAgent(
    name="StatisticalTestAgent",
    description="Performs statistical hypothesis tests",
    instructions="You run statistical tests like t-tests, ANOVA, chi-square.",
    chat_client=OpenAIChatClient()
)

copilot.add_agent(custom_agent)
```

### Event Callbacks

Monitor agent collaboration in real-time:

```python
async def on_agent_event(event):
    if event.agent_id == "CoderAgent":
        print(f"Code executed: {event.message.text}")

copilot.on_event(on_agent_event)
```

### Error Handling

```python
copilot = DataAnalystCopilot(
    max_retries=3,
    on_error=lambda e: print(f"Error: {e}")
)
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `max_round_count` | 15 | Maximum collaboration rounds |
| `max_stall_count` | 3 | Rounds without progress before reset |
| `enable_plan_review` | False | Enable human plan approval |
| `streaming_mode` | True | Stream agent outputs in real-time |
| `output_directory` | `./outputs` | Directory for generated files |

## Best Practices

1. **Start with small datasets** for testing
2. **Enable plan review** for complex analyses
3. **Monitor streaming output** to understand agent coordination
4. **Provide clear, specific queries** for best results
5. **Review generated code** before running on production data

## Troubleshooting

### Common Issues

**Issue**: Agents not collaborating effectively
- Solution: Increase `max_round_count` or provide more specific instructions

**Issue**: Code execution fails
- Solution: Check that code interpreter tool is properly configured

**Issue**: Visualizations not generated
- Solution: Ensure output directory has write permissions

## Contributing

Contributions welcome! Areas for enhancement:
- Additional specialized agents (ML, NLP, etc.)
- More visualization types
- Database connectivity
- API data sources
- Export to different formats (PDF, PowerPoint)

## License

MIT License

## Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Magentic-One Orchestration](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/magentic)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
