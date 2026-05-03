"""Weather lookup using wttr.in (no API key required)."""

import requests


def get_weather(city: str) -> dict:
    """Fetch current weather for *city* from wttr.in.

    Returns a dict with keys: city, temperature, feels_like, description,
    humidity, wind, visibility, pressure.
    """
    url = f"https://wttr.in/{city}?format=j1"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Gen-bot/1.0"})
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return {"error": f"Could not fetch weather: {exc}"}

    try:
        current = data["current_condition"][0]
        area = data.get("nearest_area", [{}])[0]
        area_name = area.get("areaName", [{}])[0].get("value", city)
        country = area.get("country", [{}])[0].get("value", "")

        return {
            "city": f"{area_name}, {country}" if country else area_name,
            "temperature": f"{current['temp_C']}°C / {current['temp_F']}°F",
            "feels_like": f"{current['FeelsLikeC']}°C / {current['FeelsLikeF']}°F",
            "description": current["weatherDesc"][0]["value"],
            "humidity": f"{current['humidity']}%",
            "wind": f"{current['windspeedKmph']} km/h {current['winddir16Point']}",
            "visibility": f"{current['visibility']} km",
            "pressure": f"{current['pressure']} mb",
        }
    except (KeyError, IndexError):
        return {"error": "Could not parse weather data."}
