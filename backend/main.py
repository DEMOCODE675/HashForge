"""HashForge FastAPI Application Entry Point.

Exposes the cryptographic engine and experiment runners to modern web frontends.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure root directory is on Python path so core.* can be imported cleanly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.validators import ValidationError
from backend.api.routes import (
    hash_router,
    experiment_router,
    avalanche_router,
    file_router,
    health_router,
)

app = FastAPI(
    title="HashForge Cryptographic API",
    description="FIPS 180-4 (SHA-256) and FIPS 202 (SHA3-256) Avalanche Laboratory API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",  # Local development wildcard
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle core validation errors with structured 400 Bad Request."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "ValidationError"},
    )


# Mount API routers
app.include_router(health_router, prefix="/api")
app.include_router(hash_router, prefix="/api")
app.include_router(experiment_router, prefix="/api")
app.include_router(avalanche_router, prefix="/api")
app.include_router(file_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "HashForge API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

