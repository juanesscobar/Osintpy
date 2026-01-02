#!/usr/bin/env python3
"""
OSINT MVP Application
"""

import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from core.config import settings
from core.logging import setup_logging
from api.v1.api import api_router

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.SERVER_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files (dashboard)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
async def root():
    """Root endpoint with documentation"""
    return {
        "message": "OSINT API - Welcome",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "redoc": "http://localhost:8000/redoc",
        "health": "http://localhost:8000/health",
        "api_v1": f"http://localhost:8000{settings.API_V1_STR}",
        "endpoints": {
            "auth": f"http://localhost:8000{settings.API_V1_STR}/auth",
            "persons": f"http://localhost:8000{settings.API_V1_STR}/persons",
            "companies": f"http://localhost:8000{settings.API_V1_STR}/companies",
            "cyber": f"http://localhost:8000{settings.API_V1_STR}/cyber",
            "investigations": f"http://localhost:8000{settings.API_V1_STR}/investigations"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True if settings.LOG_LEVEL == "DEBUG" else False,
    )