#!/usr/bin/env python3
"""
Правильный запуск backend сервера
"""
import sys
import os
import asyncio
from pathlib import Path

# Fix Windows Event Loop for psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Устанавливаем правильный Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
os.environ['PYTHONPATH'] = str(current_dir)

# Force UTF-8 for stdio to avoid Windows cp1252 issues
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

print(f"Starting backend from: {current_dir}")
print(f"Python path: {sys.path[0]}")

try:
    import uvicorn
    from apps.backend.app import app
    
    print("All modules imported successfully")
    print("Starting server at http://0.0.0.0:8000")
    print("Health check: http://localhost:8000/healthz")
    print("API docs: http://localhost:8000/docs")
    print("=" * 50)
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    
except Exception as e:
    print(f"Startup error: {e}")
    import traceback
    traceback.print_exc()
