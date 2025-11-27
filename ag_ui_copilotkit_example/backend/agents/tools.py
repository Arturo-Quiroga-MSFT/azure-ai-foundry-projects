"""
Financial Analysis Tools for AG-UI Agent

These tools demonstrate various capabilities:
- Backend tool execution with streaming results
- Human-in-the-loop approvals for sensitive operations
- State management and updates
- Data processing and visualization generation
"""

from typing import Annotated, Any
import json
from datetime import datetime, timedelta
from agent_framework import ai_function
from pydantic import Field
import random


@ai_function
def analyze_revenue(
    period: Annotated[str, Field(description="Time period (e.g., 'Q4 2024', 'last 6 months')")],
    include_forecast: Annotated[bool, Field(description="Include forecast predictions")] = True
) -> dict[str, Any]:
    """
    Analyze revenue trends for a given period.
    Returns detailed analysis including trends, growth rates, and forecasts.
    """
    # Simulated revenue data
    base_revenue = 750000
    months = ["October", "November", "December"]
    
    revenue_data = {
        "period": period,
        "total_revenue": 0,
        "monthly_breakdown": [],
        "metrics": {}
    }
    
    # Generate monthly data with growth
    for i, month in enumerate(months):
        monthly_revenue = base_revenue + (i * 85000) + random.randint(-20000, 30000)
        revenue_data["monthly_breakdown"].append({
            "month": month,
            "revenue": monthly_revenue,
            "growth": ((monthly_revenue - base_revenue) / base_revenue * 100) if i > 0 else 0
        })
        revenue_data["total_revenue"] += monthly_revenue
    
    # Calculate metrics
    avg_monthly = revenue_data["total_revenue"] / len(months)
    yoy_growth = 18.5  # Simulated
    
    revenue_data["metrics"] = {
        "average_monthly_revenue": avg_monthly,
        "yoy_growth_percentage": yoy_growth,
        "strongest_month": max(revenue_data["monthly_breakdown"], key=lambda x: x["revenue"])["month"],
        "trend": "upward" if yoy_growth > 0 else "downward"
    }
    
    # Add forecast if requested
    if include_forecast:
        last_revenue = revenue_data["monthly_breakdown"][-1]["revenue"]
        avg_growth = sum(m["growth"] for m in revenue_data["monthly_breakdown"][1:]) / (len(months) - 1)
        
        revenue_data["forecast"] = {
            "next_quarter_estimate": last_revenue * 3 * (1 + avg_growth/100),
            "confidence": "high",
            "assumptions": f"Based on {avg_growth:.1f}% average monthly growth"
        }
    
    return revenue_data


@ai_function
def generate_chart(
    chart_type: Annotated[str, Field(description="Type of chart: line, bar, pie")],
    data_source: Annotated[str, Field(description="Data to visualize (e.g., 'monthly revenue', 'growth rates')")],
    title: Annotated[str, Field(description="Chart title")] = "Financial Analysis"
) -> dict[str, Any]:
    """
    Generate chart visualization data.
    Returns structured data that can be rendered by frontend components.
    """
    # Simulated chart data generation
    chart_data = {
        "type": chart_type,
        "title": title,
        "data": [],
        "config": {
            "responsive": True,
            "maintainAspectRatio": False
        }
    }
    
    if "revenue" in data_source.lower():
        chart_data["data"] = [
            {"label": "October", "value": 765000},
            {"label": "November", "value": 850000},
            {"label": "December", "value": 950000}
        ]
        chart_data["config"]["yAxisLabel"] = "Revenue ($)"
        chart_data["config"]["xAxisLabel"] = "Month"
    
    elif "growth" in data_source.lower():
        chart_data["data"] = [
            {"label": "October", "value": 0},
            {"label": "November", "value": 11.1},
            {"label": "December", "value": 17.6}
        ]
        chart_data["config"]["yAxisLabel"] = "Growth Rate (%)"
        chart_data["config"]["xAxisLabel"] = "Month"
    
    else:
        # Default data
        chart_data["data"] = [
            {"label": "Category A", "value": 45},
            {"label": "Category B", "value": 30},
            {"label": "Category C", "value": 25}
        ]
    
    return chart_data


@ai_function
def calculate_kpi(
    kpi_name: Annotated[str, Field(description="KPI to calculate (e.g., 'ROI', 'profit margin', 'customer acquisition cost')")],
    time_period: Annotated[str, Field(description="Time period for calculation")] = "Q4 2024"
) -> dict[str, Any]:
    """
    Calculate specific financial KPIs.
    Returns the KPI value, trend, and contextual information.
    """
    # Simulated KPI calculations
    kpis = {
        "roi": {
            "value": 24.5,
            "unit": "%",
            "trend": "increasing",
            "benchmark": 18.0,
            "status": "above_target"
        },
        "profit margin": {
            "value": 32.8,
            "unit": "%",
            "trend": "stable",
            "benchmark": 30.0,
            "status": "above_target"
        },
        "customer acquisition cost": {
            "value": 145,
            "unit": "$",
            "trend": "decreasing",
            "benchmark": 180,
            "status": "above_target"
        },
        "ltv": {
            "value": 2850,
            "unit": "$",
            "trend": "increasing",
            "benchmark": 2500,
            "status": "above_target"
        }
    }
    
    # Normalize KPI name
    kpi_key = kpi_name.lower().replace("_", " ")
    
    # Find matching KPI
    for key, data in kpis.items():
        if key in kpi_key or kpi_key in key:
            return {
                "kpi_name": kpi_name,
                "time_period": time_period,
                "current_value": data["value"],
                "unit": data["unit"],
                "trend": data["trend"],
                "benchmark": data["benchmark"],
                "status": data["status"],
                "interpretation": f"{kpi_name} is {data['status'].replace('_', ' ')} with a {data['trend']} trend"
            }
    
    # Default response if KPI not found
    return {
        "kpi_name": kpi_name,
        "time_period": time_period,
        "error": f"KPI '{kpi_name}' not available in current dataset",
        "available_kpis": list(kpis.keys())
    }


@ai_function(approval_mode="always_require")
def export_report(
    report_type: Annotated[str, Field(description="Type of report: summary, detailed, executive")],
    format: Annotated[str, Field(description="Output format: pdf, excel, csv")] = "pdf",
    include_charts: Annotated[bool, Field(description="Include visualization charts")] = True
) -> dict[str, Any]:
    """
    Export financial analysis report.
    
    **REQUIRES APPROVAL** - This operation generates and exports a report.
    User will be prompted to approve before execution.
    """
    # Simulated report generation
    report_metadata = {
        "report_type": report_type,
        "format": format,
        "include_charts": include_charts,
        "generated_at": datetime.now().isoformat(),
        "file_name": f"Financial_Report_{report_type}_{datetime.now().strftime('%Y%m%d')}.{format}",
        "file_size": "2.4 MB",
        "status": "generated",
        "download_url": f"/api/reports/download/{datetime.now().timestamp()}"
    }
    
    return report_metadata


@ai_function
def search_transactions(
    query: Annotated[str, Field(description="Search query for transactions")],
    limit: Annotated[int, Field(description="Maximum number of results")] = 10,
    filters: Annotated[dict, Field(description="Filter criteria")] = None
) -> dict[str, Any]:
    """
    Search financial transactions.
    Returns matching transactions with details.
    """
    # Simulated transaction search
    transactions = []
    
    for i in range(min(limit, 5)):
        transactions.append({
            "transaction_id": f"TXN-{1000 + i}",
            "date": (datetime.now() - timedelta(days=i*7)).strftime("%Y-%m-%d"),
            "amount": random.randint(500, 5000),
            "description": f"Transaction {i+1}",
            "category": random.choice(["Revenue", "Expense", "Investment"]),
            "status": "completed"
        })
    
    return {
        "query": query,
        "total_results": len(transactions),
        "transactions": transactions,
        "filters_applied": filters or {}
    }


@ai_function
def update_dashboard(
    dashboard_data: Annotated[dict, Field(description="Dashboard metrics and visualizations")]
) -> dict[str, Any]:
    """
    Update dashboard state with new data.
    This tool is used for state management in AG-UI protocol.
    """
    # Process and validate dashboard data
    processed_data = {
        "updated_at": datetime.now().isoformat(),
        "metrics": dashboard_data.get("metrics", {}),
        "charts": dashboard_data.get("charts", []),
        "alerts": dashboard_data.get("alerts", []),
        "status": "updated"
    }
    
    return processed_data


@ai_function
def get_market_insights(
    sector: Annotated[str, Field(description="Market sector (e.g., 'technology', 'finance')")],
    timeframe: Annotated[str, Field(description="Analysis timeframe")] = "current"
) -> dict[str, Any]:
    """
    Get market insights and trends for a specific sector.
    Returns analysis of market conditions and recommendations.
    """
    # Simulated market insights
    insights = {
        "sector": sector,
        "timeframe": timeframe,
        "overall_sentiment": "positive",
        "key_trends": [
            "Strong consumer demand in Q4",
            "Digital transformation accelerating",
            "Increased investment in AI/ML"
        ],
        "market_indicators": {
            "sector_growth": 15.3,
            "volatility_index": "moderate",
            "investor_confidence": 72
        },
        "recommendations": [
            "Focus on high-growth segments",
            "Monitor competitive landscape",
            "Invest in innovation initiatives"
        ]
    }
    
    return insights
