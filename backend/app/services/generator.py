import asyncio
from io import BytesIO
from typing import Optional
import logging

import google.generativeai as genai
from fastapi import Depends
from PIL import Image

from app.core.config import settings
from app.models.generation import ImageGeneration
from app.storage_providers.base import BaseStorageProvider
from app.storage_providers.minio import MinioStorageProvider 
from app.utils.id_generator import generate_unique_id

# Configure the old SDK
genai.configure(api_key=settings.GEMINI_API_KEY)

logger = logging.getLogger(__name__)

class GeneratorService:
    """
    Service responsible for the core logic of generating and storing images.
    """ 
    def __init__(self, storage_provider: BaseStorageProvider):
        self.storage_provider = storage_provider
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def _generate_image_from_prompt(self, prompt: str) -> Optional[BytesIO]:
        """
        For now, create a simple placeholder image since Gemini image generation
        requires billing. This allows the API to work for testing.
        
        TODO: Replace with actual Gemini image generation once billing is enabled.
        """
        try:
            def create_placeholder_image():
                # Create a simple placeholder image for testing
                from PIL import Image, ImageDraw, ImageFont
                import textwrap
                
                # Create a 512x512 image with a gradient background
                img = Image.new('RGB', (512, 512), color=(30, 30, 50))
                draw = ImageDraw.Draw(img)
                
                # Draw a simple gradient effect
                for i in range(512):
                    color = (30 + i//8, 30 + i//12, 50 + i//6)
                    draw.line([(0, i), (512, i)], fill=color)
                
                # Add text overlay
                try:
                    # Try to load a font, fallback to default if not available
                    font = ImageFont.load_default()
                except:
                    font = None
                
                # Wrap the prompt text
                wrapped_text = textwrap.fill(prompt, width=40)
                lines = wrapped_text.split('\n')
                
                # Calculate text position (centered)
                y_start = 256 - (len(lines) * 15) // 2
                
                for i, line in enumerate(lines[:10]):  # Limit to 10 lines
                    # Calculate text width for centering
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = (512 - text_width) // 2
                    y = y_start + i * 20
                    
                    # Draw text with shadow effect
                    draw.text((x+1, y+1), line, fill=(0, 0, 0), font=font)  # Shadow
                    draw.text((x, y), line, fill=(255, 255, 255), font=font)  # Main text
                
                # Save to BytesIO
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                return buffer
            
            # Run in thread to simulate async behavior
            buffer = await asyncio.to_thread(create_placeholder_image)
            return buffer
        except Exception as e:
            logger.exception("Failed to create placeholder image", extra={"prompt": prompt})
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
