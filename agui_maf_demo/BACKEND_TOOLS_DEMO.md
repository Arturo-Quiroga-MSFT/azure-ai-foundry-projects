# Backend Tool Rendering Demo

This demo showcases **backend tool rendering** with AG-UI and Microsoft Agent Framework. The AI agent can call server-side function tools to perform specific tasks, with tool calls and results automatically streamed to the client.

## What is Backend Tool Rendering?

Backend tool rendering means:
- **Function tools are defined on the server**
- **The AI agent decides when to call these tools** based on user requests
- **Tools execute on the backend (server-side)** with secure access to resources
- **Tool call events and results are streamed to the client** in real-time
- **The client displays tool execution progress** for transparency

## Benefits

✅ **Security** - Sensitive operations stay on the server  
✅ **Consistency** - All clients use the same tool implementations  
✅ **Transparency** - Clients can display tool execution progress  
✅ **Flexibility** - Update tools without changing client code

## Available Tools

### 1. `get_weather(location)`
Get current weather for a location.

**Example:** "What's the weather in Paris, France?"

### 2. `search_restaurants(location, cuisine, max_results)`
Search for restaurants in a specific location.

**Example:** "Find Italian restaurants in London"

### 3. `calculate(expression)`
Perform mathematical calculations.

**Example:** "Calculate 123 * 456"

### 4. `get_current_time(timezone)`
Get current time in a specific timezone.

**Example:** "What time is it in Tokyo?"

## Running the Demo

### Terminal 1: Start the Server with Tools

```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python server_with_tools.py
```

You should see:
```
🚀 Starting AG-UI Server with Backend Tools...
📡 Endpoint: https://...openai.azure.com/
🤖 Model: gpt-4.1-mini
🔧 Tools: get_weather, search_restaurants, calculate, get_current_time
🌐 Server URL: http://127.0.0.1:8888/
```

### Terminal 2: Run the Enhanced Client

```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python client_with_tools.py
```

## Example Interactions

### Weather Query
```
User: What's the weather in Paris, France?

  🔧 Calling tool: get_weather
  📋 Arguments: {'location': 'Paris, France'}
  ⏳ Executing...

  ✅ Result: The weather in Paris, France is sunny, 22°C.