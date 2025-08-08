from abc import ABC, abstractmethod
from typing import IO, Optional


class BaseStorageProvider(ABC):
    """
    Abstract base class for storage providers.
    Defines the contract for uploading and retrieving files.
    """

    @abstractmethod
    def upload(
        self, file_object: IO[bytes], bucket: str, object_name: str, *, content_type: Optional[str] = None
    ) -> str:
        """
        Upload a file-like object and return a publicly accessible URL (or a
        presigned URL) for the uploaded object.
        """

    @abstractmethod
    def get_public_url(self, bucket: str, object_name: str, *, expires_seconds: Optional[int] = None) -> str:
        """
        Return a public or presigned URL for the object. If the bucket is
        private, implementations should return a presigned URL.
        """

    @abstractmethod
    def delete(self, bucket: str, object_name: str) -> None:
        """Delete an object from storage."""

    @abstractmethod
    def exists(self, bucket: str, object_name: str) -> bool:
        """Return True if the object exists, otherwise False."""
