#!/usr/bin/env python3
"""
Weather MCP Server using FastMCP
Now with REAL APIs:
- Open-Meteo for worldwide weather
- NWS (National Weather Service) for U.S. alerts/forecasts
"""

import asyncio
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Weather Server")

# API endpoints
OPEN_METEO_GEOCODE = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"
NWS_API_BASE = "https://api.weather.gov"

# ---------- Helpers ----------
async def fetch_json(url: str, params: dict | None = None, headers: dict | None = None):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        return {"error": str(e)}

# ---------- Tools ----------
@mcp.tool()
async def get_weather(city: str) -> str:
    """Get simple current weather for a city (worldwide).
    
    Args:
        city: City name (e.g., "London", "New York")
    """
    # Step 1: Geocode city → lat/lon
    geo = await fetch_json(OPEN_METEO_GEOCODE, {"name": city, "count": 1})
    if "results" not in geo or not geo["results"]:
        return f"Could not find location for {city}."
    loc = geo["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # Step 2: Fetch current weather
    weather = await fetch_json(OPEN_METEO_FORECAST, {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    if "current_weather" not in weather:
        return f"Could not fetch weather for {city}."

    cw = weather["current_weather"]
    return f"Weather in {city}: {cw['temperature']}°C, wind {cw['windspeed']} km/h"

@mcp.tool()
async def get_forecast(city: str) -> str:
    """Get a 3-day forecast for a city."""
    geo = await fetch_json(OPEN_METEO_GEOCODE, {"name": city, "count": 1})
    if "results" not in geo or not geo["results"]:
        return f"Could not find location for {city}."
    loc = geo["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    forecast = await fetch_json(OPEN_METEO_FORECAST, {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "forecast_days": 3,
        "timezone": "auto"
    })
    if "daily" not in forecast:
        return f"Could not fetch forecast for {city}."

    days = forecast["daily"]
    lines = []
    for i in range(3):
        lines.append(
            f"{days['time'][i]}: {days['temperature_2m_min'][i]}–{days['temperature_2m_max'][i]}°C, "
            f"precip {days['precipitation_sum'][i]}mm"
        )
    return "\n".join(lines)

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get active weather alerts for a U.S. state (NWS only).
    
    Args:
        state: Two-letter US state code (e.g., CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    alerts = await fetch_json(url, headers={"User-Agent": "WeatherMCP/1.0 (email@example.com)"})
    
    if "features" not in alerts or not alerts["features"]:
        return f"No active alerts for {state}."

    results = []
    for feature in alerts["features"][:3]:  # show top 3
        props = feature["properties"]
        results.append(
            f"Event: {props.get('event')}\n"
            f"Severity: {props.get('severity')}\n"
            f"Area: {props.get('areaDesc')}\n"
            f"Instruction: {props.get('instruction')}\n"
        )
    return "\n---\n".join(results)

# ---------- Run ----------
if __name__ == "__main__":
    mcp.run()
