"""
stt.py — Speech-to-Text using faster-whisper (runs fully offline on CPU)
"""

import streamlit as st
from faster_whisper import WhisperModel


@st.cache_resource(show_spinner="⬇️ Downloading Whisper model (first run only)...")
def _load_model():
    """Load WhisperModel once and cache it for the session."""
    return WhisperModel("base", device="cpu", compute_type="int8")


def transcribe(audio_path: str) -> str:
    """Transcribe an audio file and return the full text."""
    model = _load_model()
    segments, _ = model.transcribe(audio_path, beam_size=5)
    return " ".join(segment.text.strip() for segment in segments)
