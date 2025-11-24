from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from src.config import settings

router = APIRouter()


@router.get("/")
async def root():
    """Serve the main HTML page"""
    if os.path.exists("templates/index.html"):
        return FileResponse("templates/index.html", media_type="text/html")
    return {"message": "Company Report Generator API"}


@router.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }