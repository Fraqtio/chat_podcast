import spacy
import os

# Load SpaCy model once
nlp = spacy.load("en_core_web_md")

# Define base directory and default file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")

PIPER_EXE_PATH = os.path.join(BASE_DIR, "piper", "piper.exe")
TTS_MODEL1_PATH = os.path.join(BASE_DIR, "piper", "en_GB-alba-medium.onnx")
TTS_MODEL2_PATH = os.path.join(BASE_DIR, "piper", "en_GB-alan-medium.onnx")
