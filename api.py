from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import logging
from datetime import datetime

from src.gpt_api import generate_text, generate_json
from src.tts import geretare_wav, combine_wav
from src.config import SESSIONS_DIR

# Configure logging
log_filename = os.path.join("logs", f"api_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("API service started.")

app = FastAPI()

@app.get("/")
def home():
    logging.info("Root endpoint accessed.")
    return {"message": "Welcome to the Podcast API!"}

@app.post("/get-podcast")
async def get_podcast(dialog: UploadFile = File(...), dictionary: UploadFile = File(...)):
    try:
        session_id = str(uuid.uuid4())[:8]
        session_path = os.path.join(SESSIONS_DIR, session_id)
        os.makedirs(session_path, exist_ok=True)

        logging.info(f"Created session: {session_id}")

        dialog_path = os.path.join(session_path, "dialog.txt")
        with open(dialog_path, "wb") as buffer:
            shutil.copyfileobj(dialog.file, buffer)
        logging.info(f"dialog.txt saved to {dialog_path}")

        dictionary_path = os.path.join(session_path, "dictionary.json")
        with open(dictionary_path, "wb") as buffer:
            shutil.copyfileobj(dictionary.file, buffer)
        logging.info(f"dictionary.json saved to {dictionary_path}")

        generate_text(session_path)
        logging.info(f"Text generated for session {session_id}")

        generate_json(session_path)
        logging.info(f"JSON files created for session {session_id}")

        geretare_wav(session_path)
        logging.info(f"Audio generated for session {session_id}")

        combine_wav(session_path)
        logging.info(f"Podcast combined for session {session_id}")

        final_podcast_path = os.path.join(session_path, "final_podcast.wav")

        if os.path.exists(final_podcast_path):
            logging.info(f"Podcast ready: {final_podcast_path}")
            return {
                "status": "success",
                "session_id": session_id,
                "download_url": f"http://127.0.0.1:8000/get-audio/{session_id}"
            }
        else:
            logging.error("Final podcast file not found.")
            raise HTTPException(status_code=500, detail="Podcast audio file not found after processing.")

    except Exception as e:
        logging.exception("Exception during /get-podcast:")
        raise HTTPException(status_code=500, detail=f"Error processing podcast: {str(e)}")

@app.get("/get-audio/{session_id}")
def get_podcast_audio(session_id: str):
    session_path = os.path.join(SESSIONS_DIR, session_id)
    final_podcast_path = os.path.join(session_path, "final_podcast.wav")

    if os.path.exists(final_podcast_path):
        logging.info(f"Podcast served for session {session_id}")
        return FileResponse(final_podcast_path, media_type="audio/wav", filename="final_podcast.wav")
    else:
        logging.warning(f"Missing final_podcast.wav for session {session_id}")
        raise HTTPException(status_code=404, detail="Podcast audio file not found.")