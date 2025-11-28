"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
  agentName?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! 👋 I'm your AG-UI assistant. I can help you with weather, restaurants, calculations, and more. What would you like to know?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sampleQuestions = [
    "What's the weather in Paris?",
    "Calculate 123 * 456",
    "Find Italian restaurants in London",
    "What time is it in Tokyo?",
    "Search the web for latest AI news",
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
      const response = await fetch("http://127.0.0.1:8888/", {
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
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                  }}
                >
                  {msg.content}
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
