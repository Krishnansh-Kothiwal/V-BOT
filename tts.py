"""
tts.py — Text-to-Speech using gTTS (cloud-compatible, cross-platform)
"""

import io
from gtts import gTTS


def synthesize(text: str) -> bytes:
    """
    Convert text to speech using gTTS.
    Returns raw MP3 bytes for Streamlit playback.
    No temp files — uses in-memory BytesIO buffer.
    """
    tts = gTTS(text=text, lang="en", slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()
