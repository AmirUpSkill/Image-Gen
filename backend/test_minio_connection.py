#!/usr/bin/env python3
"""
Quick test script to verify MinIO connection and our storage provider.
Run this after starting docker-compose to ensure everything is working.
"""

import sys
import os
from io import BytesIO

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.core.config import settings
    from app.storage_providers.minio import MinioStorageProvider
    print("✅ Successfully imported modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed all requirements and set PYTHONPATH")
    sys.exit(1)

def test_minio_connection():
    """Test basic MinIO connection and bucket operations."""
    print("\n🧪 Testing MinIO Connection...")
    print(f"Endpoint: {settings.OBJECT_STORAGE_ENDPOINT}")
    print(f"Bucket: {settings.OBJECT_STORAGE_BUCKET}")
    print(f"Use HTTPS: {settings.USE_HTTPS}")
    
    try:
        # Initialize storage provider
        storage = MinioStorageProvider()
        print("✅ MinIO client initialized successfully")
        
        # Test upload with a dummy file
        test_content = b"Hello MinIO! This is a test file for AI Image Generator."
        test_file = BytesIO(test_content)
        test_key = "test/connection_test.txt"
        
        print("\n📤 Testing file upload...")
        url = storage.upload(
            file_object=test_file, 
            bucket=settings.OBJECT_STORAGE_BUCKET,
            object_name=test_key,
            content_type="text/plain"
        )
        print(f"✅ Upload successful! URL: {url}")
        
        # Test file existence
        print("\n🔍 Testing file existence...")
        exists = storage.exists(settings.OBJECT_STORAGE_BUCKET, test_key)
        print(f"✅ File exists: {exists}")
        
        # Test public URL generation
        print("\n🔗 Testing URL generation...")
        public_url = storage.get_public_url(settings.OBJECT_STORAGE_BUCKET, test_key)
        print(f"✅ Public URL: {public_url}")
        
        # Clean up test file
        print("\n🗑️ Cleaning up test file...")
        storage.delete(settings.OBJECT_STORAGE_BUCKET, test_key)
        print("✅ Test file deleted")
        
        print("\n🎉 All tests passed! MinIO is ready for your AI Image Generator.")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure docker-compose is running: docker-compose up -d")
        print("2. Check if MinIO is healthy: curl http://localhost:9000/minio/health/live")
        print("3. Verify your .env file settings match docker-compose.yml")
        print("4. Check Docker logs: docker-compose logs minio")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 AI Image Generator - MinIO Connection Test")
    print("=" * 50)
    
    # Basic config check
    try:
        print(f"Config loaded - Debug mode: {settings.DEBUG}")
        if not hasattr(settings, 'OBJECT_STORAGE_ENDPOINT'):
            raise ValueError("OBJECT_STORAGE_ENDPOINT not found in settings")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Make sure your .env file exists and contains all required variables.")
        sys.exit(1)
    
    # Run the connection test
    success = test_minio_connection()
    sys.exit(0 if success else 1)
