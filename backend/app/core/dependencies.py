from fastapi import Depends, Request
from app.storage_providers.base import BaseStorageProvider
from app.storage_providers.minio import MinioStorageProvider
from app.services.generator import GeneratorService

# This is a simple way to create a singleton instance of the storage provider.
# For more complex apps, you might use a more robust dependency injection framework.
minio_provider = MinioStorageProvider()
minio_provider.init() # Initialize the client and check for the bucket

generator_service = GeneratorService(storage_provider=minio_provider)

def get_generator_service() -> GeneratorService:
    """
    Dependency injector that provides a singleton instance of the GeneratorService.
    """
    return generator_service