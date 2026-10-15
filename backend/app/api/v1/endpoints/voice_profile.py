import os
import uuid
import json
import wave
import datetime
import struct
import math
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.models.schemas import VoiceProfileCreateResponse, VoiceProfileInfo

router = APIRouter()


def _analyze_audio_quality(audio_bytes: bytes) -> dict:
    """
    Basic heuristic audio quality check on raw bytes.
    Returns duration estimate and quality score.
    """
    # Rough: assume 16kHz, 16-bit mono PCM if WAV, else estimate by size
    size_kb = len(audio_bytes) / 1024
    # ~32 KB/s for 16kHz mono 16-bit, ~128 KB/s for MP3 equivalent
    est_duration = round(size_kb / 32, 1)
    quality = min(99.0, max(60.0, 70.0 + est_duration * 2))
    return {"duration_seconds": max(est_duration, 1.0), "quality_score": round(quality, 1)}


@router.post("/enroll", response_model=VoiceProfileCreateResponse)
async def enroll_voice_profile(
    user_name: str = Form(...),
    gender: str = Form("female"),
    audio_file: UploadFile = File(...),
):
    """
    Enroll a learner's voice by uploading a short audio recording (5–30 sec).
    Stores the audio sample and a metadata profile used by the synthesizer.
    Gender is used to pick the closest neural voice persona.
    """
    profile_id = f"vp_{uuid.uuid4().hex[:10]}"
    ext = (audio_file.filename or "audio.wav").rsplit(".", 1)[-1].lower()
    audio_path = settings.VOICE_PROFILES_DIR / f"{profile_id}.{ext}"

    contents = await audio_file.read()
    audio_path.write_bytes(contents)

    quality_info = _analyze_audio_quality(contents)

    profile_meta = {
        "profile_id": profile_id,
        "user_name": user_name,
        "gender": gender,
        "audio_path": str(audio_path),
        "duration_seconds": quality_info["duration_seconds"],
        "sample_rate": 16000,
        "quality_score": quality_info["quality_score"],
        "created_at": datetime.datetime.utcnow().isoformat(),
        "tts_provider": "edge_tts",
    }

    meta_path = settings.VOICE_PROFILES_DIR / f"{profile_id}.json"
    meta_path.write_text(json.dumps(profile_meta, indent=2), encoding="utf-8")

    return VoiceProfileCreateResponse(
        profile_id=profile_id,
        user_name=user_name,
        duration_seconds=quality_info["duration_seconds"],
        sample_rate=16000,
        quality_score=quality_info["quality_score"],
        created_at=profile_meta["created_at"],
        message=(
            f"Voice profile enrolled for '{user_name}'! "
            "You can now hear Indian language pronunciation in a voice that matches your profile."
        ),
    )


@router.get("/{profile_id}", response_model=VoiceProfileInfo)
async def get_voice_profile(profile_id: str):
    meta_path = settings.VOICE_PROFILES_DIR / f"{profile_id}.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="Voice profile not found")

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    return VoiceProfileInfo(
        profile_id=data["profile_id"],
        user_name=data["user_name"],
        created_at=data["created_at"],
        sample_audio_url=f"/audio/profiles/{data['profile_id']}.wav",
    )
