from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class GenerationStatus(str, Enum):
    """Status of an image generation task."""
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class ImageGeneration(BaseModel):
    """
    Represents the internal state of an image generation task.
    """
    generation_id: str
    prompt: str
    status: GenerationStatus = GenerationStatus.PENDING
    image_url: Optional[str] = None  # Only populated when completed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    failure_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    def mark_as_processing(self):
        """Mark the generation as in progress."""
        self.status = GenerationStatus.PROCESSING
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_completed(self, image_url: str):
        """Mark the generation as completed with the final image URL."""
        self.status = GenerationStatus.COMPLETED
        self.image_url = image_url
        self.updated_at = datetime.now(timezone.utc)

    def mark_as_failed(self, reason: str):
        """Mark the generation as failed with a reason."""
        self.status = GenerationStatus.FAILED
        self.failure_reason = reason
        self.updated_at = datetime.now(timezone.utc)


