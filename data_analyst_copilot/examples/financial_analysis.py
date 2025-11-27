"""Financial Analysis: Revenue Forecasting and Trend Analysis

This example demonstrates how to use the AI Data Analyst Copilot for:
- Revenue trend analysis
- Seasonality detection
- Growth rate calculations
- Revenue forecasting using time series models
- ROI analysis
- Actionable financial recommendations
"""

import asyncio
import logging
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from copilot import DataAnalystCopilot


async def main():
    """Run comprehensive financial analysis"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create copilot with plan review enabled
    # (important for financial analysis - you want to review the approach)
    copilot = DataAnalystCopilot(
        enable_plan_review=True,  # Review analysis plan before execution
        streaming_mode=True
    )
    
    # Define comprehensive financial analysis query
    query = """
    FINANCIAL ANALYSIS: Revenue Forecasting & Trend Analysis
    
    I have two datasets:
    1. 'revenue_data.csv' - Monthly revenue data for 2024 by product category and region
    2. 'quarterly_metrics.csv' - Quarterly business metrics from Q1 2023 to Q4 2024
    
    Please perform a comprehensive financial analysis:
    
    ## Part 1: Historical Trend Analysis
    1. Load both datasets and examine the data structure
    2. Calculate total revenue growth rate (month-over-month and year-over-year)
    3. Identify seasonality patterns in revenue
    4. Analyze revenue by product category - which categories are growing fastest?
    5. Compare regional performance (North America vs Europe)
    6. Calculate revenue per customer and customer acquisition cost trends
    
    ## Part 2: Profitability Analysis
    1. Calculate gross profit margins by category
    2. Analyze marketing ROI (Revenue/Marketing_Spend ratio)
    3. Identify the most profitable product-region combinations
    4. Calculate customer lifetime value trends from quarterly data
    5. Analyze the relationship between marketing spend and revenue growth
    
    ## Part 3: Time Series Forecasting
    1. Build a time series model to forecast revenue for the next 6 months
    2. Use appropriate method (e.g., ARIMA, exponential smoothing, or linear regression with trend)
    3. Provide confidence intervals for forecasts
    4. Identify key drivers of revenue (seasonality, trend, category mix)
    5. Calculate expected revenue for Q1 2025 and Q2 2025
    
    ## Part 4: Visualizations
    Create the following charts:
    1. Revenue trend over time (line chart with moving average)
    2. Revenue by category (stacked area chart)
    3. Regional comparison (grouped bar chart by month)
    4. Profit margin trends (line chart)
    5. Revenue forecast with confidence intervals (line chart with shaded area)
    6. Marketing ROI by category (bar chart)
    7. Customer acquisition cost trends (line chart)
    8. Correlation heatmap of key financial metrics
    
    ## Part 5: Strategic Insights & Recommendations
    Provide:
    1. Key findings from the analysis
    2. Revenue forecast for next 6 months with confidence levels
    3. Identification of growth opportunities
    4. Risk factors and concerns
    5. Actionable recommendations for:
       - Product mix optimization
       - Regional expansion priorities
       - Marketing budget allocation
       - Pricing strategies
       - Customer retention initiatives
    6. Expected ROI if recommendations are implemented
    
    ## Output Requirements
    - Use rigorous statistical methods
    - Validate assumptions and model fit
    - Provide numerical evidence for all claims
    - Create professional, publication-quality visualizations
    - Generate an executive summary suitable for board presentation
    - Include detailed methodology in appendix
    
    This analysis will inform our strategic planning and budget allocation for 2025.
    """
    
    print("\n" + "=" * 80)
    print("💰 FINANCIAL ANALYSIS: REVENUE FORECASTING & TREND ANALYSIS")
    print("=" * 80)
    print("\n📊 This analysis will provide:")
    print("   • Historical revenue trends and growth rates")
    print("   • Profitability analysis by product and region")
    print("   • 6-month revenue forecast with confidence intervals")
    print("   • Strategic recommendations for 2025")
    print("\n⚠️  Plan Review: You'll review the analysis approach before execution")
    print("=" * 80 + "\n")
    
    # Run analysis with plan review
    result = await copilot.analyze(query)
    
    # Save comprehensive report
    report_path = copilot.save_report(result, "financial_analysis_revenue_forecast.md")
    
    print("\n" + "=" * 80)
    print("✅ FINANCIAL ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n📄 Report saved to: {report_path}")
    print("\n📊 The report includes:")
    print("   ✓ Revenue trend analysis with growth rates")
    print("   ✓ Profitability breakdown by category and region")
    print("   ✓ 6-month revenue forecast with confidence intervals")
    print("   ✓ Strategic recommendations for 2025")
    print("   ✓ Professional visualizations")
    print("\n💼 Ready to share with executive team!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        logging.exception("Financial analysis failed")
