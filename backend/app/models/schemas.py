from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class VoiceProfileCreateResponse(BaseModel):
    profile_id: str
    user_name: str
    duration_seconds: float
    sample_rate: int
    quality_score: float
    created_at: str
    message: str

class VoiceProfileInfo(BaseModel):
    profile_id: str
    user_name: str
    created_at: str
    sample_audio_url: str

class PronounceRequest(BaseModel):
    profile_id: str
    text: str = Field(..., description="The word, phrase, or sentence to pronounce")
    language_code: str = Field(..., description="BCP 47 language code, e.g. hi-IN, ta-IN")
    speed: Optional[float] = Field(1.0, description="Speech rate, between 0.7 and 1.3")
    pitch: Optional[float] = Field(0.0, description="Pitch modification offset")

class PronounceResponse(BaseModel):
    audio_url: str
    phonetic_breakdown: List[str]
    transliteration: str
    native_script: str
    duration_seconds: float

class AssessmentRequest(BaseModel):
    profile_id: str
    phrase_id: Optional[str] = None
    target_text: str
    language_code: str

class PhonemeScore(BaseModel):
    phoneme: str
    score: float
    feedback: Optional[str] = None

class AssessmentResponse(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    fluency_score: float = Field(..., ge=0.0, le=100.0)
    accuracy_score: float = Field(..., ge=0.0, le=100.0)
    phoneme_scores: List[PhonemeScore]
    actionable_tip: str

class VocabularyItem(BaseModel):
    id: str
    category: str
    native_text: str
    transliteration: str
    english_meaning: str
    difficulty: str  # beginner, intermediate, advanced
    audio_reference_url: Optional[str] = None
