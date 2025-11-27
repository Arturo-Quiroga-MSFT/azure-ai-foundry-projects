# AG-UI with Microsoft Agent Framework Demo

This demo demonstrates the basic AG-UI integration with Microsoft Agent Framework, featuring:
- **Server**: AG-UI server hosting an AI agent via HTTP
- **Client**: Interactive client with streaming responses
- **Protocol**: Server-Sent Events (SSE) for real-time streaming

## Prerequisites

- Python 3.10 or later
- Azure OpenAI service endpoint and deployment configured
- Azure CLI installed and authenticated (`az login`)
- User has `Cognitive Services OpenAI Contributor` role for the Azure OpenAI resource

## Installation

1. **Activate virtual environment** (already created):
   ```bash
   source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
   ```

2. **Install required packages**:
   ```bash
   pip install agent-framework-ag-ui
   ```

   This installs:
   - `agent-framework-core` - Core agent functionality
   - `agent-framework-ag-ui` - AG-UI integration
   - `fastapi` - Web framework
   - `uvicorn` - ASGI server

3. **Configure environment**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your Azure OpenAI credentials
   ```

## Configuration

Set your Azure OpenAI credentials in `.env`:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```

Or set them directly in your shell:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```

## Running the Demo

### Step 1: Start the Server

In terminal 1:
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
python server.py
```

You should see:
```
🚀 Starting AG-UI Server...
📡 Endpoint: https://your-resource.openai.azure.com/
🤖 Model: gpt-4o-mini
🌐 Server URL: http://127.0.0.1:8888/
```

### Step 2: Run the Client

In terminal 2:
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
python client.py
```

### Step 3: Chat!

```
User: What is 2 + 2?
Assistant: 2 + 2 equals 4.

User: Tell me a fun fact about space
Assistant: Here's a fun fact: A day on Venus is longer than its year! 
Venus takes about 243 Earth days to rotate once on its axis, but only 
about 225 Earth days to orbit the Sun.
```

## Testing with curl

You can also test the server directly with curl:

```bash
curl -N http://127.0.0.1:8888/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is 2 + 2?"}
    ]
  }'
```

## How It Works

### Server-Side Flow
1. Client sends HTTP POST request with messages
2. FastAPI endpoint receives the request
3. `add_agent_framework_fastapi_endpoint` handles routing
4. Agent processes messages using Agent Framework
5. Responses are converted to AG-UI events
6. Events are streamed back as Server-Sent Events (SSE)

### Client-Side Flow
1. `AGUIChatClient` sends HTTP POST to server
2. Server responds with SSE stream
3. Client parses events into `AgentRunResponseUpdate` objects
4. Text content is displayed in real-time
5. Thread context is maintained via `threadId`

### Protocol Events
- `RUN_STARTED` - Run begins (includes threadId, runId)
- `TEXT_MESSAGE_START` - Message starts
- `TEXT_MESSAGE_CONTENT` - Streaming text chunks (delta field)
- `TEXT_MESSAGE_END` - Message ends
- `RUN_FINISHED` - Run completes
- `RUN_ERROR` - Error occurred

## Architecture

```
┌─────────────────┐
│  Client         │  (client.py)
│  AGUIChatClient │
└────────┬────────┘
         │ HTTP POST + SSE
         ▼
┌─────────────────────────┐
│  FastAPI Server         │  (server.py)
│  add_agent_framework_   │
│  fastapi_endpoint       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  ChatAgent              │
│  (Agent Framework)      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  AzureOpenAIChatClient  │
│  (Azure OpenAI)         │
└─────────────────────────┘
```

## Key Concepts

- **AG-UI Protocol**: Standardized protocol for AI agent interfaces
- **Server-Sent Events (SSE)**: Real-time streaming from server to client
- **Thread Management**: Conversation context maintained via threadId
- **FastAPI Integration**: Native async support for streaming
- **Azure Authentication**: Uses AzureCliCredential (DefaultAzureCredential pattern)

## Next Steps

After completing this basic demo, you can explore:

1. **Backend Tool Rendering** - Add server-side function tools
2. **Frontend Tool Rendering** - Add client-side function tools  
3. **CopilotKit Integration** - Build rich web UI with React

## Troubleshooting

### Authentication Errors
Ensure you're logged in to Azure CLI:
```bash
az login
```

### Connection Refused
Make sure the server is running before starting the client.

### Port Already in Use
Change the port in server.py:
```python
uvicorn.run(app, host="127.0.0.1", port=8889)  # Use different port
```

## Resources

- [AG-UI Documentation](https://docs.ag-ui.com/)
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)
- [AG-UI Getting Started](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/getting-started)
