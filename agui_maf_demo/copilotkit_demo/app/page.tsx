"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { useFrontendTool } from "@copilotkit/react-core";
import { useState } from "react";

export default function Home() {
  const [notifications, setNotifications] = useState<string[]>([]);
  const [deviceInfo, setDeviceInfo] = useState<Record<string, any>>({});

  // Frontend tool: Get user location
  useFrontendTool({
    name: "get_user_location",
    description: "Get the user's current GPS location from their browser",
    parameters: [],
    handler: async () => {
      return new Promise((resolve) => {
        if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              resolve({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy_meters: position.coords.accuracy,
                method: "Browser Geolocation API",
              });
            },
            (error) => {
              // Fallback to IP-based location
              fetch("https://ipapi.co/json/")
                .then((res) => res.json())
                .then((data) => {
                  resolve({
                    latitude: data.latitude,
                    longitude: data.longitude,
                    accuracy_meters: 1000,
                    city: data.city,
                    region: data.region,
                    country: data.country_name,
                    method: "IP-based geolocation",
                  });
                })
                .catch(() => {
                  resolve({
                    error: "Location unavailable",
                    method: "failed",
                  });
                });
            }
          );
        } else {
          resolve({
            error: "Geolocation not supported",
            method: "failed",
          });
        }
      });
    },
  });

  // Frontend tool: Read local preferences
  useFrontendTool({
    name: "read_local_preferences",
    description: "Read user preferences from browser local storage",
    parameters: [],
    handler: async () => {
      if (typeof window !== "undefined") {
        const theme = localStorage.getItem("theme") || "dark";
        const language = localStorage.getItem("language") || "en";
        const notifications = localStorage.getItem("notifications_enabled") === "true";
        
        return {
          theme,
          language,
          notifications_enabled: notifications,
          preferred_temperature_unit: "celsius",
          preferred_currency: "CAD",
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };
      }
      return { error: "localStorage not available" };
    },
  });

  // Frontend tool: Get device info
  useFrontendTool({
    name: "get_device_info",
    description: "Get information about the user's device and browser",
    parameters: [],
    handler: async () => {
      if (typeof window !== "undefined") {
        const info = {
          platform: navigator.platform,
          userAgent: navigator.userAgent,
          language: navigator.language,
          screenWidth: window.screen.width,
          screenHeight: window.screen.height,
          windowWidth: window.innerWidth,
          windowHeight: window.innerHeight,
          cookiesEnabled: navigator.cookieEnabled,
          online: navigator.onLine,
        };
        setDeviceInfo(info);
        return info;
      }
      return { error: "Device info unavailable" };
    },
  });

  // Frontend tool: Show notification
  useFrontendTool({
    name: "show_notification",
    description: "Display a notification to the user",
    parameters: [
      {
        name: "message",
        type: "string",
        description: "The notification message to display",
        required: true,
      },
      {
        name: "type",
        type: "string",
        description: "Type of notification: info, success, warning, or error",
        required: false,
      },
    ],
    handler: async ({ message, type }) => {
      const notificationText = `[${type || "info"}] ${message}`;
      setNotifications((prev) => [...prev, notificationText]);
      
      // Also try browser notification if permitted
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("Assistant", { body: message });
      }
      
      return { status: "shown", message: notificationText };
    },
  });

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar with notifications and device info */}
      <div
        style={{
          width: "300px",
          borderRight: "1px solid #333",
          padding: "1rem",
          overflow: "auto",
          background: "#111",
        }}
      >
        <h2 style={{ marginBottom: "1rem" }}>📊 Dashboard</h2>
        
        <div style={{ marginBottom: "2rem" }}>
          <h3 style={{ fontSize: "0.875rem", marginBottom: "0.5rem", color: "#888" }}>
            🔔 Notifications
          </h3>
          {notifications.length === 0 ? (
            <p style={{ fontSize: "0.75rem", color: "#666" }}>No notifications yet</p>
          ) : (
            <ul style={{ fontSize: "0.75rem", listStyle: "none" }}>
              {notifications.map((notif, idx) => (
                <li
                  key={idx}
                  style={{
                    padding: "0.5rem",
                    marginBottom: "0.5rem",
                    background: "#222",
                    borderRadius: "4px",
                  }}
                >
                  {notif}
                </li>
              ))}
            </ul>
          )}
        </div>

        {Object.keys(deviceInfo).length > 0 && (
          <div>
            <h3 style={{ fontSize: "0.875rem", marginBottom: "0.5rem", color: "#888" }}>
              💻 Device Info
            </h3>
            <div style={{ fontSize: "0.75rem", color: "#aaa" }}>
              <div style={{ marginBottom: "0.25rem" }}>
                <strong>Platform:</strong> {deviceInfo.platform}
              </div>
              <div style={{ marginBottom: "0.25rem" }}>
                <strong>Screen:</strong> {deviceInfo.screenWidth}x{deviceInfo.screenHeight}
              </div>
              <div style={{ marginBottom: "0.25rem" }}>
                <strong>Language:</strong> {deviceInfo.language}
              </div>
              <div style={{ marginBottom: "0.25rem" }}>
                <strong>Online:</strong> {deviceInfo.online ? "✅" : "❌"}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main chat area */}
      <div style={{ flex: 1, position: "relative" }}>
        <CopilotKit
          runtimeUrl="http://127.0.0.1:8888"
          agui
        >
          <CopilotChat
            instructions="You are a helpful assistant with access to several tools including weather, restaurants, calculations, time, and frontend tools like location and notifications. Use them when appropriate."
            labels={{
              title: "🤖 AG-UI Assistant",
              initial: "Hi! 👋 I'm your AG-UI assistant. I can help you with weather, restaurants, calculations, and more. What would you like to know?",
            }}
          />
        </CopilotKit>
      </div>
    </div>
  );
}
