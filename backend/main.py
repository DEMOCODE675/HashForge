"""HashForge FastAPI Application Entry Point.

Exposes the cryptographic engine and experiment runners to modern web frontends.
"""

import os
import sys
import types
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

# Ensure both backend directory and root directory are on Python path
CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
for p in (str(CURRENT_DIR), str(PARENT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Self-alias 'backend' in sys.modules so 'backend.api' ALWAYS resolves,
# even inside isolated Vercel serverless containers where root is backend/
if "backend" not in sys.modules:
    backend_pkg = types.ModuleType("backend")
    backend_pkg.__path__ = [str(CURRENT_DIR)]
    sys.modules["backend"] = backend_pkg

try:
    from backend.api.routes import (
        hash_router,
        experiment_router,
        avalanche_router,
        file_router,
        health_router,
    )
except ImportError:
    from api.routes import (
        hash_router,
        experiment_router,
        avalanche_router,
        file_router,
        health_router,
    )

try:
    from core.validators import ValidationError
except ImportError:
    from backend.core.validators import ValidationError

app = FastAPI(
    title="HashForge Cryptographic API",
    description="FIPS 180-4 (SHA-256) and FIPS 202 (SHA3-256) Avalanche Laboratory API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def direct_health_check():
    """Direct root health check endpoint for Vercel deployment verification."""
    return {
        "status": "healthy",
        "service": "HashForge Cryptographic Backend",
        "version": "2.0.0",
        "algorithms": ["sha256", "sha3_256"],
        "bit_indexing": "Big-Endian (Network Order)",
        "fips_compliant": True,
    }

@app.get("/docs", include_in_schema=False)
def docs_redirect():
    """Redirect /docs to /api/docs for compatibility."""
    return RedirectResponse(url="/api/docs")

# CORS Configuration for local development and cloud deployments (e.g. Vercel)
raw_origins = os.getenv("ALLOWED_ORIGINS", "")
if raw_origins:
    origins = [orig.strip() for orig in raw_origins.split(",") if orig.strip()]
    allow_all = "*" in origins
else:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    allow_all = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=False if allow_all else True,
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


# Mount API routers (both with /api prefix and without for full proxy compatibility)
app.include_router(health_router, prefix="/api")
app.include_router(hash_router, prefix="/api")
app.include_router(experiment_router, prefix="/api")
app.include_router(avalanche_router, prefix="/api")
app.include_router(file_router, prefix="/api")

app.include_router(health_router)
app.include_router(hash_router)
app.include_router(experiment_router)
app.include_router(avalanche_router)
app.include_router(file_router)


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

