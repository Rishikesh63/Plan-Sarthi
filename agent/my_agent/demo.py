import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from my_agent.agent import graph

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  
        "https://plan-sarthi.vercel.app", 
    ],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="Plan_Sarthi",
            description="A sample chatbot",
            graph=graph,  
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Middleware for logging requests and response processing times
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.perf_counter()
    
    print(f"Incoming request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(e)},
        )
    
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Processed response in {process_time:.4f} seconds")
    
    return response

def main():
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting server on http://0.0.0.0:{port}")  
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
