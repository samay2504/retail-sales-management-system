"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.models import init_db, close_db
from src.routes import transactions_router, meta_router
from src.middleware import RequestIDMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware
from src.utils import setup_logging, cache_manager
from src.utils.logging import get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting TruEstate API...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize cache
    await cache_manager.initialize()
    logger.info("Cache initialized")

    yield

    # Shutdown
    logger.info("Shutting down TruEstate API...")

    # Close cache
    await cache_manager.shutdown()
    logger.info("Cache closed")

    # Close database
    await close_db()
    logger.info("Database closed")


# Create FastAPI app
app = FastAPI(
    title="TruEstate API",
    description="Retail Sales Management System API with advanced search, filtering, and pagination",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
)

# Custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_per_minute)
app.add_middleware(RequestIDMiddleware)

# Include routers
app.include_router(transactions_router)
app.include_router(meta_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "TruEstate API",
        "version": "1.0.0",
        "docs": "/api/docs",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "index:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
