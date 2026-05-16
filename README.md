# 🎙️ Voice Assistant

Local speech transcription with cloud-based response generation and TTS.

**Pipeline:** Upload Audio → Whisper STT → Gemini 3.1 Flash Lite → gTTS → Play Audio

---

## Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **STT** | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech-to-text (base model, CPU, int8) |
| **LLM** | [Gemini 3.1 Flash Lite](https://ai.google.dev/) | Cloud language model inference via API |
| **TTS** | [gTTS](https://github.com/pndurette/gTTS) | Text-to-speech (Google TTS, cross-platform) |
| **UI** | [Streamlit](https://streamlit.io/) | Web interface |

---

## Prerequisites

1. **Python 3.10+**
2. A **Gemini API key** — get one free at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Setup

```bash
# 1. Clone / navigate to the project
cd V-BOT-main

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Provide your Gemini API key in a `.env` file as `GEMINI_API_KEY`.

---

## Project Structure

```
V-BOT-main/
├── app.py              # Streamlit UI — ties the pipeline together
├── stt.py              # Speech-to-Text (faster-whisper)
├── llm.py              # LLM interface (Gemini 3.1 Flash Lite)
├── tts.py              # Text-to-Speech (gTTS)
├── requirements.txt    # Python dependencies
├── .env                # Local API keys (git-ignored)
├── README.md           # This file
└── tmp/                # Auto-created — Temporary audio storage
```

---

## How It Works

1. **Upload** a `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, or `.webm` audio file
2. **Transcription** — `faster-whisper` converts speech to text on CPU
3. **LLM Response** — the transcript is sent to `Gemini 3.1 Flash Lite` via the Google GenAI API
4. **Speech Synthesis** — `gTTS` converts the LLM response to audio (MP3)
5. **Playback** — the synthesized audio plays directly in the browser

---

## Key Design Decisions

- **Sequential Processing** — The pipeline runs in steps (STT -> LLM -> TTS) rather than a real-time stream.
- **No mic input** — upload-only avoids browser permission complexities and maintains focus on the pipeline.
- **In-Memory TTS** — No audio files are saved to disk during the synthesis step.
- **Hybrid Flow** — Local STT provides a foundation for privacy, while Cloud APIs provide high-quality generation and synthesis.

---

## Privacy

Speech transcription runs locally before text is sent to cloud APIs. The transcript text is sent to the Gemini API for inference and gTTS for synthesis — both subject to [Google's privacy policy](https://policies.google.com/privacy).

---

## License

MIT
