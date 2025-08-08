from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class ImageGeneration(BaseModel):
    """
        Represent the internal State of of an image generation task.
    """
    generation_id: str
    prompt: str
    image_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True 


