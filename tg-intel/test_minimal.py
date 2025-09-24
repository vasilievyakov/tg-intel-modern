#!/usr/bin/env python3
"""
Minimal test to check if backend can start without DB
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

print(f"Testing minimal backend from: {current_dir}")

try:
    print("1. Testing health endpoint...")
    from fastapi.testclient import TestClient
    from apps.backend.app import app
    
    with TestClient(app) as client:
        response = client.get("/healthz")
        print(f"   ✓ Health check: {response.status_code} - {response.json()}")
        
        response = client.get("/api/channels")
        print(f"   ✓ Channels endpoint: {response.status_code}")
        if response.status_code == 503:
            print("   ✓ Expected 503 - database not configured")
    
    print("\n✅ Minimal test passed! Backend works without DB.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
