# Code Interpreter Capabilities

## Overview
The AG-UI assistant now includes powerful code interpreter capabilities for data analytics and visualization.

## Features

### 1. Python Code Execution
- Execute Python code safely in a sandboxed environment
- Access to popular data science libraries:
  - **NumPy**: Numerical computing
  - **Pandas**: Data manipulation and analysis
  - **Matplotlib**: Data visualization
  - **Seaborn**: Statistical data visualization

### 2. Data Analytics
- Statistical analysis
- Data transformations
- Pattern recognition
- Trend analysis
- Correlation analysis

### 3. Visualizations
- Line charts
- Bar charts
- Scatter plots
- Histograms
- Heatmaps
- Box plots
- And more!

## Usage Examples

### Example 1: Simple Bar Chart
```
Create a bar chart comparing sales: Q1=50, Q2=75, Q3=60, Q4=90
```

The assistant will:
1. Write Python code using matplotlib
2. Execute the code
3. Capture the generated chart
4. Display it as an inline image in the chat

### Example 2: Statistical Analysis
```
Analyze this data: [23, 45, 67, 89, 34, 56, 78, 90, 12, 43] 
Show mean, median, std deviation, and create a histogram
```

The assistant will:
1. Use NumPy for calculations
2. Create visualizations with matplotlib
3. Display both text output and charts

### Example 3: Advanced Visualization
```
Plot a sine and cosine wave from 0 to 2π with different colors
```

### Example 4: Data Comparison
```
Compare these datasets and show correlation:
Sales: [100, 120, 140, 130, 150]
Marketing: [20, 25, 30, 28, 35]
```

## How It Works

### Backend (Python)
1. **execute_python_code** tool receives code from the AI
2. Code executes in a controlled environment
3. stdout/stderr captured for text output
4. matplotlib figures captured as PNG images
5. Images encoded as base64
6. Results returned with `[IMAGE]base64data[/IMAGE]` markers

### Frontend (React)
1. RichContent component parses response
2. Extracts `[IMAGE]` markers
3. Renders base64 images as inline PNG
4. Displays in clean white cards with shadows

## Rich Content Markers

The system uses special markers to embed rich content:
- `[IMAGE]base64data[/IMAGE]` - Visualization images
- `[WEATHER_ICON]url[/WEATHER_ICON]` - Weather icons
- `[LINK]url[/LINK]` - Clickable links
- `[CALC_RESULT]value[/CALC_RESULT]` - Calculation badges

## Sample Questions

Try these questions to explore the capabilities:

1. **Basic Chart**: "Create a bar chart showing monthly revenue: Jan=10k, Feb=15k, Mar=12k"

2. **Statistical Analysis**: "Generate 100 random numbers and show their distribution with a histogram"

3. **Multiple Plots**: "Create 4 subplots: sine, cosine, tangent, and exponential functions"

4. **Data Comparison**: "Compare two lists [1,2,3,4,5] and [5,4,3,2,1] with scatter plot"

5. **Heatmap**: "Create a correlation heatmap for random data (5x5 matrix)"

## Security

- Code executes in a controlled Python environment
- Access to safe data science libraries only
- No file system access
- No network access from executed code
- Timeout protections (handled by AG-UI)

## Limitations

- Maximum image size: ~2MB per chart
- Complex visualizations may take longer to generate
- Interactive plots converted to static images
- Code must complete within reasonable time

## Architecture

```
User Query
    ↓
AI Agent (OrchestratorAgent)
    ↓
execute_python_code tool
    ↓
Python Interpreter
    ↓
Capture: stdout + matplotlib figures
    ↓
Encode: base64 PNG
    ↓
Return: Text + [IMAGE] markers
    ↓
React UI: Parse and render
    ↓
Display: Charts + Output
```

## Future Enhancements

Possible additions:
- Plotly for interactive charts
- scikit-learn for ML capabilities
- CSV/Excel file upload
- Data persistence
- Export charts as files
- Code history and reuse
