# Frontend Tool Rendering Demo

This demo showcases **frontend tool rendering** with AG-UI and Microsoft Agent Framework. The AI agent can request execution of client-side tools that run in the user's local environment.

## What is Frontend Tool Rendering?

Frontend tool rendering means:
- **Function tools are defined on the client** and registered with the agent
- **The AI agent decides when to call these tools** based on user requests
- **Tools execute on the client side** with access to local resources
- **The server orchestrates** when tools should be called but doesn't execute them
- **Tool results are sent back to the server** for the agent to use in its response

## Benefits

✅ **Privacy** - Sensitive local data stays on the client  
✅ **Device Access** - Can use GPS, sensors, local storage  
✅ **Personalization** - Access to user-specific preferences  
✅ **Flexibility** - Different clients can have different tools

## Available Frontend Tools

### 1. `get_user_location()`
Get the user's current GPS location (simulated).

**Returns:** Latitude, longitude, city, country

**Example:** "Where am I?" or "What's my current location?"

### 2. `read_local_preferences()`
Read user preferences from local storage (simulated).

**Returns:** Theme, language, notification settings, units, currency

**Example:** "What are my preferences?" or "What language am I using?"

### 3. `get_device_info()`
Get information about the user's device.

**Returns:** Platform, OS version, architecture, processor

**Example:** "What device am I using?" or "Tell me about my system"

### 4. `show_notification(title, message, urgency)`
Display a notification to the user (simulated in console).

**Parameters:**
- `title`: Notification title
- `message`: Notification message
- `urgency`: "low", "normal", or "high"

**Example:** "Remind me to take a break" or "Show me a notification"

## Running the Demo

### Terminal 1: Start the Basic Server

```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python server.py
```

**Important:** Use the basic `server.py`, NOT `server_with_tools.py`. Frontend tools are registered on the client side only.

### Terminal 2: Run the Frontend Tools Client

```bash
cd /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/agui_maf_demo
source /Users/arturoquiroga/GITHUB/FOUNDRY-Nov-2025/.venv/bin/activate
python client_frontend_tools.py
```

## Example Interactions

### Location Query
```
User: Where am I?

  🔧 Frontend Tool: get_user_location
  📋 Arguments: {}
  ⏳ Executing locally...
  ✅ Result: {'latitude': 52.3676, 'longitude': 4.9041, 'city': 'Amsterdam', ...}