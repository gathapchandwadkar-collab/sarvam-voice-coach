"""
Edge TTS Engine — Free, no API key required.
Uses Microsoft Edge Neural Voices which support all major Indian languages
with authentic, natural-sounding speech. Works completely offline from
any billing/credits perspective.
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional
import edge_tts

logger = logging.getLogger(__name__)

# Neural voice map for Indian languages (best voices per language)
INDIC_VOICE_MAP = {
    "hi-IN": {"female": "hi-IN-SwaraNeural",    "male": "hi-IN-MadhurNeural"},
    "ta-IN": {"female": "ta-IN-PallaviNeural",   "male": "ta-IN-ValluvarNeural"},
    "te-IN": {"female": "te-IN-ShrutiNeural",    "male": "te-IN-MohanNeural"},
    "kn-IN": {"female": "kn-IN-SapnaNeural",     "male": "kn-IN-GaganNeural"},
    "bn-IN": {"female": "bn-IN-TanishaaNeural",  "male": "bn-IN-BashkarNeural"},
    "mr-IN": {"female": "mr-IN-AarohiNeural",    "male": "mr-IN-ManoharNeural"},
    "gu-IN": {"female": "gu-IN-DhwaniNeural",    "male": "gu-IN-NiranjanNeural"},
    "ml-IN": {"female": "ml-IN-SobhanaNeural",   "male": "ml-IN-MidhunNeural"},
    "pa-IN": {"female": "pa-IN-OjasNeural",      "male": "pa-IN-GurpreetNeural"},
    "or-IN": {"female": "or-IN-SubhasiniNeural", "male": "or-IN-SukantNeural"},
    "en-IN": {"female": "en-IN-NeerjaNeural",    "male": "en-IN-PrabhatNeural"},
}

# Default fallback
DEFAULT_VOICE = "hi-IN-SwaraNeural"


def get_voice(language_code: str, gender: str = "female") -> str:
    """Return the best Edge TTS neural voice for a given language code."""
    lang_voices = INDIC_VOICE_MAP.get(language_code, INDIC_VOICE_MAP["hi-IN"])
    return lang_voices.get(gender, lang_voices["female"])


async def synthesize_to_file(
    text: str,
    output_path: Path,
    language_code: str = "hi-IN",
    gender: str = "female",
    rate: str = "-10%",   # slightly slower for learners to follow clearly
    volume: str = "+0%",
    pitch: str = "+0Hz",
) -> bool:
    """
    Synthesize `text` in `language_code` and save as audio to `output_path`.
    Returns True on success, False on failure.

    Args:
        text:          The Indic text / phrase to speak.
        output_path:   Path where the .mp3 audio file will be saved.
        language_code: BCP-47 code e.g. 'hi-IN', 'ta-IN'.
        gender:        'female' or 'male' — selects the neural persona.
        rate:          Speech rate adjustment e.g. '-10%' (slightly slower).
        volume:        Volume adjustment e.g. '+0%'.
        pitch:         Pitch adjustment e.g. '+0Hz'.
    """
    voice = get_voice(language_code, gender)
    logger.info(f"[EdgeTTS] voice={voice}  text={text[:40]!r}  -> {output_path.name}")

    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch,
        )
        await communicate.save(str(output_path))
        logger.info(f"[EdgeTTS] Saved audio ({output_path.stat().st_size} bytes)")
        return True
    except Exception as exc:
        logger.error(f"[EdgeTTS] Synthesis failed: {exc}")
        return False


async def list_indic_voices() -> list:
    """Return all available Edge TTS voices for Indian locales."""
    voices = await edge_tts.list_voices()
    return [v for v in voices if v.get("Locale", "").endswith("-IN")]
