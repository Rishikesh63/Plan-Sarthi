"use client";

import { useCopilotAction } from "@copilotkit/react-core";

export function ReviewTool({
  bullets,
  onQueryClick,
}: {
  bullets: string[];
  onQueryClick: (query: string) => void;
}) {
  return (
    <div className="p-4 bg-white text-black rounded shadow-lg">
      <h1 className="text-xl font-bold mb-4">Generated Queries</h1>
      <ul className="mb-4">
        {bullets.map((bullet, index) => (
          <li key={index} className="mb-2">
            <button
              className="text-blue-500 underline"
              onClick={() => onQueryClick(bullet)}
            >
              {bullet}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
