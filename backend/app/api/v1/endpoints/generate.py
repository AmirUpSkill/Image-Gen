from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.schemas.common import ErrorResponse
from app.services.generator import GeneratorService
from app.api.v1.dependencies import get_generator_service
from app.models.generation import GenerationStatus


router = APIRouter()

@router.post(
    "/generate",
    response_model=GenerateResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Image generation failed"}
    }
)
async def generate_image(
    request: GenerateRequest,
    service: GeneratorService = Depends(get_generator_service)
):
    """
    Generate an image from a text prompt.
    
    Args:
        request: Contains the prompt for image generation
        service: Injected generator service
        
    Returns:
        GenerateResponse with generation_id, image_url, and status
        
    Raises:
        HTTPException: If image generation fails
    """
    try:
        generation_result = await service.generate_and_store_image(request.prompt)
        
        if not generation_result or generation_result.status == GenerationStatus.FAILED:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=generation_result.failure_reason if generation_result else "Image generation failed"
            )
        
        # Ensure we have a valid image URL before returning success
        if not generation_result.image_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Image generated but no URL available"
            )
        
        # Convert the internal model to the public-facing response schema
        return GenerateResponse(
            generation_id=generation_result.generation_id,
            image_url=generation_result.image_url,
            status="success"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error during image generation: {str(e)}"
        )
