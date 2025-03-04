import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_key: str = os.getenv("OPENAI_API_KEY", "")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
