from fastapi import APIRouter, HTTPException
from app.models.schemas import PronounceRequest, PronounceResponse
from app.services.voice_clone.synthesizer import VoiceCloneSynthesizer
from app.services.indic_nlp.phonetics import IndicPhoneticsService

router = APIRouter()
synthesizer = VoiceCloneSynthesizer()


@router.post("/speak", response_model=PronounceResponse)
async def generate_pronunciation_in_own_voice(request: PronounceRequest):
    """
    Core feature: synthesize the target phrase in the learner's enrolled voice profile
    using Microsoft Edge Neural TTS (free, no API credits needed).
    Returns the audio URL + phonetic breakdown for display.
    """
    try:
        audio_url = await synthesizer.synthesize_in_learner_voice(
            profile_id=request.profile_id,
            text=request.text,
            language_code=request.language_code,
            speed=request.speed or 1.0,
            pitch=request.pitch or 0.0,
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Voice profile not found. Please record your voice first.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {exc}")

    phonemes = IndicPhoneticsService.get_phonetic_breakdown(
        request.text, request.language_code
    )
    transliteration = IndicPhoneticsService.get_transliteration(
        request.text, request.language_code
    )

    return PronounceResponse(
        audio_url=audio_url,
        phonetic_breakdown=phonemes,
        transliteration=transliteration,
        native_script=request.text,
        duration_seconds=1.8,
    )


@router.get("/demo/{language_code}")
async def get_demo_pronunciation(language_code: str, text: str = "नमस्ते"):
    """
    Quick demo endpoint — synthesizes text without needing an enrolled profile.
    Creates a temporary demo profile automatically.
    """
    import json, uuid, datetime
    from app.core.config import settings
    from app.services.tts.edge_tts_engine import synthesize_to_file

    demo_id = f"demo_{language_code.replace('-', '_')}"
    profile_path = settings.VOICE_PROFILES_DIR / f"{demo_id}.json"

    if not profile_path.exists():
        profile = {
            "profile_id": demo_id,
            "user_name": "Demo User",
            "gender": "female",
            "duration_seconds": 5.0,
            "sample_rate": 16000,
            "quality_score": 90.0,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "tts_provider": "edge_tts",
        }
        profile_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")

    try:
        audio_url = await synthesizer.synthesize_in_learner_voice(
            profile_id=demo_id,
            text=text,
            language_code=language_code,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "audio_url": audio_url,
        "text": text,
        "language_code": language_code,
        "tts_provider": "edge_tts (free)",
    }
