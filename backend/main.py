from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import shutil
import os

app = FastAPI()

# Load the Whisper model once
model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        shutil.copyfileobj(file.file, temp_audio_file)
        temp_audio_path = temp_audio_file.name

    try:
        # Transcribe and detect language using Whisper
        result = model.transcribe(temp_audio_path)
        return {
             "transcription": result["text"].strip(),
             "language": result["language"]
        }
    finally:
        os.remove(temp_audio_path)
