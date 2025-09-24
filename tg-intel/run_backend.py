#!/usr/bin/env python3
"""
Simple script to run the backend server with proper path setup
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Set environment variables
os.environ['PYTHONPATH'] = str(current_dir)

if __name__ == "__main__":
    import uvicorn
    from apps.backend.app import app
    
    print(f"Starting server from: {current_dir}")
    print(f"Python path: {sys.path[:3]}")
    
    uvicorn.run(
        "apps.backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
