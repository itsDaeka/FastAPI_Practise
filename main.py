"""
Main Application Entry Point

This file:

- Creates the FastAPI app
- Configures middleware (request timing)
- Includes all routers
- Loads lifespan() for DB initialization
- Provides a clean modular structure

Routers included:
- health_router
- user_router
- spending_router
- matrix_router
- recommendation_router
"""

import time
import logging

from fastapi import FastAPI, Request

from data.db import lifespan
from routers import (
    health_router,
    user_router,
    spending_router,
    matrix_router,
    recommendation_router,
)

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(health_router)
app.include_router(user_router)
app.include_router(spending_router)
app.include_router(matrix_router)
app.include_router(recommendation_router)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
# custom logger to write logs to file
logger = logging.getLogger("app")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    # Let the request be processed by the rest of the app
    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    # Log method, path and how long it took
    logger.info(
        f"{request.method} {request.url.path} completed in {process_time:.4f}s"
    )

    # Don't touch the response (no headers/body changed)
    return response
