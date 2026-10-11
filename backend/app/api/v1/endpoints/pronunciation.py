from fastapi import APIRouter, HTTPException
from app.models.schemas import PronounceRequest, PronounceResponse
from app.services.voice_clone.synthesizer import VoiceCloneSynthesizer
from app.services.indic_nlp.phonetics import IndicPhoneticsService

router = APIRouter()
synthesizer = VoiceCloneSynthesizer()

@router.post("/speak", response_model=PronounceResponse)
async def generate_pronunciation_in_own_voice(request: PronounceRequest):
    """
    Core Feature: Generate correct pronunciation of target vocabulary/phrase
    cloned directly into the learner's own voice.
    """
    try:
        audio_url = await synthesizer.synthesize_in_learner_voice(
            profile_id=request.profile_id,
            text=request.text,
            language_code=request.language_code,
            speed=request.speed or 1.0,
            pitch=request.pitch or 0.0
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Voice profile not found. Please enroll voice first.")

    phonemes = IndicPhoneticsService.get_phonetic_breakdown(request.text, request.language_code)
    transliteration = IndicPhoneticsService.get_transliteration(request.text, request.language_code)

    return PronounceResponse(
        audio_url=audio_url,
        phonetic_breakdown=phonemes,
        transliteration=transliteration,
        native_script=request.text,
        duration_seconds=1.8
    )
