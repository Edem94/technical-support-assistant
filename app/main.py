from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from uvicorn import logging

# logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    app.state.startup_error = None
    print("Starting up the application...")
    yield
    print("Shutting down the application...")

app = FastAPI(title="Technical Support Assistant", lifespan=lifespan)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "message": "The application is running smoothly.", 
            "environment": "development"}


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/", tags=["Root"])
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/ask", tags=["Ask"])
async def ask_question(question: str):
    # Here you would implement the logic to handle the question,
    # possibly using the Anthropic API or any other service.
    # For now, we'll just return a placeholder response.
    return {"question": question, "answer": "This is a placeholder answer."}