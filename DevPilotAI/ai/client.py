import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


def ask_ai(prompt):
    """
    Send a prompt to Gemini and return the response.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text