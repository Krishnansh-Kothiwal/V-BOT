# 🎙️ Offline Voice Assistant

A **fully local, fully free** voice assistant that runs entirely on your machine — no cloud APIs, no data collection, no subscriptions.

**Pipeline:** Upload Audio → Whisper STT → Ollama LLM → Piper TTS → Play Audio

---

## Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **STT** | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech-to-text (base model, CPU, int8) |
| **LLM** | [Ollama](https://ollama.com/) + `qwen2.5:7b` | Local language model inference |
| **TTS** | [Piper](https://github.com/rhasspy/piper) | Text-to-speech (`en_US-lessac-medium`) |
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

> **Note:** On first run, the Piper voice model (~75 MB) will be auto-downloaded from HuggingFace into a `voices/` directory. This is a one-time download.

---

## Project Structure

```
Proj3/
├── app.py              # Streamlit UI — ties the pipeline together
├── stt.py              # Speech-to-Text (faster-whisper)
├── llm.py              # LLM call (Ollama / qwen2.5:7b)
├── tts.py              # Text-to-Speech (Piper)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── voices/             # Auto-created — Piper voice models
```

---

## How It Works

1. **Upload** a `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, or `.webm` audio file
2. **Transcription** — faster-whisper converts speech to text on CPU
3. **LLM Response** — the transcript is sent to Ollama (`qwen2.5:7b`) running locally
4. **Speech Synthesis** — Piper converts the LLM response back to audio
5. **Playback** — the synthesized audio plays directly in the browser

---

## Key Design Decisions

- **No mic input** — upload-only keeps the scope focused and avoids browser permission issues
- **No streaming** — simpler pipeline, easier to debug
- **No agents/tools** — direct prompt → response, no unnecessary abstractions
- **CPU inference** — works on any machine without a GPU (slower but universal)
- **Auto-download** — Piper voice model is fetched automatically on first run

---

## Privacy

**Everything runs locally.** No audio, text, or data ever leaves your machine. There are zero external API calls (except the one-time Piper model download).

---

## License

MIT
