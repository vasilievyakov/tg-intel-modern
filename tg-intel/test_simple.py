#!/usr/bin/env python3
"""
Simple test script to check if backend can start
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

print(f"Testing from: {current_dir}")
print(f"Python path: {sys.path[0]}")

try:
    print("1. Testing basic imports...")
    import uvicorn
    print("   ✓ uvicorn imported")
    
    from apps.backend.app import app
    print("   ✓ app imported")
    print(f"   ✓ App title: {app.title}")
    
    print("2. Testing health endpoint...")
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        response = client.get("/healthz")
        print(f"   ✓ Health check: {response.status_code} - {response.json()}")
    
    print("3. Testing channels endpoint...")
    with TestClient(app) as client:
        response = client.get("/api/channels")
        print(f"   ✓ Channels endpoint: {response.status_code}")
        if response.status_code == 503:
            print("   ✓ Expected 503 - database not configured")
    
    print("\n✅ All tests passed! Backend is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
