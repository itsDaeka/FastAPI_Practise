# routers/health_router.py
from fastapi import APIRouter, Depends
from config.settings import get_settings, Settings

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/info")
def info(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug_mode,
        "database": settings.database_url
    }