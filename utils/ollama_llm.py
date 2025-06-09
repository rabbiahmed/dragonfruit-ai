# utils/ollama_llm.py

import requests


def ask_ollama(prompt):
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        return res.json().get("response", "Sorry, no response.")
    except Exception as e:
        return f"⚠️ Error: {e}"
