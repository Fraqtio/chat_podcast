from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid

from src.gpt_api import generate_text, generate_json
from src.tts import geretare_wav, combine_wav
from src.config import SESSIONS_DIR

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Podcast API!"}

@app.post("/get-podcast")
async def get_podcast(dialog: UploadFile = File(...), dictionary: UploadFile = File(...)):
    """Creates a session folder, stores files, processes the podcast, and returns the final WAV file."""

    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())[:8]  # Shorten UUID for readability
        session_path = os.path.join(SESSIONS_DIR, session_id)

        # Ensure session folder exists
        os.makedirs(session_path, exist_ok=True)

        # Save uploaded `dialog.txt`
        dialog_path = os.path.join(session_path, "dialog.txt")
        with open(dialog_path, "wb") as buffer:
            shutil.copyfileobj(dialog.file, buffer)

        # Save uploaded `dictionary.json`
        dictionary_path = os.path.join(session_path, "dictionary.json")
        with open(dictionary_path, "wb") as buffer:
            shutil.copyfileobj(dictionary.file, buffer)

        # Run the full podcast pipeline
        generate_text(session_path)  # Generate podcast text
        generate_json(session_path)  # Convert dialogue into JSON for TTS
        geretare_wav(session_path)  # Convert JSON text to speech
        combine_wav(session_path)  # Merge WAV files into a final podcast

        # Return the final podcast audio file
        final_podcast_path = os.path.join(session_path, "final_podcast.wav")

        if os.path.exists(final_podcast_path):
            return {
                "status": "success",
                "session_id": session_id,
                "download_url": f"http://127.0.0.1:8000/get-audio/{session_id}"
            }
        else:
            raise HTTPException(status_code=500, detail="Podcast audio file not found after processing.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing podcast: {str(e)}")


@app.get("/get-audio/{session_id}")
def get_podcast_audio(session_id: str):
    """Returns the final podcast audio file for a given session."""
    session_path = os.path.join(SESSIONS_DIR, session_id)
    final_podcast_path = os.path.join(session_path, "final_podcast.wav")

    if os.path.exists(final_podcast_path):
        return FileResponse(final_podcast_path, media_type="audio/wav", filename="final_podcast.wav")
    else:
        raise HTTPException(status_code=404, detail="Podcast audio file not found.")