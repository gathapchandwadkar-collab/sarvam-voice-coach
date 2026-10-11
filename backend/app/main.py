from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Clone a learner's voice and generate correct pronunciation of new vocabulary or phrases in their own voice across Indian languages.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
from pathlib import Path

# Mount audio cache for streaming audio
app.mount("/audio", StaticFiles(directory=str(settings.AUDIO_CACHE_DIR)), name="audio")

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

FRONTEND_INDEX = settings.DATA_DIR.parent / "frontend" / "index.html"

@app.get("/")
def serve_index():
    return FileResponse(str(FRONTEND_INDEX))

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "languages_supported": len(settings.SUPPORTED_LANGUAGES)
    }
