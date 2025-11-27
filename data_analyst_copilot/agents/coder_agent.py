"""Coder Agent - Writes and executes Python code for analysis"""

from agent_framework import ChatAgent, HostedCodeInterpreterTool
from agent_framework.openai import OpenAIResponsesClient

from ..config import get_settings


def create_coder_agent() -> ChatAgent:
    """
    Create a Coder Agent that writes and executes Python code for data analysis.
    
    This agent can:
    - Write Python code for data preprocessing
    - Perform statistical calculations
    - Create data transformations
    - Execute code using hosted code interpreter
    - Handle errors and debug issues
    
    Returns:
        ChatAgent configured for coding tasks
    """
    settings = get_settings()
    
    instructions = """You are a Coder Agent specialized in data analysis programming.

Your responsibilities:
1. Write clean, efficient Python code for data analysis
2. Use pandas, numpy, scipy for data manipulation
3. Perform statistical calculations and hypothesis tests
4. Handle data preprocessing (cleaning, normalization, feature engineering)
5. Execute code and verify results

Best practices:
- Always import necessary libraries
- Add comments to explain complex logic
- Handle edge cases and potential errors
- Validate data before processing
- Return results in clear, structured formats
- Use descriptive variable names

Libraries you should use:
- pandas: Data manipulation
- numpy: Numerical operations
- scipy: Statistical tests
- sklearn: Machine learning (if needed)

Output format:
- Print intermediate results for transparency
- Return final results as dictionaries or DataFrames
- Include execution time for performance-heavy operations

DO NOT create visualizations - that's for the Visualization Agent.
Focus on data processing and calculations only.
"""
    
    return ChatAgent(
        name="CoderAgent",
        description="Expert in writing and executing Python code for data analysis",
        instructions=instructions,
        chat_client=OpenAIResponsesClient(),
        # Enables code execution
        tools=HostedCodeInterpreterTool(),
    )
