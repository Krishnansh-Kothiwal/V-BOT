# 🎙️ Offline Voice Assistant

A **fully local, fully free** voice assistant that runs entirely on your machine — no cloud APIs, no data collection, no subscriptions.

**Pipeline:** Upload Audio → Whisper STT → Ollama LLM → pyttsx3 TTS → Play Audio

---

## Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **STT** | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech-to-text (base model, CPU, int8) |
| **LLM** | [Ollama](https://ollama.com/) + `qwen2.5:7b` | Local language model inference |
| **TTS** | [pyttsx3](https://github.com/nateshmbhat/pyttsx3) | Text-to-speech (Native Windows SAPI) |
| **UI** | [Streamlit](https://streamlit.io/) | Web interface |

---

## Prerequisites

1. **Python 3.10+**
2. **Ollama** installed and running with `qwen2.5:7b`:
   ```bash
   # If you haven't pulled the model yet:
   ollama pull qwen2.5:7b

   # Make sure Ollama is running:
   ollama serve
   ```

---

## Setup

```bash
# 1. Clone / navigate to the project
cd Proj3

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

> **Note:** The assistant uses your system's native voices via SAPI5. No extra downloads are required for speech synthesis.

---

## Project Structure

```
Proj3/
├── app.py              # Streamlit UI — ties the pipeline together
├── stt.py              # Speech-to-Text (faster-whisper)
├── llm.py              # LLM call (Ollama / qwen2.5:7b)
├── tts.py              # Text-to-Speech (pyttsx3)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── tmp/                # Auto-created — Temporary audio storage
```

---

## How It Works

1. **Upload** a `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, or `.webm` audio file
2. **Transcription** — faster-whisper converts speech to text on CPU
3. **LLM Response** — the transcript is sent to Ollama (`qwen2.5:7b`) running locally
4. **Speech Synthesis** — pyttsx3 converts the LLM response back to audio using native system voices
5. **Playback** — the synthesized audio plays directly in the browser

---

## Key Design Decisions

- **No mic input** — upload-only keeps the scope focused and avoids browser permission issues
- **No streaming** — simpler pipeline, easier to debug
- **No agents/tools** — direct prompt → response, no unnecessary abstractions
- **CPU inference** — works on any machine without a GPU (slower but universal)
- **Native TTS** — Uses system voices to avoid large model downloads and maintain speed

---

## Privacy

**Everything runs locally.** No audio, text, or data ever leaves your machine. There are zero external API calls (except the one-time Piper model download).

---

## License

MIT
