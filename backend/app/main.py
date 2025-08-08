from fastapi import FastAPI
from app.core.lifecycle import register_lifecycle

app = FastAPI()
register_lifecycle(app)
