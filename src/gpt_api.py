from openai import OpenAI
import os
import json
from src.dialog_parser import get_top_keywords
from src.config import SPEAKER1_JSON_PATH, SPEAKER2_JSON_PATH
from src.keys import OPENAI_KEY


# Initialize OpenAI client (NEW WAY)
client = OpenAI(api_key=OPENAI_KEY)


def generate_text(model="gpt-4o", max_tokens=2000):
    """Generates text using OpenAI API."""
    topics = get_top_keywords()
    prompt = f"""
            I want you to write a podcast dialog.
            It must be a discussion about following topics: {", ".join(topics)}
            Result must looks like:
            "First sentence to speak from person 1."
            "First sentence to speak from person 2."
            "Second sentence to speak from person 1." 
            etc. without mention of speaker.
            Make sure your response will handle 2000 tokens
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

        # Extract the AI's response
        output_text = response.choices[0].message.content.strip()

        # Save response to file
        with open("last_response.txt", mode="w", encoding="UTF-8") as f:
            f.writelines(line + "\n" for line in response.choices[0].message.content.split("\n") if line.strip())

        return output_text

    except Exception as e:
        print(f"Error while generating text: {e}")
        return None


def generate_json():
    # Read file and process lines
    with open(SPEAKER1_JSON_PATH, "w", encoding="utf-8") as outfile1, open(SPEAKER2_JSON_PATH, "w",
                                                                           encoding="utf-8") as outfile2:
        # Read the response file and process each line
        with open('last_response.txt', 'r', encoding="utf-8") as file:
            for count, line in enumerate(file):

                text_entry = {
                    "text": line.strip().strip('"'),  # Remove surrounding quotes & spaces
                    "output_file": f"line_{count:03d}.wav",
                }

                # Alternate between two speakers
                if count % 2 == 0:
                    json.dump(text_entry, outfile1)
                    outfile1.write("\n")
                else:
                    json.dump(text_entry, outfile2)
                    outfile2.write("\n")

