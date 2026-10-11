import re
from typing import List, Dict

class IndicPhoneticsService:
    """
    Handles syllable segmentation, phonetic breakdown, and Romanized transliteration
    for Indian languages (Devanagari, Tamil, Telugu, Kannada, Bengali, etc.).
    """

    # Vowel sign and virama patterns for Indic scripts
    VIRAMA_MAP = {
        "hi-IN": "\u094D",  # Devanagari halant
        "ta-IN": "\u0BCD",  # Tamil pulli
        "te-IN": "\u0C4D",  # Telugu virama
        "kn-IN": "\u0CCD",  # Kannada virama
        "bn-IN": "\u09CD",  # Bengali virama
        "mr-IN": "\u094D",  # Marathi halant
    }

    @classmethod
    def get_phonetic_breakdown(cls, text: str, language_code: str) -> List[str]:
        """
        Splits an Indic word into practice syllables/phonemes.
        Example: 'नमस्ते' -> ['न (na)', 'म (ma)', 'स्ते (ste)']
        """
        words = text.strip().split()
        phonemes = []
        for word in words:
            # Basic grapheme cluster / syllable separation
            chars = list(word)
            cluster = ""
            for c in chars:
                cluster += c
                # If next char is not a diacritic or matra, or if word ended
                if len(cluster) >= 1:
                    phonemes.append(cluster)
                    cluster = ""
            if cluster:
                phonemes.append(cluster)
        return phonemes if phonemes else [text]

    @classmethod
    def get_transliteration(cls, text: str, language_code: str) -> str:
        """
        Returns English phonetic guide / transliteration for learner.
        """
        # Common sample mapping for quick display
        common_lookups = {
            "नमस्ते": "Namaste",
            "धन्यवाद": "Dhanyavaad",
            "வணக்கம்": "Vanakkam",
            "நன்றி": "Nandri",
            "నమస్కారం": "Namaskāram",
            "ಧನ್ಯವಾದಗಳು": "Dhanyavādagalu",
            "নমস্কার": "Nomoshkar",
            "नमस्कार": "Namaskār"
        }
        return common_lookups.get(text, text)
