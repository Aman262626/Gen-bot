"""AI chatbot helper for Telegram integration (extracted from gpt.py)."""

import requests


def get_chat_response(question: str) -> str:
    """Get an AI response for *question* via the chatbot API."""
    payload = {
        "messages": [
            {"role": "assistant", "content": "Hello! How can I help you today?"},
            {"role": "user", "content": question},
        ]
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        ),
        "Location": "https://seoschmiede.at/en/aitools/chatgpt-tool/",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        return f"API error (status {resp.status_code}). Try again later."
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as exc:
        return f"Error: {exc}"
