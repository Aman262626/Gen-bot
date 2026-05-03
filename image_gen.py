"""Reusable image-generation helper.

Uses Pollinations.ai (free, no auth required) as the primary provider.
Falls back to free-ai-online.com if available.
"""

import json
import logging
import re
from urllib.parse import quote

import requests
from user_agent import generate_user_agent

logger = logging.getLogger(__name__)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&nologo=true"
FREE_AI_BASE_URL = "https://www.free-ai-online.com/"


def generate_image(prompt: str) -> dict:
    """Generate an image and return ``{"success": bool, "image_url": str | None}``."""
    result = _generate_pollinations(prompt)
    if result["success"]:
        return result

    logger.info("Pollinations failed, trying free-ai-online fallback")
    return _generate_free_ai(prompt)


def _generate_pollinations(prompt: str) -> dict:
    """Generate via Pollinations.ai — simple GET request, no auth needed."""
    url = POLLINATIONS_URL.format(prompt=quote(prompt))
    try:
        resp = requests.head(url, timeout=30, allow_redirects=True)
        if resp.status_code == 200:
            return {"success": True, "image_url": url}
    except requests.exceptions.RequestException as exc:
        logger.warning("Pollinations request failed: %s", exc)
    return {"success": False, "image_url": None}


def _fetch_nonce(session: requests.Session) -> str | None:
    """Scrape the WP nonce required by the free-ai-online chat endpoint."""
    resp = session.get(FREE_AI_BASE_URL, headers={"User-Agent": generate_user_agent()})
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


def _generate_free_ai(prompt: str) -> dict:
    """Generate via free-ai-online.com (fallback)."""
    try:
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
            "origin": FREE_AI_BASE_URL,
            "referer": "https://www.free-ai-online.com/free-square-ai-image-generator/",
        }

        resp = session.post(
            FREE_AI_BASE_URL + "wp-json/mwai-ui/v1/chats/submit",
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
    except requests.exceptions.RequestException as exc:
        logger.warning("free-ai-online request failed: %s", exc)
        return {"success": False, "image_url": None}
