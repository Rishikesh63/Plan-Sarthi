"use client";

import { useCopilotAction } from "@copilotkit/react-core";

export function ReviewTool() {
  useCopilotAction({
    name: "ReviewResponse",
    available: "remote",
    parameters: [
      {
        name: "ai_response",
        type: "string",
        description: "The AI-generated response to review",
        required: true,
      },
    ],
    renderAndWaitForResponse: ({ args, status, respond }) => {
      console.log("Args:", args);
      console.log("Status:", status);
      console.log("Respond Function:", respond);

      return (
        <div className="p-4 bg-white text-black rounded shadow-lg">
          <h1 className="text-xl font-bold mb-4">AI Response Review</h1>
          <p className="mb-4">{args?.ai_response || "Mock AI response for testing."}</p>
          <div className="flex gap-4">
            <button
              className="bg-green-500 text-white px-4 py-2 rounded"
              onClick={() =>
                respond?.({
                  decision: "APPROVE",
                  reason: "User approved the response",
                })
              }
            >
              Approve
            </button>
            <button
              className="bg-red-500 text-white px-4 py-2 rounded"
              onClick={() =>
                respond?.({
                  decision: "REJECT",
                  reason: "User rejected the response",
                })
              }
            >
              Reject
            </button>
          </div>
        </div>
      );
    },
  });

  // Fallback UI in case CopilotAction fails
  return (
    <div className="text-center p-4 bg-white text-black rounded shadow-lg">
      <h1 className="text-xl font-bold">AI Response Approval</h1>
    </div>
  );
}
