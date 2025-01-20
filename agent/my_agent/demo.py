import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import logging
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from my_agent.agent import graph

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://plan-sarthi.vercel.app").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SDK
sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="Plan_Sarthi",
            description="A sample chatbot",
            graph=graph,
        )
    ],
)

# Add SDK endpoint
add_fastapi_endpoint(app, sdk, "/copilotkit")

# Favicon handler
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("my_agent/favicon.ico")  # Update path as needed

# Root endpoint for health check
@app.get("/")
async def plan():
    return {"message": "Hello World"}

# Custom exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred", "detail": str(exc)},
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")

# Main entry point
def main():
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
