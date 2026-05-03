"""Reusable image-generation helper extracted from the original gen.py."""

import json
import re

import requests
from user_agent import generate_user_agent

BASE_URL = "https://www.free-ai-online.com/"


def _fetch_nonce(session: requests.Session) -> str | None:
    """Scrape the WP nonce required by the chat endpoint."""
    resp = session.get(BASE_URL, headers={"User-Agent": generate_user_agent()})
    resp.raise_for_status()

    patterns = [
        r'var\s+mwai_nonce\s*=\s*["\']([a-f0-9]+)["\']',
        r'"nonce":"([a-f0-9]+)"',
        r'<meta\s+name=["\']wp-nonce["\']\s+content=["\']([a-f0-9]+)["\']',
        r'<meta\s+name=["\']nonce["\']\s+content=["\']([a-f0-9]+)["\']',
        r'x-wp-nonce:\s*["\']?([a-f0-9]+)["\']?',
    ]
    for pattern in patterns:
        match = re.search(pattern, resp.text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def generate_image(prompt: str) -> dict:
    """Generate an image from *prompt* and return ``{"success": bool, "image_url": str | None}``."""
    session = requests.Session()
    nonce = _fetch_nonce(session)
    if not nonce:
        return {"success": False, "image_url": None}

    payload = {
        "botId": "AI IMAGE",
        "customId": None,
        "session": "69d532dce3118",
        "chatId": "3tz0gw4axx3",
        "contextId": 766,
        "messages": [
            {
                "id": "ejv7c2t6x2v",
                "role": "assistant",
                "content": "Hello! What image do you want?",
                "who": "AI: ",
            }
        ],
        "newMessage": prompt,
        "newFileId": None,
        "newFileIds": None,
        "stream": True,
    }

    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "x-wp-nonce": nonce,
        "origin": BASE_URL,
        "referer": "https://www.free-ai-online.com/free-square-ai-image-generator/",
    }

    resp = session.post(
        BASE_URL + "wp-json/mwai-ui/v1/chats/submit",
        data=json.dumps(payload),
        headers=headers,
        stream=True,
    )

    image_url = None
    for line in resp.iter_lines(decode_unicode=True):
        if line and line.startswith("data:"):
            try:
                data = json.loads(line[6:])
                if data.get("type") == "end":
                    end_data = json.loads(data.get("data", "{}"))
                    images = end_data.get("images", [])
                    if images:
                        image_url = images[0]
            except (json.JSONDecodeError, ValueError):
                pass

    return {"success": bool(image_url), "image_url": image_url}
