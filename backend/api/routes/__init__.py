"""API routes package."""

try:
    from backend.api.routes.hash_routes import router as hash_router
    from backend.api.routes.experiment_routes import router as experiment_router
    from backend.api.routes.avalanche_routes import router as avalanche_router
    from backend.api.routes.file_routes import router as file_router
    from backend.api.routes.health_routes import router as health_router
except ImportError:
    from api.routes.hash_routes import router as hash_router
    from api.routes.experiment_routes import router as experiment_router
    from api.routes.avalanche_routes import router as avalanche_router
    from api.routes.file_routes import router as file_router
    from api.routes.health_routes import router as health_router

__all__ = [
    "hash_router",
    "experiment_router",
    "avalanche_router",
    "file_router",
    "health_router",
]

