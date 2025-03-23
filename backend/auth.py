import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "")

async def require_api_key(x_api_key: str = Header(default="")):
    if not API_KEY:
        return  # open if not configured
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")
