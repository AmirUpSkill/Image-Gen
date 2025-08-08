from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str 
    OBJECT_STORAGE_ENDPOINT: str 
    OBJECT_STORAGE_BUCKET: str
    OBJECT_STORAGE_ACCESS_KEY: str 
    OBJECT_STORAGE_SECRET_KEY: str
    USE_HTTPS: bool = True
    DEBUG: bool = False

    model_config = ConfigDict(env_file=".env")
        
settings = Settings()

