"""Example with human-in-the-loop plan review"""

import asyncio
import logging

from copilot import DataAnalystCopilot


async def main():
    """Run analysis with plan review"""
    logging.basicConfig(level=logging.INFO)
    
    # Create copilot with plan review enabled
    copilot = DataAnalystCopilot(
        enable_plan_review=True,  # Enable human review
        streaming_mode=True
    )
    
    # Define analysis query
    query = """
    Analyze customer churn data from 'customer_churn.csv'.
    
    The dataset includes:
    - Customer demographics (age, gender, location)
    - Account information (tenure, monthly charges, total charges)
    - Services subscribed (internet, phone, streaming, etc.)
    - Churn status (yes/no)
    
    Please:
    1. Load and explore the data
    2. Calculate overall churn rate
    3. Identify features most correlated with churn
    4. Segment customers by churn risk
    5. Create visualizations showing churn patterns
    6. Perform statistical tests to validate findings
    7. Build a simple predictive model (logistic regression)
    8. Provide recommendations to reduce churn
    
    This is a critical analysis for our retention strategy.
    """
    
    print("🚀 Starting analysis with plan review...\n")
    print("⚠️  You will be asked to review and approve the analysis plan before execution.\n")
    
    # Run analysis (will pause for plan review)
    result = await copilot.analyze(query)
    
    # Save report
    report_path = copilot.save_report(result, "churn_analysis_report.md")
    
    print(f"\n✅ Analysis complete! Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
