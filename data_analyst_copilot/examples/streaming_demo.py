"""Example demonstrating real-time streaming of agent work"""

import asyncio
import logging

from agent_framework import (
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticFinalResultEvent,
    MagenticOrchestratorMessageEvent,
    WorkflowCompletedEvent,
)

from copilot import DataAnalystCopilot


async def custom_event_handler(event):
    """Custom handler to track specific events"""
    if isinstance(event, MagenticOrchestratorMessageEvent):
        print(f"\n📌 Manager is planning: {event.kind}")
    elif isinstance(event, MagenticAgentMessageEvent):
        print(f"\n✨ Agent '{event.agent_id}' completed a task")


async def main():
    """Stream analysis events in real-time"""
    logging.basicConfig(level=logging.DEBUG)
    
    # Create copilot with custom event handler
    copilot = DataAnalystCopilot(
        enable_plan_review=False,
        streaming_mode=True,
        on_event=custom_event_handler
    )
    
    # Define analysis query
    query = """
    Quick analysis of website traffic data:
    
    1. Load 'web_traffic.csv' (columns: Date, Page, Visitors, Bounce_Rate)
    2. Calculate total visitors per page
    3. Identify pages with highest bounce rate
    4. Create a visualization comparing page performance
    5. Recommend pages that need optimization
    
    Keep it concise - focus on actionable insights.
    """
    
    print("🚀 Starting streaming analysis demo...\n")
    print("📡 You'll see agent collaboration in real-time\n")
    
    # Stream events
    final_result = None
    async for event in copilot.analyze_stream(query):
        # Process events as they come
        if isinstance(event, MagenticAgentDeltaEvent):
            # Real-time token streaming
            pass  # Already handled by default handler
        
        elif isinstance(event, WorkflowCompletedEvent):
            final_result = event.data
    
    # Display final result
    if final_result:
        result_text = getattr(final_result, "text", str(final_result))
        report_path = copilot.save_report(result_text, "streaming_demo_report.md")
        print(f"\n✅ Streaming analysis complete! Report: {report_path}")
    else:
        print("\n⚠️  Analysis completed but no result received")


if __name__ == "__main__":
    asyncio.run(main())
