"""
app.py — Offline Voice Assistant (Streamlit UI)

Pipeline: Upload Audio → Whisper STT → Ollama LLM → Piper TTS → Play Audio
"""

import tempfile
from pathlib import Path

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0C1821 50%, #1B2A41 100%);
    }

    /* Header */
    .hero-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #CCC9DC, #324A5F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        text-align: center;
        color: #CCC9DC;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }

    /* Pipeline step cards */
    .step-card {
        background: rgba(27, 42, 65, 0.4);
        border: 1px solid rgba(50, 74, 95, 0.5);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
    }
    .step-card h4 {
        margin: 0 0 0.4rem 0;
        color: #CCC9DC;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .step-card p, .step-card div {
        color: #ccd6f6;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .badge-ok   { background: #324A5F; color: #CCC9DC; }
    .badge-wait { background: #0C1821; color: #1B2A41; }

    /* Buttons */
    .stButton>button {
        background-color: #324A5F !important;
        color: #CCC9DC !important;
        border: 1px solid #CCC9DC !important;
    }

    /* Divider */
    hr { border-color: rgba(204, 201, 220, 0.1); }

    /* Footer */
    .footer {
        text-align: center;
        color: #324A5F;
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
    }

    /* File uploader tweaks */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03);
        border: 1px dashed rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🎙️ Offline Voice Assistant</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Upload audio → Whisper → Ollama (qwen2.5:7b) → Piper TTS</p>',
    unsafe_allow_html=True,
)

# ─── Stack Info ────────────────────────────────────────────────
with st.expander("⚙️ Stack Details", expanded=False):
    cols = st.columns(4)
    stack = [
        ("🗣️ STT", "faster-whisper (base)"),
        ("🧠 LLM", "Ollama · qwen2.5:7b"),
        ("🔊 TTS", "Piper · lessac-medium"),
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

        # ── Step 1: Transcription ──────────────────────────────
        with st.status("🎧 Transcribing audio...", expanded=True) as status:
            # Save uploaded file to a temp path for faster-whisper
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            transcript = transcribe(tmp_path)
            status.update(label="✅ Transcription complete", state="complete")

        st.markdown(f"""
        <div class="step-card">
            <h4>📝 Transcription <span class="badge badge-ok">DONE</span></h4>
            <p>{transcript}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Step 2: LLM Response ───────────────────────────────
        with st.status("🧠 Generating response with qwen2.5:7b...", expanded=True) as status:
            answer = generate_response(transcript)
            status.update(label="✅ LLM response ready", state="complete")

        st.markdown(f"""
        <div class="step-card">
            <h4>💬 Assistant Response <span class="badge badge-ok">DONE</span></h4>
            <p>{answer}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Step 3: Text-to-Speech ─────────────────────────────
        with st.status("🔊 Synthesizing speech with Piper...", expanded=True) as status:
            # Truncate very long responses to keep TTS fast
            tts_text = answer[:2000] if len(answer) > 2000 else answer
            audio_bytes = synthesize(tts_text)
            status.update(label="✅ Audio synthesized", state="complete")

        st.markdown("""
        <div class="step-card">
            <h4>🔊 Response Audio <span class="badge badge-ok">DONE</span></h4>
        </div>
        """, unsafe_allow_html=True)

        st.audio(audio_bytes, format="audio/wav")

        # ── Pipeline Summary ───────────────────────────────────
        st.success("✅ Full pipeline complete — 100% offline, 100% free.")

else:
    st.markdown("""
    <div class="step-card">
        <h4>👆 Upload an audio file to get started</h4>
        <p>Record a question on your phone or computer, then upload the file here.
        The entire pipeline runs locally on your machine — no data leaves your computer.</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Powered by faster-whisper · Ollama · Piper TTS · Streamlit<br>
    No cloud APIs · No data collection · Fully offline
</div>
""", unsafe_allow_html=True)
