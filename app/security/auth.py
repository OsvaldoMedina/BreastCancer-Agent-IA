# app/security/auth.py
from fastapi import Header, HTTPException
from app.config import settings

async def require_api_key(x_api_key: str | None = Header(default=None)):
    expected = getattr(settings, "API_KEY", None)
    if expected and x_api_key == expected:
        return True
    raise HTTPException(status_code=401, detail="API key inválida")
