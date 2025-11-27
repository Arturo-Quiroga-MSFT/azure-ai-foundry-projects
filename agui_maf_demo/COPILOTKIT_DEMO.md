# CopilotKit Integration Demo

This demo showcases how to build a **full-stack AI agent application** using:
- **Backend**: Microsoft Agent Framework (Python) with AG-UI protocol
- **Frontend**: CopilotKit (React/Next.js) with professional chat UI

## What is CopilotKit?

**CopilotKit** is a React framework for building AI-native applications. It provides:
- 🎨 **Pre-built UI components**: `CopilotChat`, `CopilotSidebar`, `CopilotPopup`
- 🔧 **Frontend tools**: Register browser-side functions your agent can call
- 🎭 **Generative UI**: Render custom React components based on agent actions
- 👥 **Human-in-the-loop**: Approval flows for sensitive operations
- 🔄 **Shared state**: Sync agent state with React component state

## Architecture Overview

```
┌──────────────────────────────────────────┐
│          Browser (localhost:3000)        │
│  ┌────────────────────────────────────┐  │
│  │     CopilotKit React App           │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │   CopilotChat Component      │  │  │
│  │  │   (Professional chat UI)     │  │  │
│  │  └──────────────────────────────┘  │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │   useFrontendTool hooks      │  │  │
│  │  │   • get_user_location        │  │  │
│  │  │   • read_local_preferences   │  │  │
│  │  │   • get_device_info          │  │  │
│  │  │   • show_notification        │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
                    │
                    │ AG-UI Protocol
                    │ (SSE + HTTP POST)
                    ▼
┌──────────────────────────────────────────┐
│      Python Server (localhost:8888)      │
│  ┌────────────────────────────────────┐  │
│  │    Microsoft Agent Framework       │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │   ChatAgent                  │  │  │
│  │  │   (Azure OpenAI)             │  │  │
│  │  └──────────────────────────────┘  │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │   @ai_function tools         │  │  │
│  │  │   • get_weather              │  │  │
│  │  │   • search_restaurants       │  │  │
│  │  │   • calculate                │  │  │
│  │  │   • get_current_time         │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## Key Features

### 1. Professional Chat UI (CopilotChat)
- Modern, responsive design
- Streaming responses with typewriter effect
- Tool execution visualization
- Markdown rendering
- Code syntax highlighting
- Copy-to-clipboard for code blocks

### 2. Frontend Tools (Browser-side)
Tools that execute in the user's browser:

**get_user_location**
- Tries browser Geolocation API first
- Falls back to IP-based geolocation
- Returns coordinates, city, region, country

**read_local_preferences**
- Reads from localStorage
- Returns theme, language, notifications settings
- Auto-detects timezone from browser

**get_device_info**
- Platform, user agent, screen size
- Window dimensions, language
- Online status, cookies enabled

**show_notification**
- Displays in-app notification in sidebar
- Also uses browser Notification API if permitted
- Supports different types (info, success, warning, error)

### 3. Backend Tools (Server-side)
Tools that execute on the Python server:

**get_weather**
- Simulated weather data (can connect to real API)
- Returns temperature and conditions

**search_restaurants**
- Filter by cuisine type
- Limit number of results
- Returns name, rating, price level

**calculate**
- Safe mathematical expression evaluation
- Supports basic arithmetic operations

**get_current_time**
- Timezone-aware time lookup
- Uses pytz for accurate timezone handling

### 4. Live Dashboard
Sidebar shows:
- Real-time notifications as they're created
- Device information after first query
- Visual feedback for frontend tool execution

## Running the Demo

### Terminal 1: Backend Server
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
python server_with_tools.py
```

Output:
```
🚀 Starting AG-UI Server with Backend Tools...
📡 Endpoint: https://aq-ai-foundry-sweden-central.openai.azure.com/
🤖 Model: gpt-4.1-mini
🔧 Tools: get_weather, search_restaurants, calculate, get_current_time
🌐 Server URL: http://127.0.0.1:8888/
```

### Terminal 2: Frontend Dev Server
```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo/copilotkit_demo
npm install  # First time only
npm run dev
```

Output:
```
  ▲ Next.js 15.1.3
  - Local:        http://localhost:3000

 ✓ Starting...
 ✓ Ready in 2.1s
```

### Browser
Open `http://localhost:3000` and start chatting!

## Example Conversations

### Example 1: Location-based Weather
```
User: What's the weather in my location?