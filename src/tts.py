import os
import subprocess
from pydub import AudioSegment
from src.config import PIPER_EXE_PATH, TTS_MODEL1_PATH, TTS_MODEL2_PATH


def geretare_wav(session_path):
    """Runs Piper TTS and saves WAV files inside the session folder."""
    speaker1_json = os.path.join(session_path, "input_one.json")
    speaker2_json = os.path.join(session_path, "input_two.json")

    cmd1 = f"type {speaker1_json} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL1_PATH}"
    cmd2 = f"type {speaker2_json} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL2_PATH}"

    subprocess.run(cmd1, shell=True, cwd=session_path)
    subprocess.run(cmd2, shell=True, cwd=session_path)


def combine_wav(session_path):
    """Merges all WAV files in the session folder into a single podcast file."""
    # Get all WAV files in the folder, sorted by name
    wav_files = sorted([f for f in os.listdir(session_path) if f.endswith(".wav")])

    # Create a 0.4s silent audio segment
    silence = AudioSegment.silent(duration=400)  # 400ms silence

    # Start with an empty AudioSegment
    combined_audio = AudioSegment.empty()

    for wav in wav_files:
        wav_path = os.path.join(session_path, wav)
        sound = AudioSegment.from_wav(wav_path)
        combined_audio += sound + silence

    output_file = os.path.join(session_path, "final_podcast.wav")

    # Export the final concatenated file
    combined_audio.export(output_file, format="wav")

    # Delete all individual WAV files except the final one
    for wav in wav_files:
        wav_path = os.path.join(session_path, wav)
        if wav_path != output_file:
            os.remove(wav_path)
