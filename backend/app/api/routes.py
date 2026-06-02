from fastapi import APIRouter

from app.api.v1 import baselines, benchmarks, directories, health, logs, settings, verifications

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(directories.router)
api_router.include_router(baselines.router)
api_router.include_router(verifications.router)
api_router.include_router(benchmarks.router)
api_router.include_router(logs.router)
api_router.include_router(settings.router)
