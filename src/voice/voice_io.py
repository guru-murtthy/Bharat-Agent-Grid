"""Voice-first I/O for 20+ Indian languages (Challenge 3).

Hackathon scope provides stubs with a clean interface so real providers
(Bhashini for Indian languages, Whisper for STT) can be dropped in later.
"""
from __future__ import annotations

SUPPORTED_LANGUAGES = {
    "hi": "Hindi",
    "kn": "Kannada",
    "en": "English",
    # extend toward 22 scheduled languages via Bhashini
}


def detect_language(text: str) -> str:
    """Naive language hint for the demo. Replace with a real detector."""
    devanagari = any("\u0900" <= ch <= "\u097f" for ch in text)
    kannada = any("\u0c80" <= ch <= "\u0cff" for ch in text)
    if kannada:
        return "kn"
    if devanagari:
        return "hi"
    return "en"


def speech_to_text(audio_or_text: str, language: str | None = None) -> str:
    """Stub: in the demo we pass text directly. Swap in Whisper/Bhashini STT."""
    return audio_or_text


def text_to_speech(text: str, language: str = "en") -> str:
    """Stub: returns the text that would be spoken aloud."""
    lang = SUPPORTED_LANGUAGES.get(language, language)
    return f"[speak:{lang}] {text}"
