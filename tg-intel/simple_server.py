#!/usr/bin/env python3
"""
Simple FastAPI server for testing
"""
import sys
import os
import asyncio
from pathlib import Path

# Fix Windows Event Loop for psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
os.environ['PYTHONPATH'] = str(current_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create simple app
app = FastAPI(title="Simple Test API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/api/channels")
async def list_channels():
    print("Received GET request for channels")
    return {"message": "Database not configured", "channels": []}

@app.post("/api/channels")
async def create_channel(data: dict):
    print(f"Received POST request with data: {data}")
    return {
        "id": 1,
        "tg_url": data.get("tg_url", ""),
        "title": "Test Channel",
        "status": "pending",
        "created_at": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting simple server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
