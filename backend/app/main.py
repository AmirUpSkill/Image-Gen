from fastapi import FastAPI
from app.core.lifecycle import register_lifecycle
from app.api.health import router as health_router

app = FastAPI()
register_lifecycle(app)
app.include_router(health_router, prefix="/api/v1")
