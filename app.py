"""
app.py — Offline Voice Assistant (Streamlit UI)

Pipeline: Upload Audio → Whisper STT → Gemini API LLM → gTTS TTS → Play Audio
"""

import os
import html
import tempfile
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from stt import transcribe
from llm import generate_response
from tts import synthesize

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Offline Voice Assistant",
    page_icon="🎙️",
    layout="centered",
)

# ─── Custom Styling ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #B8E3E9; /* Light teal for main text */
    }

    .stApp {
        background: #0B2E33; /* Dark Teal Background */
    }

    /* Header Section */
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #B8E3E9;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .hero-sub {
        text-align: center;
        color: #93B1B5; /* Muted teal-gray */
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 2.5rem;
    }

    /* Step Cards */
    .step-card {
        background: #153D42; /* Slightly lighter teal */
        border: 1px solid #4F7C82;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    .step-card h4 {
        margin: 0 0 0.75rem 0;
        color: #B8E3E9;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .step-card p {
        color: #93B1B5;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 12px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 800;
        margin-left: 10px;
        background: #B8E3E9;
        color: #0B2E33;
        vertical-align: middle;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: #153D42;
        border: 1px dashed #4F7C82;
        border-radius: 12px;
        padding: 2rem;
    }

    /* Button Styling */
    .stButton>button {
        background: #4F7C82 !important;
        color: #B8E3E9 !important;
        border: 1px solid #B8E3E9 !important;
        padding: 0.6rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: #B8E3E9 !important;
        color: #0B2E33 !important;
        transform: translateY(-2px);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #93B1B5;
        font-size: 0.8rem;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #4F7C82;
    }

    /* Streamlit Status Widget */
    .stStatusWidget {
        background-color: #153D42 !important;
        border: 1px solid #4F7C82 !important;
    }
    hr { border-color: #4F7C82; }
</style>
""", unsafe_allow_html=True)

# Fetch API key directly from environment variables / .env
api_key = os.environ.get("GEMINI_API_KEY", "")

# ─── Header ────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🎙️ Voice Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Upload audio → Whisper → Gemini 3.1 Flash Lite → gTTS</p>',
    unsafe_allow_html=True,
)

# ─── Stack Info ────────────────────────────────────────────────
with st.expander("⚙️ Stack Details", expanded=False):
    cols = st.columns(4)
    stack = [
        ("🗣️ STT", "faster-whisper (base)"),
        ("🧠 LLM", "Gemini 3.1 Flash Lite"),
        ("🔊 TTS", "gTTS · Google TTS"),
        ("🖥️ UI", "Streamlit"),
    ]
    for col, (label, desc) in zip(cols, stack):
        col.markdown(f"**{label}**")
        col.caption(desc)

st.markdown("---")

# ─── File Upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "ogg", "flac", "m4a", "webm"],
    help="Supported formats: WAV, MP3, OGG, FLAC, M4A, WEBM",
)

if uploaded_file is not None:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

    if st.button("🚀 Process Audio", use_container_width=True, type="primary"):

        # Guard: require API key before processing
        if not api_key:
            st.error("⚠️ API Key missing! Please set GEMINI_API_KEY in your .env file.")
            st.stop()

        # ── Step 1: Transcription ──────────────────────────────
        tmp_path = None
        try:
            with st.status("🎧 Transcribing audio...", expanded=True) as status:
                # Save uploaded file to a temp path for faster-whisper
                suffix = Path(uploaded_file.name).suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                transcript = transcribe(tmp_path)
                status.update(label="✅ Transcription complete", state="complete")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

        safe_transcript = html.escape(transcript)
        st.markdown(f"""
        <div class="step-card">
            <h4>📝 Transcription <span class="badge badge-ok">DONE</span></h4>
            <p>{safe_transcript}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Step 2: LLM Response ───────────────────────────────
        with st.status("🧠 Generating response with Gemini 3.1 Flash Lite...", expanded=True) as status:
            answer = generate_response(transcript, api_key)
            status.update(label="✅ LLM response ready", state="complete")

        safe_answer = html.escape(answer)
        st.markdown(f"""
        <div class="step-card">
            <h4>💬 Assistant Response <span class="badge badge-ok">DONE</span></h4>
            <p>{safe_answer}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Step 3: Text-to-Speech ─────────────────────────────
        with st.status("🔊 Synthesizing speech...", expanded=True) as status:
            # Truncate very long responses to keep TTS fast
            tts_text = answer[:2000] if len(answer) > 2000 else answer
            audio_bytes = synthesize(tts_text)
            status.update(label="✅ Audio synthesized", state="complete")

        st.markdown("""
        <div class="step-card">
            <h4>🔊 Response Audio <span class="badge badge-ok">DONE</span></h4>
        </div>
        """, unsafe_allow_html=True)

        st.audio(audio_bytes, format="audio/mp3")

        # ── Pipeline Summary ───────────────────────────────────
        st.success("✅ Full pipeline complete.")

else:
    st.markdown("""
    <div class="step-card">
        <h4>👆 Upload an audio file to get started</h4>
        <p>Record a question on your phone or computer, then upload the file here.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Powered by faster-whisper · Gemini 3.1 Flash Lite · gTTS · Streamlit
</div>
""", unsafe_allow_html=True)
