"""
FastAPI dependencies for the v1 API endpoints.
"""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.services.generator import GeneratorService
from app.storage_providers.minio import MinioStorageProvider
from app.storage_providers.base import BaseStorageProvider


@lru_cache()
def get_storage_provider() -> BaseStorageProvider:
    """
    Create and cache a storage provider instance.
    Using LRU cache to ensure we get the same instance across requests.
    """
    return MinioStorageProvider()


def get_generator_service(
    storage_provider: Annotated[BaseStorageProvider, Depends(get_storage_provider)]
) -> GeneratorService:
    """
    Create a generator service with injected storage provider.
    """
    return GeneratorService(storage_provider)
