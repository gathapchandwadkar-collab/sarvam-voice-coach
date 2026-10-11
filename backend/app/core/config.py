import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "VoiceCoach Indic"
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    
    # Sarvam AI Credentials
    SARVAM_API_KEY: str = ""
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"

    # Data paths
    DATA_DIR: Path = BASE_DIR / "data"
    VOICE_PROFILES_DIR: Path = BASE_DIR / "data" / "voice_profiles"
    AUDIO_CACHE_DIR: Path = BASE_DIR / "data" / "audio_cache"
    VOCABULARY_DIR: Path = BASE_DIR / "data" / "vocabulary"

    # Supported Indian Languages
    SUPPORTED_LANGUAGES: dict = {
        "hi-IN": "Hindi",
        "ta-IN": "Tamil",
        "te-IN": "Telugu",
        "kn-IN": "Kannada",
        "bn-IN": "Bengali",
        "mr-IN": "Marathi",
        "gu-IN": "Gujarati",
        "ml-IN": "Malayalam",
        "pa-IN": "Punjabi",
        "or-IN": "Odia",
    }

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.VOICE_PROFILES_DIR.mkdir(parents=True, exist_ok=True)
settings.AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
settings.VOCABULARY_DIR.mkdir(parents=True, exist_ok=True)
