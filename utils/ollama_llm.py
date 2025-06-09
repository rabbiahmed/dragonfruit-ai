# utils/ollama_llm.py

import os
import requests
import logging

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

def ask_ollama(prompt):
    """
        Sends a prompt to the Ollama API and returns the response text.
        Falls back to a default message if the request fails.

        Returns:
            str: AI-generated response or error message.
        """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(url, json=payload, timeout=15)
        res.raise_for_status()  # Raises HTTPError for bad responses
        return res.json().get("response", "⚠️ No response from Ollama.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama API error: {e}")
        return f"⚠️ Error connecting to Ollama: {e}"
