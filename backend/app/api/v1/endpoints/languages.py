import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.core.config import settings
from app.models.schemas import VocabularyItem

router = APIRouter()

@router.get("/supported")
async def get_supported_languages() -> Dict[str, str]:
    """Returns the list of supported Indian languages with their BCP 47 codes."""
    return settings.SUPPORTED_LANGUAGES

@router.get("/vocabulary/{language_code}", response_model=List[VocabularyItem])
async def get_vocabulary(language_code: str):
    """
    Returns curated practice vocabulary & everyday phrases for the selected Indian language.
    """
    # e.g., hi-IN -> hindi.json, ta-IN -> tamil.json
    lang_prefix = language_code.split("-")[0]
    lang_map = {
        "hi": "hindi.json",
        "ta": "tamil.json",
        "te": "telugu.json",
        "kn": "kannada.json",
        "mr": "marathi.json",
        "bn": "bengali.json",
    }
    filename = lang_map.get(lang_prefix, f"{lang_prefix}.json")
    vocab_file = settings.VOCABULARY_DIR / filename

    if not vocab_file.exists():
        # Fallback to empty list or default
        return []

    with open(vocab_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
