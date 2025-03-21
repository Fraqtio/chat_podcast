import os
import subprocess
import logging
from datetime import datetime
from pydub import AudioSegment
from src.config import PIPER_EXE_PATH, TTS_MODEL1_PATH, TTS_MODEL2_PATH

# Setup logging
log_filename = os.path.join("logs", f"tts_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("tts module loaded.")


def geretare_wav(session_path):
    """Runs Piper TTS and saves WAV files inside the session folder."""

    speaker1_json = os.path.join(session_path, "input_one.json")
    speaker2_json = os.path.join(session_path, "input_two.json")

    cmd1 = f"type {speaker1_json} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL1_PATH}"
    cmd2 = f"type {speaker2_json} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL2_PATH}"

    try:
        logging.info(f"Generating TTS audio from {speaker1_json}")
        subprocess.run(cmd1, shell=True, cwd=session_path, check=True)

        logging.info(f"Generating TTS audio from {speaker2_json}")
        subprocess.run(cmd2, shell=True, cwd=session_path, check=True)

        logging.info(f"WAV files generated in {session_path}")
    except subprocess.CalledProcessError as e:
        logging.exception("Error while running Piper TTS command:")
    except Exception as e:
        logging.exception("Unexpected exception during TTS generation:")


def combine_wav(session_path):
    """Merges all WAV files in the session folder into a single podcast file."""

    try:
        wav_files = sorted([f for f in os.listdir(session_path) if f.endswith(".wav")])
        logging.info(f"🔍 Found {len(wav_files)} WAV files to combine in {session_path}")

        silence = AudioSegment.silent(duration=400)  # 400ms silence
        combined_audio = AudioSegment.empty()

        for wav in wav_files:
            wav_path = os.path.join(session_path, wav)
            sound = AudioSegment.from_wav(wav_path)
            combined_audio += sound + silence

        output_file = os.path.join(session_path, "final_podcast.wav")
        combined_audio.export(output_file, format="wav")

        logging.info(f"🎧 Final podcast saved to {output_file}")

        # Clean up intermediate WAV files
        for wav in wav_files:
            wav_path = os.path.join(session_path, wav)
            if wav_path != output_file:
                os.remove(wav_path)
                logging.info(f"🗑️ Deleted intermediate file: {wav_path}")

    except Exception as e:
        logging.exception("Error while combining WAV files:")