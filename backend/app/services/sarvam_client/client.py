import base64
import httpx
import logging
from typing import Optional, Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class SarvamClient:
    """
    Client for interacting with Sarvam AI's Indic Speech APIs:
    - Text-to-Speech (Bulbul v3 / v4-flash)
    - Speech-to-Text (Saaras)
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SARVAM_API_KEY
        self.base_url = settings.SARVAM_BASE_URL.rstrip("/")
        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def text_to_speech(
        self,
        text: str,
        target_language_code: str,
        speaker: str = "aditya",
        model: str = "bulbul:v3"
    ) -> Dict[str, Any]:
        """
        Synthesize speech using Sarvam AI Bulbul TTS.
        Returns the parsed response dictionary containing base64 audio chunks.
        """
        endpoint = f"{self.base_url}/text-to-speech"
        payload = {
            "inputs": [text],
            "target_language_code": target_language_code,
            "speaker": speaker,
            "model": model
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, json=payload, headers=self.headers)
            
            if response.status_code == 402:
                logger.warning("Sarvam AI API returned 402: No credits available on this account.")
                return {
                    "status": "quota_exceeded",
                    "error": "No credits available on the Sarvam API key. Please recharge credits on dashboard.sarvam.ai.",
                    "audios": []
                }
            
            response.raise_for_status()
            return response.json()

    async def speech_to_text(
        self,
        audio_bytes: bytes,
        language_code: str = "hi-IN",
        model: str = "saaras:v1"
    ) -> Dict[str, Any]:
        """
        Transcribe speech using Sarvam AI Saaras ASR.
        """
        endpoint = f"{self.base_url}/speech-to-text"
        headers = {"api-subscription-key": self.api_key}

        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
            data = {
                "language_code": language_code,
                "model": model,
                "with_diarization": False
            }
            response = await client.post(endpoint, headers=headers, files=files, data=data)
            if response.status_code == 402:
                logger.warning("Sarvam AI ASR quota exceeded.")
                return {"transcript": "", "error": "Quota exceeded"}
            response.raise_for_status()
            return response.json()
