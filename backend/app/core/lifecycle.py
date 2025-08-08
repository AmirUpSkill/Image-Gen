from fastapi import FastAPI
from app.core.logging import setup_logging

def register_lifecycle(app: FastAPI):

    @app.on_event("startup")
    async def on_startup():
        setup_logging()
        # Initialize object store or model client here if needed
        print("🔁 App startup completed")

    @app.on_event("shutdown")
    async def on_shutdown():
        print("🛑 App shutdown complete")
