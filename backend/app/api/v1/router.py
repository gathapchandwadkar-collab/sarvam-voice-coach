from fastapi import APIRouter
from app.api.v1.endpoints import voice_profile, pronunciation, assessment, languages

api_router = APIRouter()

api_router.include_router(voice_profile.router, prefix="/voice-profile", tags=["Voice Profile Enrollment"])
api_router.include_router(pronunciation.router, prefix="/pronunciation", tags=["Own-Voice Pronunciation Coach"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Pronunciation Assessment"])
api_router.include_router(languages.router, prefix="/languages", tags=["Indic Languages & Vocabulary"])
