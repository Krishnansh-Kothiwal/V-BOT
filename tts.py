"""
tts.py — Text-to-Speech using pyttsx3 (Windows SAPI, fully offline, no temp dir issues)
"""

import os
import pyttsx3
from pathlib import Path

# Save audio inside the project — avoids Windows AppData\Temp permission errors
_TMP_DIR = Path(__file__).parent / "tmp"
_TMP_DIR.mkdir(exist_ok=True)
_OUTPUT_FILE = str(_TMP_DIR / "response.wav")


def synthesize(text: str) -> bytes:
    """
    Convert text to speech using pyttsx3 (Windows SAPI voices).
    Saves to a local WAV file, returns raw bytes for Streamlit playback.
    """
    engine = pyttsx3.init()

    # Tweak voice properties
    engine.setProperty("rate", 175)    # Words per minute (default ~200)
    engine.setProperty("volume", 1.0)  # Max volume

    # Save to a WAV file we control
    engine.save_to_file(text, _OUTPUT_FILE)
    engine.runAndWait()
    engine.stop()

    # Read and return raw bytes
    with open(_OUTPUT_FILE, "rb") as f:
        return f.read()
