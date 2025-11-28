"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
  agentName?: string;
}

// Function to parse and render rich content
function RichContent({ content }: { content: string }) {
  // Parse weather icons
  const weatherIconMatch = content.match(/\[WEATHER_ICON\](.*?)\[\/WEATHER_ICON\]/);
  const weatherIcon = weatherIconMatch ? weatherIconMatch[1] : null;
  let displayContent = content.replace(/\[WEATHER_ICON\].*?\[\/WEATHER_ICON\]/g, "");
  
  // Parse links
  const linkRegex = /\[LINK\](.*?)\[\/LINK\]/g;
  const links: string[] = [];
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    links.push(match[1]);
  }
  displayContent = displayContent.replace(linkRegex, "");
  
  // Parse calculation results
  const calcMatch = content.match(/\[CALC_RESULT\](.*?)\[\/CALC_RESULT\]/);
  const calcResult = calcMatch ? calcMatch[1] : null;
  displayContent = displayContent.replace(/\[CALC_RESULT\].*?\[\/CALC_RESULT\]/g, "");
  
  // Parse image IDs (not base64 - images stored on server)
  const imageIdRegex = /\[IMAGE_ID\](.*?)\[\/IMAGE_ID\]/g;
  const imageIds: string[] = [];
  while ((match = imageIdRegex.exec(content)) !== null) {
    imageIds.push(match[1]);
  }
  displayContent = displayContent.replace(imageIdRegex, "");
  
  // Convert markdown-style bold and code to HTML
  displayContent = displayContent.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  displayContent = displayContent.replace(/`(.*?)`/g, "<code style='background:#f3f4f6;padding:2px 6px;border-radius:4px;'>$1</code>");
  
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
      <div dangerouslySetInnerHTML={{ __html: displayContent.replace(/\n/g, "<br/>") }} />
      
      {weatherIcon && (
        <div style={{ 
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          padding: "1rem",
          borderRadius: "0.5rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "center"
        }}>
          <img src={weatherIcon} alt="Weather" style={{ width: "64px", height: "64px" }} />
        </div>
      )}
      
      {calcResult && (
        <div style={{
          background: "#10b981",
          color: "white",
          padding: "1rem",
          borderRadius: "0.5rem",
          fontSize: "1.5rem",
          fontWeight: "bold",
          textAlign: "center"
        }}>
          = {calcResult}
        </div>
      )}
      
      {imageIds.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem", marginTop: "0.5rem" }}>
          {imageIds.map((imageId, idx) => (
            <div 
              key={idx} 
              style={{ 
                background: "white",
                padding: "1rem",
                borderRadius: "0.5rem",
                border: "1px solid #e5e7eb",
                boxShadow: "0 1px 3px rgba(0,0,0,0.1)"
              }}
            >
              <img 
                src={`${backendUrl}/images/${imageId}`} 
                alt={`Visualization ${idx + 1}`} 
                style={{ 
                  width: "100%", 
                  height: "auto",
                  borderRadius: "0.25rem"
                }} 
              />
            </div>
          ))}
        </div>
      )}
      
      {links.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem", marginTop: "0.5rem" }}>
          {links.map((link, idx) => (
            <a
              key={idx}
              href={link}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: "#2563eb",
                textDecoration: "none",
                fontSize: "0.875rem",
                padding: "0.5rem",
                background: "#eff6ff",
                borderRadius: "0.375rem",
                border: "1px solid #bfdbfe",
                display: "block",
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                cursor: "pointer",
                transition: "all 0.2s"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#dbeafe";
                e.currentTarget.style.borderColor = "#60a5fa";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "#eff6ff";
                e.currentTarget.style.borderColor = "#bfdbfe";
              }}
            >
              🔗 {link}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

export default function Home() {
  const [backendUrl, setBackendUrl] = useState("http://127.0.0.1:8888");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! 👋 I'm your AG-UI assistant with code interpreter capabilities. I can help you with weather, web search, calculations, data analytics, and visualizations. What would you like to explore?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load backend URL from runtime config
  useEffect(() => {
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        if (data.backendUrl) {
          setBackendUrl(data.backendUrl);
        }
      })
      .catch(() => {
        // Fallback to localhost for development
        console.log("Using localhost backend");
      });
  }, []);

  const sampleQuestions = [
    "🌤️ Research weather in Paris and London, then create a comparison chart",
    "📊 Find the top 3 AI trends and visualize their adoption rates",
    "🎨 Create a beautiful 3D surface plot of z = sin(√(x² + y²))",
    "🌍 What's the weather in Tokyo and show me a temperature visualization",
    "🔬 Plot the Mandelbrot set fractal with color gradient",
    "📈 Search for recent breakthroughs in quantum computing and show timeline",
    "🧮 Calculate (45 * 89) + (123 / 4) - 56 and explain the steps",
    "📉 Analyze this sales data and create insights: Q1=120, Q2=150, Q3=95, Q4=200",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleQuestionClick = (question: string) => {
    if (isLoading) return;
    setInput(question);
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    const updatedMessages = [...messages, { role: "user" as const, content: userMessage }];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      // Send full conversation history to maintain context
      const response = await fetch(`${backendUrl}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map(m => ({ role: m.role, content: m.content })),
        }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = "";
      let currentAgentName = "OrchestratorAgent";

      if (reader) {
        setMessages((prev) => [...prev, { role: "assistant", content: "", agentName: currentAgentName }]);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6);
              if (data === "[DONE]") continue;

              try {
                const json = JSON.parse(data);
                
                // Detect agent changes from TEXT_MESSAGE_START
                if (json.type === "TEXT_MESSAGE_START" && json.role === "assistant") {
                  // Agent name might be in future events, for now use default
                  currentAgentName = "Assistant";
                }
                
                if (json.type === "TEXT_MESSAGE_CONTENT" && json.delta) {
                  assistantMessage += json.delta;
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1].content = assistantMessage;
                    newMessages[newMessages.length - 1].agentName = currentAgentName;
                    return newMessages;
                  });
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, there was an error connecting to the server." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", background: "#fff" }}>
        {/* Header */}
        <div style={{ padding: "1rem", borderBottom: "1px solid #e5e7eb", background: "#f9fafb" }}>
          <h1 style={{ margin: 0, fontSize: "1.25rem", fontWeight: "600" }}>🤖 AG-UI Assistant</h1>
          <p style={{ margin: "0.25rem 0 0 0", fontSize: "0.875rem", color: "#6b7280" }}>
            Powered by Microsoft Agent Framework
          </p>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "1.5rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{ display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
              <div style={{ maxWidth: "70%", display: "flex", flexDirection: "column", gap: "0.25rem" }}>
                {msg.role === "assistant" && msg.agentName && (
                  <div style={{ fontSize: "0.75rem", color: "#6b7280", paddingLeft: "0.5rem" }}>
                    🤖 {msg.agentName}
                  </div>
                )}
                <div
                  style={{
                    padding: "0.75rem 1rem",
                    borderRadius: "0.75rem",
                    background: msg.role === "user" ? "#2563eb" : "#f3f4f6",
                    color: msg.role === "user" ? "#fff" : "#111827",
                    wordBreak: "break-word",
                  }}
                >
                  {msg.role === "user" ? msg.content : <RichContent content={msg.content} />}
                </div>
              </div>
            </div>
          ))}
          {isLoading && messages[messages.length - 1]?.role !== "assistant" && (
            <div style={{ display: "flex", justifyContent: "flex-start" }}>
              <div style={{ padding: "0.75rem 1rem", borderRadius: "0.75rem", background: "#f3f4f6", color: "#6b7280" }}>
                Thinking...
              </div>
            </div>
          )}
          
          {/* Sample Questions */}
          {messages.length === 1 && !isLoading && (
            <div style={{ marginTop: "2rem" }}>
              <p style={{ fontSize: "0.875rem", color: "#6b7280", marginBottom: "0.75rem", fontWeight: "500" }}>
                Try asking:
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {sampleQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuestionClick(question)}
                    style={{
                      padding: "0.75rem 1rem",
                      background: "#fff",
                      border: "1px solid #e5e7eb",
                      borderRadius: "0.5rem",
                      fontSize: "0.875rem",
                      color: "#374151",
                      cursor: "pointer",
                      textAlign: "left",
                      transition: "all 0.2s",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = "#2563eb";
                      e.currentTarget.style.background = "#eff6ff";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = "#e5e7eb";
                      e.currentTarget.style.background = "#fff";
                    }}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={sendMessage} style={{ padding: "1rem", borderTop: "1px solid #e5e7eb", background: "#f9fafb" }}>
          <div style={{ display: "flex", gap: "0.5rem" }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              disabled={isLoading}
              style={{
                flex: 1,
                padding: "0.75rem 1rem",
                border: "1px solid #d1d5db",
                borderRadius: "0.5rem",
                fontSize: "0.875rem",
                outline: "none",
              }}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              style={{
                padding: "0.75rem 1.5rem",
                background: isLoading || !input.trim() ? "#9ca3af" : "#2563eb",
                color: "#fff",
                border: "none",
                borderRadius: "0.5rem",
                fontSize: "0.875rem",
                fontWeight: "500",
                cursor: isLoading || !input.trim() ? "not-allowed" : "pointer",
              }}
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
