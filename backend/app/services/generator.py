import asyncio
from io import BytesIO
from typing import Optional
import logging

from google import genai
from fastapi import Depends

from app.core.config import settings
from app.models.generation import ImageGeneration
from app.storage_providers.base import BaseStorageProvider
from app.storage_providers.minio import MinioStorageProvider 
from app.utils.id_generator import generate_unique_id

logger = logging.getLogger(__name__)

class GeneratorService:
    """
    Service responsible for the core logic of generating and storing images.
    """ 
    def __init__(self, storage_provider: BaseStorageProvider):
        self.storage_provider = storage_provider
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.0-flash-preview-image-generation"

    async def _generate_image_from_prompt(self, prompt: str) -> Optional[BytesIO]:
        """
        Calls the Gemini API to generate an image using Gemini 2.0 Flash.
        """
        try:
            def generate():
                from google.genai import types
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )
            
            # Run the blocking function in separate thread
            result = await asyncio.to_thread(generate)
            
            # Process the response - Gemini 2.0 returns content parts
            if result.candidates and len(result.candidates) > 0:
                for part in result.candidates[0].content.parts:
                    if part.inline_data is not None:
                        # Found image data - convert to BytesIO
                        buffer = BytesIO(part.inline_data.data)
                        buffer.seek(0)
                        return buffer
            return None 
        except Exception as e:
            logger.exception("Failed to generate image from Gemini", extra={"prompt": prompt})
            return None
    async def generate_and_store_image(self, prompt: str) -> Optional[ImageGeneration]:
        """
        Orchestrates the full image generation and storage workflow.
        
        Args:
            prompt: The user's text prompt for image generation
            
        Returns:
            ImageGeneration object with metadata, or None if failed
        """
        generation_id = generate_unique_id(prefix="gen")
        object_name = f"{generation_id}.png"

        # Create initial generation record
        generation_result = ImageGeneration(
            generation_id=generation_id,
            prompt=prompt,
        )
        
        # Step 1: Mark as processing and generate the image
        generation_result.mark_as_processing()
        image_buffer = await self._generate_image_from_prompt(prompt)
        if not image_buffer:
            generation_result.mark_as_failed("Failed to generate image from AI model")
            logger.warning("Image generation failed", extra={"generation_id": generation_id})
            return generation_result
            
        # Step 2: Upload the generated image to storage
        try:
            def upload():
                return self.storage_provider.upload(
                    file_object=image_buffer,
                    bucket=settings.OBJECT_STORAGE_BUCKET,
                    object_name=object_name,
                    content_type="image/png"
                )
            public_url = await asyncio.to_thread(upload)
            generation_result.mark_as_completed(public_url)
        except Exception as e:
            generation_result.mark_as_failed(f"Storage upload failed: {str(e)}")
            logger.exception(
                "Failed to upload generated image", 
                extra={"generation_id": generation_id, "object_name": object_name}
            )
        finally:
            image_buffer.close()

        logger.info(
            "Successfully generated and stored image", 
            extra={"generation_id": generation_id, "prompt_length": len(prompt)}
        )
        return generation_result
