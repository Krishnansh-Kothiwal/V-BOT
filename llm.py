"""
llm.py — Local LLM interface via Ollama (qwen2.5:7b)
"""

import requests


def generate_response(prompt: str) -> str:
    """Send a prompt to the local Ollama server and return the response."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
