"""Main DataAnalystCopilot class using Magentic-One orchestration"""

import asyncio
import logging
from pathlib import Path
from typing import AsyncIterator, Callable, Optional

from agent_framework import (
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticBuilder,
    MagenticCallbackEvent,
    MagenticCallbackMode,
    MagenticFinalResultEvent,
    MagenticOrchestratorMessageEvent,
    MagenticPlanReviewDecision,
    MagenticPlanReviewReply,
    MagenticPlanReviewRequest,
    RequestInfoEvent,
    WorkflowCompletedEvent,
)
from agent_framework.openai import OpenAIChatClient

from .agents import (
    create_coder_agent,
    create_insights_agent,
    create_report_agent,
    create_research_agent,
    create_visualization_agent,
)
from .config import get_settings

logger = logging.getLogger(__name__)


class DataAnalystCopilot:
    """
    AI Data Analyst Copilot using Magentic-One multi-agent orchestration.
    
    Coordinates specialized agents to perform comprehensive data analysis:
    - Research Agent: Finds and loads datasets
    - Coder Agent: Writes and executes analysis code
    - Visualization Agent: Creates charts and graphs
    - Insights Agent: Interprets results
    - Report Agent: Synthesizes final report
    """
    
    def __init__(
        self,
        enable_plan_review: Optional[bool] = None,
        streaming_mode: Optional[bool] = None,
        on_event: Optional[Callable[[MagenticCallbackEvent], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        """
        Initialize the Data Analyst Copilot.
        
        Args:
            enable_plan_review: Enable human-in-the-loop plan review
            streaming_mode: Enable streaming of agent outputs
            on_event: Custom event callback
            on_error: Custom error handler
        """
        self.settings = get_settings()
        self.enable_plan_review = enable_plan_review or self.settings.enable_plan_review
        self.streaming_mode = streaming_mode or self.settings.streaming_mode
        self.custom_on_event = on_event
        self.custom_on_error = on_error
        
        # State for streaming
        self._last_stream_agent_id: Optional[str] = None
        self._stream_line_open: bool = False
        
        # Create specialized agents
        self.agents = {
            "research": create_research_agent(),
            "coder": create_coder_agent(),
            "visualization": create_visualization_agent(),
            "insights": create_insights_agent(),
            "report": create_report_agent(),
        }
        
        # Build workflow
        self.workflow = self._build_workflow()
        
        logger.info("DataAnalystCopilot initialized with %d agents", len(self.agents))
    
    def _build_workflow(self):
        """Build the Magentic workflow with all agents"""
        builder = (
            MagenticBuilder()
            .participants(**self.agents)
            .on_event(
                self._default_event_handler,
                mode=MagenticCallbackMode.STREAMING if self.streaming_mode else MagenticCallbackMode.COMPLETE
            )
            .with_standard_manager(
                chat_client=OpenAIChatClient(ai_model_id=self.settings.orchestrator_model),
                max_round_count=self.settings.max_round_count,
                max_stall_count=self.settings.max_stall_count,
                max_reset_count=self.settings.max_reset_count,
            )
        )
        
        if self.custom_on_error:
            builder = builder.on_exception(self.custom_on_error)
        
        if self.enable_plan_review:
            builder = builder.with_plan_review()
        
        return builder.build()
    
    async def _default_event_handler(self, event: MagenticCallbackEvent) -> None:
        """Default event handler for workflow events"""
        
        if isinstance(event, MagenticOrchestratorMessageEvent):
            print(f"\n🎯 [ORCHESTRATOR:{event.kind}]")
            print(f"{getattr(event.message, 'text', '')}")
            print("-" * 70)
        
        elif isinstance(event, MagenticAgentDeltaEvent):
            # Streaming tokens from agents
            if self._last_stream_agent_id != event.agent_id or not self._stream_line_open:
                if self._stream_line_open:
                    print()
                agent_emoji = self._get_agent_emoji(event.agent_id)
                print(f"\n{agent_emoji} [{event.agent_id}]: ", end="", flush=True)
                self._last_stream_agent_id = event.agent_id
                self._stream_line_open = True
            print(event.text, end="", flush=True)
        
        elif isinstance(event, MagenticAgentMessageEvent):
            # Complete agent responses
            if self._stream_line_open:
                print(" ✓")
                self._stream_line_open = False
            
            msg = event.message
            if msg is not None:
                agent_emoji = self._get_agent_emoji(event.agent_id)
                response_text = (msg.text or "").replace("\n", " ")[:200]
                print(f"\n{agent_emoji} [{event.agent_id}] {msg.role.value}")
                print(f"   {response_text}...")
                print("-" * 70)
        
        elif isinstance(event, MagenticFinalResultEvent):
            # Final synthesized result
            print("\n" + "=" * 70)
            print("📊 FINAL ANALYSIS REPORT")
            print("=" * 70)
            if event.message is not None:
                print(event.message.text)
            print("=" * 70)
        
        # Call custom handler if provided
        if self.custom_on_event:
            await self.custom_on_event(event)
    
    @staticmethod
    def _get_agent_emoji(agent_id: str) -> str:
        """Get emoji for agent based on ID"""
        emoji_map = {
            "ResearchAgent": "🔍",
            "CoderAgent": "💻",
            "VisualizationAgent": "📊",
            "InsightsAgent": "🧠",
            "ReportAgent": "📝",
        }
        return emoji_map.get(agent_id, "🤖")
    
    async def analyze(self, query: str) -> str:
        """
        Perform data analysis based on a natural language query.
        
        Args:
            query: Natural language description of the analysis to perform
            
        Returns:
            Final analysis report as a string
        """
        logger.info("Starting analysis for query: %s", query[:100])
        
        print("\n" + "=" * 70)
        print("🚀 AI DATA ANALYST COPILOT")
        print("=" * 70)
        print(f"\n📝 Query: {query}\n")
        print("=" * 70)
        
        try:
            if self.enable_plan_review:
                return await self._analyze_with_plan_review(query)
            else:
                return await self._analyze_direct(query)
        except Exception as e:
            logger.exception("Analysis failed")
            if self.custom_on_error:
                self.custom_on_error(e)
            raise
    
    async def _analyze_direct(self, query: str) -> str:
        """Run analysis without plan review"""
        completion_event: Optional[WorkflowCompletedEvent] = None
        
        async for event in self.workflow.run_stream(query):
            if isinstance(event, WorkflowCompletedEvent):
                completion_event = event
        
        if completion_event is not None:
            data = getattr(completion_event, "data", None)
            result = getattr(data, "text", None) or (str(data) if data is not None else "")
            logger.info("Analysis completed successfully")
            return result
        
        raise RuntimeError("Analysis did not complete successfully")
    
    async def _analyze_with_plan_review(self, query: str) -> str:
        """Run analysis with human-in-the-loop plan review"""
        completion_event: Optional[WorkflowCompletedEvent] = None
        pending_request: Optional[RequestInfoEvent] = None
        
        while True:
            # Run until completion or review request
            if pending_request is None:
                async for event in self.workflow.run_stream(query):
                    if isinstance(event, WorkflowCompletedEvent):
                        completion_event = event
                    
                    if isinstance(event, RequestInfoEvent) and event.request_type is MagenticPlanReviewRequest:
                        pending_request = event
                        review_req = event.data
                        if hasattr(review_req, 'plan_text') and review_req.plan_text:
                            print("\n" + "=" * 70)
                            print("📋 PLAN REVIEW REQUEST")
                            print("=" * 70)
                            print(review_req.plan_text)
                            print("=" * 70)
            
            # Check if completed
            if completion_event is not None:
                break
            
            # Handle plan review
            if pending_request is not None:
                reply = await self._get_plan_review_decision()
                
                async for event in self.workflow.send_responses_streaming({pending_request.request_id: reply}):
                    if isinstance(event, WorkflowCompletedEvent):
                        completion_event = event
                    elif isinstance(event, RequestInfoEvent):
                        pending_request = event
                    else:
                        pending_request = None
        
        if completion_event is not None:
            data = getattr(completion_event, "data", None)
            result = getattr(data, "text", None) or (str(data) if data is not None else "")
            logger.info("Analysis with plan review completed successfully")
            return result
        
        raise RuntimeError("Analysis did not complete successfully")
    
    async def _get_plan_review_decision(self) -> MagenticPlanReviewReply:
        """Get user decision on plan review"""
        print("\n🤔 Review the plan above. What would you like to do?")
        print("   1. Approve (proceed with this plan)")
        print("   2. Reject (request a new plan)")
        print("   3. Modify (approve with changes)")
        
        choice = input("\nYour choice (1/2/3): ").strip()
        
        if choice == "2":
            return MagenticPlanReviewReply(decision=MagenticPlanReviewDecision.REJECT)
        elif choice == "3":
            print("\nEnter your modified plan:")
            modified_plan = input().strip()
            return MagenticPlanReviewReply(
                decision=MagenticPlanReviewDecision.APPROVE,
                edited_plan=modified_plan
            )
        else:
            return MagenticPlanReviewReply(decision=MagenticPlanReviewDecision.APPROVE)
    
    async def analyze_stream(self, query: str) -> AsyncIterator[MagenticCallbackEvent]:
        """
        Stream analysis events in real-time.
        
        Args:
            query: Natural language description of the analysis
            
        Yields:
            MagenticCallbackEvent objects as they occur
        """
        logger.info("Starting streaming analysis for query: %s", query[:100])
        
        async for event in self.workflow.run_stream(query):
            yield event
    
    def save_report(self, report: str, filename: Optional[str] = None) -> Path:
        """
        Save analysis report to file.
        
        Args:
            report: Report content to save
            filename: Output filename (auto-generated if not provided)
            
        Returns:
            Path to saved report file
        """
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_report_{timestamp}.md"
        
        output_path = self.settings.output_directory / filename
        output_path.write_text(report, encoding="utf-8")
        
        logger.info("Report saved to: %s", output_path)
        print(f"\n💾 Report saved to: {output_path}")
        
        return output_path


async def main():
    """Example usage"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create copilot
    copilot = DataAnalystCopilot(
        enable_plan_review=False,
        streaming_mode=True
    )
    
    # Example query
    query = """
    Analyze the sales data from the past quarter.
    Load the data, calculate monthly revenue trends,
    identify the top 5 products by revenue,
    create visualizations showing the trends,
    and provide recommendations for the next quarter.
    """
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    
    # Run analysis
    result = await copilot.analyze(query)
    
    # Save report
    copilot.save_report(result)


if __name__ == "__main__":
    asyncio.run(main())
