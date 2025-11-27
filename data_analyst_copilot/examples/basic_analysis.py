"""Basic data analysis example"""

import asyncio
import logging

from copilot import DataAnalystCopilot


async def main():
    """Run a basic analysis"""
    logging.basicConfig(level=logging.INFO)
    
    # Create copilot
    copilot = DataAnalystCopilot(
        enable_plan_review=False,
        streaming_mode=True
    )
    
    # Define analysis query
    query = """
    I have a dataset called 'monthly_sales.csv' with columns: Date, Product, Revenue, Units_Sold.
    
    Please:
    1. Load and examine the data
    2. Calculate total revenue and units sold per product
    3. Identify the top 5 products by revenue
    4. Create a bar chart showing revenue by product
    5. Calculate month-over-month growth rate
    6. Create a line plot showing revenue trends over time
    7. Provide insights on which products are performing best
    8. Recommend products to focus on for next quarter
    
    Generate a comprehensive report with all findings and visualizations.
    """
    
    # Run analysis
    print("🚀 Starting basic data analysis...\n")
    result = await copilot.analyze(query)
    
    # Save report
    report_path = copilot.save_report(result, "basic_analysis_report.md")
    
    print(f"\n✅ Analysis complete! Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
