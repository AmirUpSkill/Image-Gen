from fastapi import APIRouter
from .endpoints import generate, generation, health

api_router = APIRouter()

# Include routers from the endpoint modules
api_router.include_router(generate.router, tags=["Image Generation"])
api_router.include_router(generation.router, tags=["Generation Details"])
api_router.include_router(health.router, tags=["Health"])
