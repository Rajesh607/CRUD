from fastapi import APIRouter

from app.api.routes import analysis, auth, data

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(data.router)
api_router.include_router(analysis.router)
