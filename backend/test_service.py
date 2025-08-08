#!/usr/bin/env python3
"""
Test script to verify the service layer functionality.
Run this to test Gemini API and MinIO storage integration.
"""
import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.config import settings
from app.services.generator import GeneratorService
from app.storage_providers.minio import MinioStorageProvider

async def test_service():
    """Test the full image generation and storage workflow."""
    print("🧪 Starting Service Layer Test...")
    print(f"📋 Configuration:")
    print(f"   - Gemini API Key: {'*' * 20}{settings.GEMINI_API_KEY[-10:]}")
    print(f"   - Storage Endpoint: {settings.OBJECT_STORAGE_ENDPOINT}")
    print(f"   - Storage Bucket: {settings.OBJECT_STORAGE_BUCKET}")
    print(f"   - Debug Mode: {settings.DEBUG}")
    print()

    try:
        # 1. Initialize storage provider
        print("🗄️  Initializing MinIO storage provider...")
        storage_provider = MinioStorageProvider()
        print("✅ Storage provider initialized successfully")
        
        # 2. Initialize generator service
        print("🤖 Initializing generator service...")
        generator = GeneratorService(storage_provider)
        print("✅ Generator service initialized successfully")
        
        # 3. Test image generation
        test_prompt = "a futuristic city skyline at sunset with flying cars"
        print(f"🎨 Generating image from prompt: '{test_prompt}'")
        
        result = await generator.generate_and_store_image(test_prompt)
        
        if result:
            print("✅ Image generation successful!")
            print(f"   - Generation ID: {result.generation_id}")
            print(f"   - Status: {result.status}")
            print(f"   - Image URL: {result.image_url}")
            print(f"   - Created: {result.created_at}")
            if result.failure_reason:
                print(f"   - Failure Reason: {result.failure_reason}")
        else:
            print("❌ Image generation failed - no result returned")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_service())
