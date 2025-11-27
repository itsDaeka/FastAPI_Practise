# routers/health_router.py

from fastapi import APIRouter, Depends
from config.settings import get_settings, Settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get(
    "/ping",
    summary="Health check: Service availability",
    description="""
Returns a simple **pong** response and confirms that the API service 
is running and reachable.

### Responses
- **200 OK** – service is alive
""",
)
def ping():
    return {"message": "pong"}


@router.get(
    "/info",
    summary="Get application environment information",
    description="""
Returns metadata about the application environment, including:

- Application name  
- Version  
- Active environment (development/deployment)  
- Debug mode status  
- Database URL  

This endpoint is **safe for non-sensitive environments** but should be secured 
in production environments where configuration details must not be exposed.

### Responses
- **200 OK** – environment configuration details  
""",
)
def info(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug_mode,
        "database": settings.database_url,
    }
