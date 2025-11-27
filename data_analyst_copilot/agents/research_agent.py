"""Research Agent - Finds and loads datasets"""

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

from ..config import get_settings


def create_research_agent() -> ChatAgent:
    """
    Create a Research Agent that specializes in finding and loading datasets.
    
    This agent can:
    - Search for datasets online
    - Load local files (CSV, JSON, Excel, Parquet)
    - Provide data overview and statistics
    - Understand data schema and structure
    
    Returns:
        ChatAgent configured for research tasks
    """
    settings = get_settings()
    
    instructions = """You are a Research Agent specialized in data discovery and loading.

Your responsibilities:
1. Find relevant datasets based on user queries
2. Load data from various formats (CSV, JSON, Excel, Parquet)
3. Provide initial data overview (shape, columns, data types)
4. Identify potential data quality issues
5. Suggest data preprocessing steps

When loading data:
- Check file format and size
- Display first few rows for preview
- Report basic statistics (null counts, unique values)
- Identify the target variable if it's a prediction task
- Note any anomalies or data quality concerns

Always provide clear, concise summaries of what you found.
DO NOT perform complex analysis - that's for the Coder Agent.
Focus on data discovery and initial exploration only.
"""
    
    return ChatAgent(
        name="ResearchAgent",
        description="Specialist in finding datasets and providing data overviews",
        instructions=instructions,
        # Uses search-enabled model for finding datasets
        chat_client=OpenAIChatClient(ai_model_id=settings.research_model),
    )
