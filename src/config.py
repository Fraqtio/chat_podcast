import spacy
import os

# Load SpaCy model once
nlp = spacy.load("en_core_web_md")

# Define base directory and default file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIALOG_PATH = os.path.join(BASE_DIR, "data", "dialog.txt")
INPUT_DICTIONARY_PATH = os.path.join(BASE_DIR, "data", "dictionary.json")
PIPER_EXE_PATH = os.path.join(BASE_DIR, "piper", "piper.exe")
SPEAKER1_JSON_PATH = os.path.join(BASE_DIR, "src", "input_one.json")
SPEAKER2_JSON_PATH = os.path.join(BASE_DIR, "src", "input_two.json")
TTS_MODEL1_PATH = os.path.join(BASE_DIR, "piper", "en_GB-alba-medium.onnx")
TTS_MODEL2_PATH = os.path.join(BASE_DIR, "piper", "en_GB-alan-medium.onnx")
TTS_OUTPUT_PATH = os.path.join(BASE_DIR, "src", "audio")
