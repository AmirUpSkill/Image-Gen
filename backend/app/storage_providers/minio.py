from io import BytesIO
from typing import Optional, IO
from urllib.parse import quote
from datetime import timedelta
import logging

from minio import Minio
from minio.error import S3Error

from app.core.config import settings
from .base import BaseStorageProvider

logger = logging.getLogger(__name__)


class MinioStorageProvider(BaseStorageProvider):
    """
    Storage provider for a MinIO S3-compatible service.
    """

    def __init__(self):
        self.client = Minio(
            settings.OBJECT_STORAGE_ENDPOINT,
            access_key=settings.OBJECT_STORAGE_ACCESS_KEY,
            secret_key=settings.OBJECT_STORAGE_SECRET_KEY,
            secure=settings.USE_HTTPS,
        )
        try:
            bucket = getattr(settings, "OBJECT_STORAGE_BUCKET", None)
            if bucket:
                self._ensure_bucket_exists(bucket)
        except S3Error as e:
            logger.exception(
                "minio.ensure_bucket_failed",
                extra={"bucket": getattr(settings, "OBJECT_STORAGE_BUCKET", None)},
            )
            raise

    def _ensure_bucket_exists(self, bucket_name: str) -> None:
        """Create the bucket if it doesn't already exist."""
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload(
        self, file_object: IO[bytes], bucket: str, object_name: str, *, content_type: Optional[str] = None
    ) -> str:
        """Upload a file-like object to MinIO and return an access URL."""
        try:
            try:
                # Try efficient path for BytesIO-like objects
                size: int
                file_object.seek(0)
                size = getattr(file_object, "getbuffer", lambda: None)()
                if size is not None:  # type: ignore[truthy-bool]
                    size = size.nbytes  # type: ignore[assignment]
                    data_stream = file_object  # type: ignore[assignment]
                else:
                    raise AttributeError
            except AttributeError:
                # Fallback: read into memory to determine size
                file_object.seek(0)
                data_bytes = file_object.read()
                size = len(data_bytes)
                data_stream = BytesIO(data_bytes)

            self.client.put_object(
                bucket_name=bucket,
                object_name=object_name,
                data=data_stream,
                length=size,
                content_type=content_type or "image/png",
            )
            return self.get_public_url(bucket, object_name)
        except S3Error as e:
            logger.exception(
                "minio.upload_failed",
                extra={"bucket": bucket, "object_name": object_name},
            )
            raise

    def get_public_url(self, bucket: str, object_name: str, *, expires_seconds: Optional[int] = None) -> str:
        """
        Construct a URL for the object.
        - If expires_seconds is provided, return a presigned URL.
        - Otherwise, construct a direct URL (assumes public bucket).
        """
        if expires_seconds:
            try:
                return self.client.presigned_get_object(
                    bucket, object_name, expires=timedelta(seconds=expires_seconds)
                )
            except S3Error as e:
                logger.exception(
                    "minio.presign_failed",
                    extra={"bucket": bucket, "object_name": object_name},
                )
                raise

        protocol = "https" if settings.USE_HTTPS else "http"
        endpoint = settings.OBJECT_STORAGE_ENDPOINT.rstrip("/")
        # Ensure forward slashes and URL-encode each path segment
        safe_object = "/".join(quote(p, safe="") for p in object_name.split("/"))
        return f"{protocol}://{endpoint}/{bucket}/{safe_object}"

    def delete(self, bucket: str, object_name: str) -> None:
        try:
            self.client.remove_object(bucket, object_name)
        except S3Error as e:
            logger.exception(
                "minio.delete_failed",
                extra={"bucket": bucket, "object_name": object_name},
            )
            raise

    def exists(self, bucket: str, object_name: str) -> bool:
        try:
            self.client.stat_object(bucket, object_name)
            return True
        except S3Error:
            return False
