"""Vercel serverless function for the chatbot API."""

import json

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

CHATBOT_URL = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ),
    "Location": "https://seoschmiede.at/en/aitools/chatgpt-tool/",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_chatbot_response(message: str, history: list[dict] | None = None) -> str:
    """Get a response from the chatbot API."""
    messages = []
    if history:
        messages.extend(history)
    else:
        messages.append({"role": "assistant", "content": "Hello! How can I help you today?"})
    messages.append({"role": "user", "content": f"Please respond in English. {message}"})

    payload = {"messages": messages}

    try:
        resp = requests.post(CHATBOT_URL, json=payload, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        return f"Error: API returned status {resp.status_code}"
    except requests.exceptions.RequestException as exc:
        return f"Request failed: {exc}"
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        return f"Failed to parse response: {exc}"


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    message = body.get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400

    history = body.get("history")
    reply = get_chatbot_response(message, history)
    return jsonify({"reply": reply})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})
