import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";
import App from './App.tsx'
import './index.css'

const runtimeUrl = import.meta.env.VITE_AGUI_SERVER_URL || "http://localhost:8888/agent";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <CopilotKit runtimeUrl={runtimeUrl}>
      <App />
    </CopilotKit>
  </StrictMode>,
)
