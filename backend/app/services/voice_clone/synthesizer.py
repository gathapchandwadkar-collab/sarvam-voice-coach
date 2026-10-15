"""
Voice Clone Synthesizer — now powered by Edge TTS (free, no API key).

Pipeline:
 1. Learner enrolls a voice sample → profile stored with acoustic metadata.
 2. When "Hear in Your Own Voice" is triggered, the target phrase is
    synthesized via Microsoft Edge Neural TTS (authentic Indic neural voices).
 3. (Future upgrade) Once voice-cloning credits/model available, the audio
    is further passed through a speaker-conversion layer so the learner
    hears their own timbre over the native pronunciation reference.
"""
import json
import logging
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.services.tts.edge_tts_engine import synthesize_to_file

logger = logging.getLogger(__name__)


class VoiceCloneSynthesizer:
    def __init__(
        self,
        profiles_dir: Optional[Path] = None,
        cache_dir: Optional[Path] = None,
    ):
        self.profiles_dir = profiles_dir or settings.VOICE_PROFILES_DIR
        self.cache_dir = cache_dir or settings.AUDIO_CACHE_DIR

    async def synthesize_in_learner_voice(
        self,
        profile_id: str,
        text: str,
        language_code: str,
        speed: float = 1.0,
        pitch: float = 0.0,
        gender: str = "female",
    ) -> str:
        """
        Generate audio pronouncing `text` in `language_code`.
        Currently uses Edge TTS neural voices (free).
        Returns a URL path that can be served by the /audio static mount.
        """
        profile_path = self.profiles_dir / f"{profile_id}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Voice profile '{profile_id}' not found.")

        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        # Build a stable cache filename
        safe_text = "".join(c for c in text[:25] if c.isalnum() or c in "_-")
        output_filename = f"synth_{profile_id}_{language_code}_{safe_text}.mp3"
        output_path = self.cache_dir / output_filename

        # Convert speed float (0.7–1.3) → Edge TTS rate string
        rate_pct = int((speed - 1.0) * 100)
        rate_str = f"{rate_pct:+d}%"   # e.g. "-15%" or "+5%"

        # Convert pitch float → Hz string
        pitch_str = f"{int(pitch):+d}Hz"

        if not output_path.exists():
            success = await synthesize_to_file(
                text=text,
                output_path=output_path,
                language_code=language_code,
                gender=profile.get("gender", gender),
                rate=rate_str,
                pitch=pitch_str,
            )
            if not success:
                # Hard fallback: write a silent 1-sec MP3 stub
                output_path.write_bytes(b"\xff\xfb\x90\x00" * 441)
                logger.warning(f"Used silent MP3 stub for {output_filename}")

        logger.info(f"Serving pronunciation: {output_filename}")
        return f"/audio/{output_filename}"
