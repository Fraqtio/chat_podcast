import re
import json
import logging
from datetime import datetime
import os
from collections import Counter
from src.config import nlp

# Setup logging
log_filename = os.path.join("logs", f"dialog_parser_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("dialog_parser module loaded.")

def get_top_keywords(dialog_file_path, top_n=10):
    """Extracts and returns the top N keywords from the given dialog file."""
    cleaned_text = []
    pattern = re.compile(r'^".+?":$')  # Matches lines with speaker names

    try:
        with open(dialog_file_path, "r", encoding="UTF8") as file:
            for line in file:
                if not pattern.match(line.strip()):
                    cleaned_text.append(line.strip())
        logging.info(f"Loaded dialog from {dialog_file_path}")

        dialog_text_cleaned = " ".join(cleaned_text)
        doc = nlp(dialog_text_cleaned)

        keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
        keyword_counts = Counter(keywords)
        top_keywords = [word for word, _ in keyword_counts.most_common(top_n)]

        logging.info(f"Extracted top {top_n} keywords: {top_keywords}")
        return top_keywords

    except FileNotFoundError:
        logging.error(f"File not found: {dialog_file_path}")
        return []
    except Exception as e:
        logging.exception("Exception in get_top_keywords:")
        return []

def dictionary_key_info(keywords, dictionary_file_path):
    try:
        with open(dictionary_file_path, 'r') as file:
            json_data = json.load(file)

        matching_keys = set(keywords) & set(json_data.keys())
        extracted_info = {key: json_data[key] for key in matching_keys}

        logging.info(f"Found info for {len(matching_keys)} keyword(s) from dictionary.")
        return extracted_info

    except FileNotFoundError:
        logging.error(f"Dictionary file not found: {dictionary_file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in {dictionary_file_path}")
        return {}
    except Exception as e:
        logging.exception("Exception in dictionary_key_info:")
        return {}