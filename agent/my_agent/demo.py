import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from my_agent.agent import graph

# Initialize FastAPI application
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://plan-sarthi.vercel.app"],  # Update with allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the CopilotKit SDK with agents
sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="Plan_Sarthi",
            description="A sample chatbot",
            graph=graph,  # Ensure `graph` is correctly defined in `my_agent.agent`
        )
    ],
)

# Add the CopilotKit endpoint to the FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit")

# Test endpoint to verify server functionality
@app.get("/")
async def plan():
    return {"message": "Hello World"}

# Entry point to run the server
def main():
    port = int(os.getenv("PORT", "8000"))  # Default to port 8000 if PORT is not set
    print(f"Starting server on http://0.0.0.0:{port}")  # Debug log for server start
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
