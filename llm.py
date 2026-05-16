"""
llm.py — Cloud LLM interface via Gemini API (gemini-3.1-flash-lite)
"""

from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = (
    "You are a helpful voice assistant. "
    "Always respond in plain text only. "
    "Do not use any markdown formatting such as asterisks, bold, italics, "
    "bullet points, headers, or backticks. Write as if speaking naturally."
)

def generate_response(prompt: str, api_key: str) -> str:
    """Send a prompt to the Gemini API and return the response text."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )
    return response.text
