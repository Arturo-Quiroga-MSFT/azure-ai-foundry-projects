# Financial Analysis Examples

This directory contains specialized examples for financial analysis use cases using the AI Data Analyst Copilot.

## 📊 Available Examples

### 1. Comprehensive Revenue Forecasting (`financial_analysis.py`)
**Best for:** Strategic planning, board presentations, annual budgeting

**Features:**
- Complete historical trend analysis
- Profitability analysis by product and region
- Time series forecasting with confidence intervals
- 8+ professional visualizations
- Strategic recommendations for 2025
- Executive summary suitable for leadership

**Runtime:** ~5-10 minutes (includes plan review)

**Run:**
```bash
python financial_analysis.py
```

### 2. Quick KPI Dashboard (`quick_financial_kpi.py`)
**Best for:** Daily monitoring, quick insights, tactical decisions

**Features:**
- Essential KPIs and metrics
- Fast execution (no plan review)
- Dashboard-style visualizations
- Quick win identification
- Concise insights

**Runtime:** ~2-3 minutes

**Run:**
```bash
python quick_financial_kpi.py
```

## 📁 Sample Data

### `revenue_data.csv`
Monthly revenue data for 2024 including:
- Date
- Product Category (Electronics, Clothing, Home & Garden)
- Region (North America, Europe)
- Revenue
- Units Sold
- Cost of Goods
- Marketing Spend
- Customer Acquisition

**11 months of data** (January - November 2024)

### `quarterly_metrics.csv`
Quarterly business metrics from Q1 2023 to Q4 2024:
- Total Revenue
- Operating Costs
- Net Profit
- Profit Margin
- Market Share
- Customer Lifetime Value
- Churn Rate

**8 quarters of data** covering 2 years

## 🎯 Analysis Capabilities

### Trend Analysis
- Month-over-month growth rates
- Year-over-year comparisons
- Seasonality detection
- Moving averages and trends

### Profitability Analysis
- Gross profit margins
- Marketing ROI
- Customer acquisition cost (CAC)
- Customer lifetime value (CLV)
- Product-region profitability matrix

### Forecasting
- ARIMA/exponential smoothing models
- 6-month revenue projections
- Confidence intervals
- Trend extrapolation
- Scenario analysis

### Visualizations
- Time series charts
- Stacked area charts
- Regional comparisons
- Correlation heatmaps
- Forecast plots with confidence bands
- ROI analysis charts

### Strategic Insights
- Growth opportunity identification
- Risk factor assessment
- Budget allocation recommendations
- Pricing strategy suggestions
- Market expansion priorities

## 💡 Customization

### Modify the Analysis

1. **Change forecast horizon:**
```python
query = """
...
Build a time series model to forecast revenue for the next 12 months
...
"""
```

2. **Focus on specific categories:**
```python
query = """
...
Focus the analysis on Electronics category only.
Compare performance across all regions.
...
"""
```

3. **Add scenario analysis:**
```python
query = """
...
Create three scenarios:
- Conservative: 5% growth
- Base case: Current trends continue
- Optimistic: 15% growth with expanded marketing
...
"""
```

### Use Your Own Data

Replace the sample CSV files with your data. Ensure columns match:

**revenue_data.csv requirements:**
- Date column (date format)
- Revenue column (numeric)
- Any categorical columns (product, region, etc.)

**quarterly_metrics.csv requirements:**
- Quarter column (text or date)
- Financial metrics (numeric columns)

Then update the query to reference your column names.

## 📈 Expected Outputs

### Charts Generated
1. `revenue_trend.png` - Historical revenue with moving average
2. `revenue_by_category.png` - Category breakdown
3. `regional_comparison.png` - North America vs Europe
4. `profit_margins.png` - Margin trends over time
5. `revenue_forecast.png` - 6-month forecast with confidence bands
6. `marketing_roi.png` - ROI by category
7. `cac_trends.png` - Customer acquisition cost trends
8. `correlation_heatmap.png` - Key metrics correlation

### Reports Generated
- Markdown report with full analysis
- Executive summary
- Detailed findings
- Recommendations
- Methodology appendix

## 🔧 Troubleshooting

### Data Loading Issues
If data fails to load, ensure:
- CSV files are in `sample_data/` directory
- File paths are correct
- CSV format is valid (no corrupt lines)

### Forecast Errors
If forecasting fails:
- Check for sufficient historical data (need 12+ data points)
- Ensure no missing values in time series
- Verify date column is properly formatted

### Performance Issues
If analysis is slow:
- Use quick KPI version for faster results
- Reduce number of visualizations requested
- Limit forecast horizon
- Disable plan review

## 🚀 Next Steps

1. Run the comprehensive analysis first to understand capabilities
2. Review the generated report and visualizations
3. Customize queries for your specific needs
4. Integrate with your data sources
5. Schedule regular analysis runs
6. Build dashboards from generated insights

## 💼 Business Value

**For CFOs/Finance Teams:**
- Automated monthly reporting
- Data-driven budget planning
- Risk identification
- Performance tracking

**For Strategy Teams:**
- Market opportunity analysis
- Competitive positioning
- Growth planning
- Investment prioritization

**For Operations:**
- Resource allocation
- Efficiency optimization
- Performance monitoring
- Tactical decision support

---

**Questions or Issues?** Check the main README or create an issue in the repository.
