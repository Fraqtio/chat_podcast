from openai import OpenAI
import json
import os
from src.dialog_parser import get_top_keywords, dictionary_key_info
from src.keys import OPENAI_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_KEY)


def generate_text(session_path, model="gpt-4o", max_tokens=2000):
    """Generates text using OpenAI API and saves it in the session folder."""

    dialog_path = os.path.join(session_path, "dialog.txt")
    dictionary_path = os.path.join(session_path, "dictionary.json")
    response_path = os.path.join(session_path, "last_response.txt")

    # Extract topics from the session’s dialog.txt
    topics = get_top_keywords(dialog_path)

    # Retrieve topic information from dictionary.json
    topic_info = dictionary_key_info(keywords=topics, dictionary_file_path=dictionary_path)

    # Construct the AI prompt
    prompt = f"""
    I want you to write a podcast dialog.
    It must be a discussion about the following topics: {", ".join(topics)}.
    Use this information about these topics: {topic_info}.
    The result must look like:
    "First sentence from person 1."
    "First sentence from person 2."
    "Second sentence from person 1."
    etc., without mentioning the speaker's name.
    Make sure they ask questions and respond naturally, like a real conversation.
    Ensure your response fits within 2000 tokens.
    """

    try:
        # Make API request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI that generates scientific podcast dialogues."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        # Extract and save response
        output_text = response.choices[0].message.content.strip()

        with open(response_path, "w", encoding="UTF-8") as f:
            f.writelines(line + "\n" for line in output_text.split("\n") if line.strip())

        return output_text

    except Exception as e:
        print(f"Error while generating text: {e}")
        return None


def generate_json(session_path):
    """Generates JSON files for TTS processing inside the session folder."""

    response_path = os.path.join(session_path, "last_response.txt")
    speaker1_json = os.path.join(session_path, "input_one.json")
    speaker2_json = os.path.join(session_path, "input_two.json")

    with open(response_path, "r", encoding="utf-8") as file, \
            open(speaker1_json, "w", encoding="utf-8") as outfile1, \
            open(speaker2_json, "w", encoding="utf-8") as outfile2:

        for count, line in enumerate(file):
            text_entry = {"text": line.strip().strip('"'), "output_file": f"line_{count:03d}.wav"}

            if count % 2 == 0:
                json.dump(text_entry, outfile1)
                outfile1.write("\n")
            else:
                json.dump(text_entry, outfile2)
                outfile2.write("\n")
