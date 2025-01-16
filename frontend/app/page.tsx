"use client";

import { useState } from "react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat, CopilotKitCSSProperties } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { ReviewTool } from "./ReviewTool";

export default function Home() {
  const [isReviewMode, setIsReviewMode] = useState(false);
  const [reviewContent, setReviewContent] = useState<string[]>([]);

  // Handler to process agent responses
  const handleAgentResponse = (response: string) => {
    const bullets = response
      .split("\n")
      .filter((line) => line.trim().startsWith("-"));
    setReviewContent(bullets);
    setIsReviewMode(true);
  };

  return (
    <main
      className="h-screen w-full p-10"
      style={{
        "--copilot-kit-primary-color": "#0078D7",
        "--copilot-kit-contrast-color": "#FFFFFF",
        "--copilot-kit-secondary-color": "#F3F4F6",
        "--copilot-kit-secondary-contrast-color": "#333333",
        "--copilot-kit-background-color": "#F9FAFB",
        "--copilot-kit-muted-color": "#6B7280",
        "--copilot-kit-separator-color": "#E5E7EB",
        "--copilot-kit-scrollbar-color": "#D1D5DB",
        "--copilot-kit-response-button-color": "#2563EB",
        "--copilot-kit-response-button-background-color": "#EFF6FF",
      } as CopilotKitCSSProperties}
    >
      <CopilotKit runtimeUrl="/api/copilotkit" agent="Plan_Sarthi">
        <div className="text-center mb-4">
          <h1 className="text-2xl font-bold">Plan Sarthi</h1>
          <button
            className="bg-blue-500 text-white px-4 py-2 mt-2 rounded"
            onClick={() => setIsReviewMode((prev) => !prev)}
          >
            {isReviewMode ? "Exit Review Mode" : "Enter Review Mode"}
          </button>
        </div>

        <div className="flex flex-col md:flex-row gap-6">
          {/* Chat Interface */}
          <div className="flex-1 border border-gray-300 rounded-lg p-4">
            <CopilotChat
              className="h-full w-full"
              labels={{
                title: "Plan Sarthi",
                initial: "Hi! 👋 How can I assist you today?",
              }}
              onInProgress={(inProgress) =>
                !inProgress &&
                handleAgentResponse("- Travel destination\n- Mock Exam Prep")
              }
            />
          </div>

          {/* Conditional Rendering of ReviewTool */}
          {isReviewMode && (
            <div className="flex-1 border border-gray-300 rounded-lg p-4">
              <ReviewTool bullets={reviewContent} onQueryClick={(query) => console.log(query)} />
            </div>
          )}
        </div>
      </CopilotKit>
    </main>
  );
}
