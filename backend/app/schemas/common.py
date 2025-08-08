from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

class Status(str, Enum):
    success = "success"
    error = "error"

class ErrorResponse(BaseModel):
    """Standard error envelope."""
    status: Literal["error"] = "error"
    message: str
    code: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "error",
                "message": "Prompt is required.",
                "code": "PROMPT_REQUIRED",
            }
        }
    )

