#!/usr/bin/env python3
"""
Test script to verify the FastAPI endpoints work correctly.
"""
import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app

def test_api():
    """Test the API endpoints."""
    print("🧪 Starting API Test...")
    
    client = TestClient(app)
    
    # Test 1: Health check
    print("🔍 Testing health endpoint...")
    health_response = client.get("/api/v1/health")
    print(f"   Status: {health_response.status_code}")
    print(f"   Response: {health_response.json()}")
    
    # Test 2: Generate image
    print("🎨 Testing image generation endpoint...")
    generate_data = {"prompt": "a beautiful sunset over mountains"}
    generate_response = client.post("/api/v1/generate", json=generate_data)
    print(f"   Status: {generate_response.status_code}")
    
    if generate_response.status_code == 200:
        result = generate_response.json()
        print(f"   Generation ID: {result.get('generation_id')}")
        print(f"   Image URL: {result.get('image_url')}")
        print(f"   Status: {result.get('status')}")
    else:
        print(f"   Error: {generate_response.text}")
    
    # Test 3: Get generation details (should return 501)
    print("📋 Testing generation details endpoint...")
    details_response = client.get("/api/v1/generation/test-id")
    print(f"   Status: {details_response.status_code}")
    print(f"   Response: {details_response.json()}")
    
    print("✅ API tests completed!")

if __name__ == "__main__":
    test_api()
