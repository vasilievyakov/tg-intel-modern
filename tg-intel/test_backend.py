#!/usr/bin/env python3
"""
Test script to check if backend can be imported and run
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Set environment variables
os.environ['PYTHONPATH'] = str(current_dir)

print(f"Testing backend from: {current_dir}")
print(f"Python path: {sys.path[:3]}")

try:
    print("1. Testing basic import...")
    from apps.backend.app import app
    print("✅ App imported successfully!")
    
    print("2. Testing app object...")
    print(f"App type: {type(app)}")
    print(f"App title: {getattr(app, 'title', 'No title')}")
    
    print("3. Testing health endpoint...")
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/healthz")
    print(f"Health check status: {response.status_code}")
    print(f"Health check response: {response.json()}")
    
    print("✅ Backend is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
