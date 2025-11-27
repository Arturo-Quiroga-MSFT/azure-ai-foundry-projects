import { CopilotPopup } from "@copilotkit/react-ui";
import { useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";
import FinancialDashboard from "./components/FinancialDashboard";
import "./App.css";

function App() {
  const [dashboardData, setDashboardData] = useState<any>(null);

  // Handle chart generation from agent
  useCopilotAction({
    name: "generate_chart",
    description: "Render a financial chart visualization",
    parameters: [
      {
        name: "chart_data",
        type: "object",
        description: "Chart configuration and data",
        required: true
      }
    ],
    render: ({ args }) => {
      // Update dashboard with new chart
      setDashboardData((prev: any) => ({
        ...prev,
        latestChart: args.chart_data
      }));
      return null; // Dashboard will render the chart
    }
  });

  // Handle export report approval
  useCopilotAction({
    name: "export_report",
    description: "Export financial report (requires approval)",
    parameters: [
      {
        name: "report_type",
        type: "string",
        description: "Type of report to export"
      },
      {
        name: "format",
        type: "string",
        description: "Output format (pdf, excel, csv)"
      }
    ],
    renderAndWaitForResponse: ({ args, respond }) => {
      const handleApprove = () => {
        respond?.({ approved: true });
      };

      const handleCancel = () => {
        respond?.({ approved: false });
      };

      return (
        <div className="approval-dialog">
          <h3>🔒 Approve Report Export</h3>
          <p>
            The agent wants to export a <strong>{args.report_type}</strong> report
            in <strong>{args.format}</strong> format.
          </p>
          <div className="dialog-actions">
            <button onClick={handleApprove} className="btn-approve">
              ✅ Approve
            </button>
            <button onClick={handleCancel} className="btn-cancel">
              ❌ Cancel
            </button>
          </div>
        </div>
      );
    }
  });

  return (
    <div className="app">
      <header className="app-header">
        <h1>💼 Financial Analysis AI</h1>
        <p>Powered by AG-UI + CopilotKit + Azure AI Foundry</p>
      </header>

      <main className="app-main">
        <FinancialDashboard data={dashboardData} />
        
        <div className="info-panel">
          <h2>🤖 Your AI Financial Analyst</h2>
          <p>
            Click the chat icon to interact with your AI financial analyst.
            Try asking:
          </p>
          <ul>
            <li>"Analyze Q4 2024 revenue trends"</li>
            <li>"Create a line chart of monthly growth"</li>
            <li>"Calculate ROI for this quarter"</li>
            <li>"Export a detailed financial report"</li>
            <li>"What are the current market insights?"</li>
          </ul>
          
          <div className="features">
            <h3>✨ Features</h3>
            <div className="feature-grid">
              <div className="feature">
                <span>📊</span>
                <div>
                  <strong>Real-time Analysis</strong>
                  <p>Streaming insights as they're generated</p>
                </div>
              </div>
              <div className="feature">
                <span>📈</span>
                <div>
                  <strong>Dynamic Charts</strong>
                  <p>Interactive visualizations rendered live</p>
                </div>
              </div>
              <div className="feature">
                <span>🔒</span>
                <div>
                  <strong>Approval Workflows</strong>
                  <p>Human-in-the-loop for sensitive operations</p>
                </div>
              </div>
              <div className="feature">
                <span>🔄</span>
                <div>
                  <strong>State Sync</strong>
                  <p>Dashboard updates in real-time</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <CopilotPopup
        instructions="You are a financial analysis AI assistant. Help users analyze revenue, create charts, calculate KPIs, and generate reports. Always explain your findings clearly."
        labels={{
          title: "Financial Analyst AI",
          initial: "Hello! I'm your AI financial analyst. How can I help you today?"
        }}
        defaultOpen={false}
      />
    </div>
  );
}

export default App;
