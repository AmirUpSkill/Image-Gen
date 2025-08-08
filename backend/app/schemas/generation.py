from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict

class GenerationStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class GenerationDetailResponse(BaseModel):
    """
    Schema for the response of GET /generation/{id}.
    Reflects real lifecycle: image_url may be absent until completion.
    """
    generation_id: str
    prompt: str
    status: GenerationStatus
    image_url: Optional[str] = None
    created_at: datetime
    # updated_at: Optional[datetime] = None  # Uncomment when tracked

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "generation_id": "img-1a2b3c4d",
                "prompt": "a futuristic city skyline at sunset",
                "status": "completed",
                "image_url": "https://cdn.example.com/assets/img-1a2b3c4d.png",
                "created_at": "2025-08-08T14:00:00Z"
            }
        }
    )
