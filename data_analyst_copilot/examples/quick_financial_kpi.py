"""Quick Financial KPI Dashboard Analysis

A faster version focusing on key metrics and dashboards.
"""

import asyncio
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from copilot import DataAnalystCopilot


async def main():
    """Run quick KPI dashboard analysis"""
    logging.basicConfig(level=logging.INFO)
    
    # Create copilot without plan review for faster execution
    copilot = DataAnalystCopilot(
        enable_plan_review=False,
        streaming_mode=True
    )
    
    query = """
    Quick Financial KPI Dashboard - Revenue Analysis
    
    Data: 'revenue_data.csv' and 'quarterly_metrics.csv'
    
    Generate a concise KPI dashboard showing:
    
    1. **Top-Line Metrics**
       - Total revenue (current month vs last month vs same month last year)
       - Month-over-month growth rate
       - Year-to-date revenue
       - Revenue run rate (annualized)
    
    2. **Performance by Segment**
       - Revenue by product category (with growth rates)
       - Revenue by region (with market share)
       - Top 3 product-region combinations
    
    3. **Efficiency Metrics**
       - Gross margin by category
       - Marketing efficiency (CAC and revenue per marketing dollar)
       - Revenue per customer
    
    4. **Key Visualizations**
       - Revenue trend chart (last 12 months)
       - Category performance comparison (bar chart)
       - Regional split (pie chart)
       - Growth rate heatmap by category and region
    
    5. **Quick Insights**
       - Identify the fastest growing segment
       - Flag any concerning trends
       - Quick win opportunities
    
    Format as an executive dashboard - concise, visual, actionable.
    Focus on the most important metrics only.
    """
    
    print("\n📊 Generating Financial KPI Dashboard...\n")
    
    result = await copilot.analyze(query)
    report_path = copilot.save_report(result, "financial_kpi_dashboard.md")
    
    print(f"\n✅ Dashboard complete! Saved to: {report_path}\n")


if __name__ == "__main__":
    asyncio.run(main())
