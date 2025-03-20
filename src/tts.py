import os
import subprocess
from pydub import AudioSegment
from src.config import PIPER_EXE_PATH, TTS_MODEL1_PATH, TTS_MODEL2_PATH, \
                   SPEAKER1_JSON_PATH, SPEAKER2_JSON_PATH, TTS_OUTPUT_PATH


def geretare_wav():

    cmd1 = f"type {SPEAKER1_JSON_PATH} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL1_PATH}"
    cmd2 = f"type {SPEAKER2_JSON_PATH} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL2_PATH}"
    # os.system(f"type {SPEAKER1_JSON_PATH} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL1_PATH}")
    # os.system(f"type {SPEAKER2_JSON_PATH} | {PIPER_EXE_PATH} --json-input -m {TTS_MODEL2_PATH} ")
    subprocess.run(cmd1, shell=True, cwd=TTS_OUTPUT_PATH)
    subprocess.run(cmd2, shell=True, cwd=TTS_OUTPUT_PATH)


def combine_wav():
    # Define the directory where WAV files are stored
    output_file = "final_podcast.wav"

    # Get all WAV files in the folder, sorted by name
    wav_files = sorted([f for f in os.listdir(TTS_OUTPUT_PATH) if f.endswith(".wav")])

    print(wav_files)
    # Create a 0.4s silent audio segment
    silence = AudioSegment.silent(duration=400)  # 400ms silence

    # Load the first file
    combined_audio = AudioSegment.empty()

    # Process each file and concatenate them with silence in between
    for wav in wav_files:
        wav_path = os.path.join(TTS_OUTPUT_PATH, wav)
        sound = AudioSegment.from_wav(wav_path)

        # Add the audio file to the combined file, followed by silence
        combined_audio += sound + silence

    # Export the final concatenated file
    combined_audio.export(output_file, format="wav")

    # Delete all individual WAV files except the final one
    for wav in wav_files:
        wav_path = os.path.join(TTS_OUTPUT_PATH, wav)
        if wav_path != output_file:  # Ensure we don't delete the final podcast
            os.remove(wav_path)
