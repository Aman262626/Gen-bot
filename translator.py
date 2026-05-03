"""Text translation using MyMemory free translation API (no key required)."""

import requests


def translate_text(
    text: str, target_lang: str = "en", source_lang: str = "auto"
) -> dict:
    """Translate *text* to *target_lang*.

    Uses the MyMemory free API. Returns a dict with translated_text,
    source_lang, and target_lang.
    """
    lang_pair = f"{source_lang}|{target_lang}"
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": lang_pair}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return {"error": f"Translation failed: {exc}"}

    translated = data.get("responseData", {}).get("translatedText")
    if not translated:
        return {"error": "No translation returned."}

    detected = data.get("responseData", {}).get("detectedLanguage", source_lang)

    return {
        "translated_text": translated,
        "source_lang": detected if detected else source_lang,
        "target_lang": target_lang,
    }
