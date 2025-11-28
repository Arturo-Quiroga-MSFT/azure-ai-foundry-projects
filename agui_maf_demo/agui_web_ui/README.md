# CopilotKit + AG-UI Demo

This demo shows how to integrate **CopilotKit** (React UI components) with **Microsoft Agent Framework** via the **AG-UI protocol**.

## Architecture

```
┌─────────────────────┐         AG-UI Protocol         ┌──────────────────────┐
│                     │  ◄──── (Server-Sent Events) ───►│                      │
│  Next.js Frontend   │                                 │  Python AG-UI Server │
│  (CopilotKit UI)    │         HTTP POST               │  (FastAPI)           │
│                     │  ────► (User messages) ─────►   │                      │
└─────────────────────┘                                 └──────────────────────┘
        │                                                         │
        │ Frontend Tools                                          │ Backend Tools
        │ (Browser-side)                                          │ (Server-side)
        │                                                         │
        ▼                                                         ▼
  • get_user_location                                    • get_weather
  • read_local_preferences                               • search_restaurants
  • get_device_info                                      • calculate
  • show_notification                                    • get_current_time
```

## Features

### Frontend (React/Next.js with CopilotKit)
- 🎨 **CopilotChat component**: Professional chat UI with streaming responses
- 🔧 **Frontend tools** using `useFrontendTool` hook:
  - Browser geolocation (with IP fallback)
  - LocalStorage preferences
  - Device/browser information
  - In-app notifications
- 📊 **Live dashboard**: Shows notifications and device info in sidebar

### Backend (Python AG-UI Server)
- 🤖 **Microsoft Agent Framework**: ChatAgent with Azure OpenAI
- 🛠️ **Backend tools** via `@ai_function`:
  - Weather lookup
  - Restaurant search
  - Mathematical calculations
  - Timezone-aware time
- 🌐 **AG-UI protocol**: FastAPI server with SSE streaming

## Setup

### 1. Install Frontend Dependencies

```bash
cd copilotkit_demo
npm install
```

### 2. Start the Backend Server

In a terminal from the parent directory:

```bash
cd ..
python server_with_tools.py
```

Server will run on `http://127.0.0.1:8888`

### 3. Start the Frontend

In another terminal:

```bash
cd copilotkit_demo
npm run dev
```

Frontend will run on `http://localhost:3000`

### 4. Open Your Browser

Navigate to `http://localhost:3000` and start chatting!

## Try These Queries

### Backend Tools (Server-side execution)
- "What's the weather in Paris?"
- "Find me Italian restaurants in London"
- "Calculate 123 * 456"
- "What time is it in Tokyo?"

### Frontend Tools (Browser-side execution)
- "Where am I?" → Gets your actual location
- "What are my preferences?" → Reads localStorage
- "What device am I using?" → Shows in sidebar
- "Remind me to take a break" → Creates notification

### Combined Queries
- "What's the weather in my location?" → Uses frontend tool to get location, then backend tool for weather
- "Show me restaurants near me" → Combines location + restaurant search

## How It Works

### AG-UI Protocol
1. **Frontend → Backend**: User messages sent via HTTP POST to `/thread/run`
2. **Backend → Frontend**: Streaming responses via Server-Sent Events (SSE)
3. **Tool Calls**: 
   - Backend tools execute on server, results streamed back
   - Frontend tools execute in browser, results sent to server, then incorporated into response

### CopilotKit Integration
- `CopilotKit` provider connects to AG-UI server via `runtimeUrl` prop with `agui` flag
- `CopilotChat` renders the chat interface
- `useFrontendTool` registers browser-accessible functions
- Frontend tools automatically forwarded to agent via AG-UI protocol

## Project Structure

```
copilotkit_demo/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main chat page with frontend tools
│   └── globals.css         # Global styles
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── next.config.ts          # Next.js config
├── tailwind.config.ts      # Tailwind CSS config
└── README.md               # This file
```

## Key Technologies

- **Next.js 15**: React framework with App Router
- **CopilotKit**: React components for AI chat UI
- **TypeScript**: Type-safe frontend code
- **Tailwind CSS**: Utility-first styling
- **AG-UI Protocol**: Server-Sent Events + HTTP POST
- **Microsoft Agent Framework**: Python agent backend

## Next Steps

Explore other CopilotKit features:
- **Generative UI**: Render custom components based on agent output
- **Human-in-the-loop**: Approval flows for sensitive actions
- **Shared State**: Synchronize agent state with React state
- **Authentication**: Add user auth to AG-UI server

Check the [CopilotKit docs](https://docs.copilotkit.ai/microsoft-agent-framework) for more!
