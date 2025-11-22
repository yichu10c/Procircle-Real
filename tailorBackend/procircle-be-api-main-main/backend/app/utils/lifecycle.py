"""
Application Lifecycle
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from tools.observability.log import main_logger
from app.tools.resource.garbage import GarbageCollectorType, periodic_garbage_collector


async def healthcheck():
    return "healthy"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    """
    # on startup
    main_logger.info("Application is starting")
    minor_gc = periodic_garbage_collector(GarbageCollectorType.MINOR, 300)
    major_gc = periodic_garbage_collector(GarbageCollectorType.MAJOR, 1800)

    # on running
    main_logger.info("Application start complete")
    yield
    main_logger.info("Application is shutting down")

    # on shutdown
    minor_gc.abort()
    major_gc.abort()
    main_logger.info("Application shutdown complete")
