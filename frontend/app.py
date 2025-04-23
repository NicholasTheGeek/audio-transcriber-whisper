import streamlit as st
import requests
import base64
import sounddevice as sd
import scipy.io.wavfile
import io

#Page Configuration
st.set_page_config(
    page_title="Whisper Audio Transcriber",
    page_icon="🎧",
    layout="centered",
)

#Custom CSS Styling
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .main{
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.05); 
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

#Title and Description
st.title("🎧 Whisper Audio Transcriber")
st.markdown("Upload or record audio, and let Whisper transcribe and detect the language using a locally running AI model.")

#Theme Toggle
theme = st.radio("🌓 Select Theme", options=["Light", "Dark"], horizontal=True)
if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #1c1c1c;
            color: white;
        }
        .main, .block-container {
            background-color: #2e2e2e;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, label, .stRadio > div, .stCheckbox > div, .stSlider > div, .stFileUploader > div {
            color: white !important;
        }
        .stRadio > label, .stCheckbox > label, .stSlider > label, .stFileUploader > label {
            color: white !important;
        }
        .st-bw {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
            color: black;
        }
        .main, .block-container {
            background-color: white;
            color: black;
        }
        h1, h2, h3, h4, h5, h6, p, label, .stRadio > div, .stCheckbox > div, .stSlider > div, .stFileUploader > div {
            color: black !important;
        }
        .stRadio > label, .stCheckbox > label, .stSlider > label, .stFileUploader > label {
            color: black !important;
        }
        .st-bw {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)



#Live Mic Recording
record_option = st.checkbox("🎤 Record with Microphone")
uploaded_file = None

if record_option:
    duration = st.slider("⏱️ Duration (seconds)", 1, 10, 5)
    if st.button("🔴 Record"):
        st.info("Recording...")
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        # Save recording to BytesIO
        wav_io = io.BytesIO()
        scipy.io.wavfile.write(wav_io, fs, recording)
        wav_io.seek(0)
        uploaded_file = wav_io

        st.audio(wav_io, format="audio/wav")
else:
    uploaded_file = st.file_uploader("📁 Choose your audio file", type=["mp3", "wav", "m4a"])

#Transcription Button
if uploaded_file:
    if st.button("📝 Transcribe"):
        with st.spinner("Transcribing... hang tight 🌀"):
            try:
                files = {
                    "file": (
                        "recording.wav",  # filename
                        uploaded_file.read() if not record_option else uploaded_file.getvalue(),
                        "audio/wav")
                }
                response = requests.post("http://localhost:8000/transcribe/", files=files)

                if response.status_code == 200:
                    data = response.json()
                    transcription = data.get("transcription", "")
                    language = data.get("language", "Unknown")
                    word_count = len(transcription.split())

                    st.success("✅ Transcription successful!")
                    st.subheader("🗒️ Here's what was said:")
                    st.write(transcription)
                    st.markdown(f"🌐 **Language Detected:** `{language}`")
                    st.markdown(f"**🧮 Word Count:** {word_count}")

                    # --- Download Transcription ---
                    b64 = base64.b64encode(transcription.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="transcription.txt">📥 Download transcription</a>'
                    st.markdown(href, unsafe_allow_html=True)

                else:
                    st.error(f"❌ Server error: {response.text}")
            except Exception as e:
                st.error(f"🚨 Oops! Something went wrong: {e}")