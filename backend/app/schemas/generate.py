from pydantic import BaseModel, Field, ConfigDict, field_validator
from .common import Status, ErrorResponse

class GenerateRequest(BaseModel):
    """
    Schema for the request body of the /generate endpoint.
    """
    prompt: str = Field(
        ...,  # required
        min_length=10,
        max_length=500,
        description="The user's imaginative input for the image."
    )

    @field_validator("prompt")
    @classmethod
    def non_empty_after_strip(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("Prompt cannot be empty or whitespace.")
        return v2

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "a futuristic city skyline at sunset"
            }
        }
    )

class GenerateResponse(BaseModel):
    """
    Schema for the successful response of the /generate endpoint.
    """
    generation_id: str
    image_url: str
    status: Status

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "generation_id": "img-1a2b3c4d",
                "image_url": "https://cdn.example.com/assets/img-1a2b3c4d.png",
                "status": "success"
            }
        }
    )
