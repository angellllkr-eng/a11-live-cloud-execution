"""
A11 API Server Entry Point
FastAPI application with health checks and basic routing.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    logger.info("🚀 A11 Platform starting up...")
    yield
    logger.info("🛑 A11 Platform shutting down...")


# Create FastAPI app
app = FastAPI(
    title="A11 Platform API",
    description="Sovereign RAG + Evidence Platform",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "a11-platform",
            "version": "0.1.0",
            "environment": settings.ENV,
        }
    )


# Ready check endpoint
@app.get("/ready", tags=["health"])
async def ready_check():
    """Readiness check endpoint. Verifies database and cache connectivity."""
    checks = {
        "api": "ready",
    }
    
    # TODO: Add database connectivity check when implemented
    # TODO: Add Redis connectivity check when implemented
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "checks": checks,
        }
    )


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "A11 Platform API",
        "version": "0.1.0",
        "description": "Sovereign RAG + Evidence Platform",
        "docs": "/docs" if settings.DEBUG else None,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
