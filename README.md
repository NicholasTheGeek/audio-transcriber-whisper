# 🎧 Whisper Audio Transcriber

A clean and interactive full-stack app that lets you upload or record audio and get real-time transcriptions with language detection — powered by [OpenAI Whisper](https://openai.com/research/whisper), built with **Streamlit** and **FastAPI**.

## 🔥 Features

- 🎤 Upload or record audio (via mic)
- 📝 Local transcription with Whisper
- 🌐 Auto language detection
- 🌓 Light/Dark mode toggle
- 📥 Download transcription as `.txt`

## 📦 Tech Stack

- `FastAPI` – backend API to handle transcriptions
- `Streamlit` – beautiful interactive frontend
- `Whisper` – OpenAI speech-to-text model
- `Sounddevice`, `Scipy` – for mic recording
- `CapCut` – for editing YouTube demo

## ⚙️ How to Run

### 1. Clone the repo

## How to Run
    1. OpenAI speech-to-text model
    2. Run backend: `uvicorn backend.main:app --reload`
    3. Run frontend: `streamlit run frontend/app.py`
    4. Upload an MP3/WAV and get transcriptions!
    
# 🧠 Lessons Learned
    Originally tried integrating Whisper with Ollama but faced model loading and deployment issues. This led me to learn and adapt with the local Whisper API instead — a great reminder that every bug is a learning opportunity!

📽️ Demo
📺 Watch the full project walkthrough on YouTube
 https://youtu.be/WgoCvZD6ZBE
