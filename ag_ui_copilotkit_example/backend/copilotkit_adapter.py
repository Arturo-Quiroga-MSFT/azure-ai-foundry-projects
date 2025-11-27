"""
CopilotKit Adapter for AG-UI Agent

This adapter translates between CopilotKit's expected format and AG-UI protocol.
"""

import json
import logging
from typing import AsyncIterator, Dict, Any, List
from fastapi import Request
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)


async def copilotkit_adapter_endpoint(request: Request, agent) -> StreamingResponse:
    """
    Adapter endpoint that translates CopilotKit requests to AG-UI and back.
    
    CopilotKit expects:
    - Input: {"messages": [...], "threadId": "...", ...}
    - Output: SSE stream with specific event format
    """
    try:
        body = await request.json()
        messages = body.get("messages", [])
        thread_id = body.get("threadId")
        
        logger.info(f"CopilotKit request: {len(messages)} messages, thread: {thread_id}")
        
        # Convert CopilotKit messages to AG-UI format
        agui_request = {
            "messages": messages,
            "threadId": thread_id
        }
        
        async def event_generator() -> AsyncIterator[str]:
            """Generate CopilotKit-compatible SSE events from AG-UI protocol."""
            try:
                # Call AG-UI agent
                response = await agent.run_stream(agui_request)
                
                assistant_message = ""
                message_id = None
                
                async for event in response:
                    event_type = event.get("type")
                    
                    if event_type == "TEXT_MESSAGE_START":
                        message_id = event.get("messageId")
                        # Send CopilotKit message start event
                        yield f"data: {json.dumps({'type': 'message_start', 'id': message_id})}\n\n"
                    
                    elif event_type == "TEXT_MESSAGE_CONTENT":
                        delta = event.get("delta", "")
                        assistant_message += delta
                        # Send CopilotKit content delta
                        yield f"data: {json.dumps({'type': 'content', 'delta': delta})}\n\n"
                    
                    elif event_type == "TEXT_MESSAGE_END":
                        # Send final message
                        yield f"data: {json.dumps({'type': 'message', 'message': {'role': 'assistant', 'content': assistant_message}})}\n\n"
                    
                    elif event_type == "TOOL_CALL_START":
                        tool_name = event.get("toolName")
                        tool_args = event.get("arguments", {})
                        logger.info(f"Tool call: {tool_name}")
                        yield f"data: {json.dumps({'type': 'tool_call', 'name': tool_name, 'args': tool_args})}\n\n"
                    
                    elif event_type == "RUN_COMPLETED":
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
                # Final done signal
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"Error in event generator: {e}", exc_info=True)
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    except Exception as e:
        logger.error(f"Adapter error: {e}", exc_info=True)
        return StreamingResponse(
            iter([f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"]),
            media_type="text/event-stream"
        )
