import re
import json
from collections import Counter
from src.config import nlp, INPUT_DIALOG_PATH, INPUT_DICTIONARY_PATH


def get_top_keywords(dialog_file_path=INPUT_DIALOG_PATH, top_n=10):
    """Extracts and returns the top N keywords from the given dialog file."""
    cleaned_text = []
    pattern = re.compile(r'^".+?":$')  # Matches lines with speaker names

    try:
        # Read file and filter out speaker names
        with open(dialog_file_path, "r", encoding="UTF8") as file:
            for line in file:
                if not pattern.match(line.strip()):
                    cleaned_text.append(line.strip())

        # Join filtered text into one block
        dialog_text_cleaned = " ".join(cleaned_text)

        # Process text with SpaCy NLP model
        doc = nlp(dialog_text_cleaned)

        # Extract keywords (lemmatized, excluding stopwords & punctuation)
        keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

        # Count keyword frequency and return top N
        keyword_counts = Counter(keywords)
        return [word for word, _ in keyword_counts.most_common(top_n)]

    except FileNotFoundError:
        print(f"Error: File '{dialog_file_path}' not found.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def dictionary_key_info(keywords, dictionary_file_path=INPUT_DICTIONARY_PATH):
    with open(dictionary_file_path, 'r') as file:
        json_data = json.load(file)

        matching_keys = set(keywords) & set(json_data.keys())
        # Extract values for matching keys
        extracted_info = {key: json_data[key] for key in matching_keys}
    return extracted_info
