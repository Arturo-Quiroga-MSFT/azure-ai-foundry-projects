# Magentic Orchestration vs. Simple Orchestrator

This directory now contains **two different orchestration approaches** for comparison:

## 1. Simple Orchestrator (`server_multi_agent.py`)

### Architecture:
- **Single OrchestratorAgent** with all tools
- Agent selects tools directly based on user query
- Simple, straightforward approach
- Tools: `get_weather`, `web_search`, `calculate`, `execute_python_code`

### When to Use:
✅ Straightforward queries with clear intent  
✅ Single-domain tasks  
✅ Quick responses needed  
✅ Predictable workflows  

### Example Queries:
- "What's the weather in Paris?"
- "Search for AI news"
- "Plot a sine wave"

### How It Works:
```
User Query → OrchestratorAgent → Select Tool → Execute → Return Result
```

---

## 2. Magentic Orchestration (`server_magentic.py`) 

### Architecture:
- **Magentic Manager** dynamically coordinates specialized agents
- **3 Specialized Agents**: ResearchAgent, WeatherAgent, DataAnalystAgent
- Manager builds task ledger and adapts plan in real-time
- Iterative refinement through agent collaboration

### When to Use:
✅ Complex, multi-step problems  
✅ Open-ended tasks without predetermined solution  
✅ Requires research → analysis → visualization workflow  
✅ Need for dynamic planning and backtracking  

### Example Queries:
- "Research the top 3 AI trends, then create visualizations comparing their adoption rates"
- "Find weather in 5 major cities and create a comparison chart"
- "Search for Python best practices and analyze code examples statistically"

### How It Works:
```
User Query → Magentic Manager 
             ↓
         Build Plan
             ↓
    Select Agent (ResearchAgent/WeatherAgent/DataAnalyst)
             ↓
    Execute & Evaluate Progress
             ↓
    Refine Plan (iterate if needed)
             ↓
    Synthesize Final Result
```

---

## Key Differences

| Feature | Simple Orchestrator | Magentic Orchestration |
|---------|-------------------|----------------------|
| **Complexity** | Low | High |
| **Agent Count** | 1 (with tools) | 4 (Manager + 3 specialists) |
| **Planning** | No explicit planning | Dynamic task ledger |
| **Iteration** | Single pass | Multiple rounds |
| **Progress Tracking** | None | Built-in stall detection |
| **Backtracking** | No | Yes |
| **Best For** | Simple queries | Complex, multi-step tasks |

---

## Running the Servers

### Simple Orchestrator (Port 8888):
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python server_multi_agent.py
```

### Magentic Orchestration (Port 8888):
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python server_magentic.py
```

**Note:** Both use the same port (8888), so stop one before starting the other!

---

## Testing Magentic Orchestration

Try these complex queries to see Magentic's power:

### 1. Multi-Step Research + Visualization:
```
"Research the current temperature in London, Paris, and Tokyo. 
Then create a bar chart comparing them."
```

**Expected Flow:**
1. Manager → WeatherAgent (3x for each city)
2. Manager → DataAnalystAgent (create chart)
3. Manager → Synthesize result

### 2. Web Search + Data Analysis:
```
"Search for information about Python vs JavaScript popularity. 
Then create a visualization showing the comparison."
```

**Expected Flow:**
1. Manager → ResearchAgent (web search)
2. Manager → DataAnalystAgent (analyze and visualize)
3. Manager → Synthesize insights

### 3. Complex Calculation + Explanation:
```
"Calculate the first 10 Fibonacci numbers, then plot them 
and explain the golden ratio relationship."
```

**Expected Flow:**
1. Manager → DataAnalystAgent (calculate Fibonacci)
2. Manager → DataAnalystAgent (create plot)
3. Manager → Synthesize with explanation

---

## Observing Magentic in Action

When running `server_magentic.py`, you'll see console output showing:

```
[MANAGER:PLANNING]
Task ledger being built...

[MANAGER:SELECTING_AGENT]
Choosing ResearchAgent for web search...

[ResearchAgent] assistant
Performing web search...

[MANAGER:EVALUATING_PROGRESS]
Progress: 50% complete, moving to next step...

[DataAnalystAgent] assistant
Creating visualization...

[MANAGER:FINAL_SYNTHESIS]
Combining results...

=========================
FINAL RESULT:
=========================
```

This shows the **dynamic coordination** in action!

---

## UI Works with Both!

The React UI (`agui_web_ui/`) works seamlessly with both servers since they both:
- Use AG-UI protocol (SSE streaming)
- Support rich content markers ([IMAGE_ID], [WEATHER_ICON], [LINK], [CALC_RESULT])
- Run on http://127.0.0.1:8888/

Just switch servers and refresh the UI to compare!

---

## Which Should You Use?

### Use **Simple Orchestrator** if:
- Queries are straightforward
- Single-domain tasks
- Fast responses are critical
- You want simpler debugging

### Use **Magentic Orchestration** if:
- Complex, open-ended problems
- Multi-step workflows
- Need dynamic planning
- Want to leverage specialized agents
- Building enterprise-grade agentic systems

---

## Next Steps

1. **Try both servers** with the same queries
2. **Compare response quality** and coordination
3. **Monitor console output** to see Magentic's planning
4. **Test complex queries** that benefit from multi-agent collaboration

The Magentic pattern truly shines when tasks require **research → analysis → synthesis** workflows!
