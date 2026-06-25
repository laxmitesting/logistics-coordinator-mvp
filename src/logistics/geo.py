import os
from typing import Any, Dict, List

import requests

def ors_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("ORS_API_KEY")
    if not api_key:
        return {"ok": False, "error": "Missing ORS_API_KEY environment variable"}

    url = f"https://api.openrouteservice.org{path}"
    response = requests.get(url, params={**params, "api_key": api_key}, timeout=30)
    
    # Optional: You can make network errors resilient too instead of crashing!
    if not response.ok:
        return {"ok": False, "error": f"API HTTP Error: {response.status_code}"}
        
    return response.json()


def ors_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("ORS_API_KEY")
    if not api_key:
        return {"ok": False, "error": "Missing ORS_API_KEY environment variable"}

    url = f"https://api.openrouteservice.org{path}"
    response = requests.post(
        url,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    
    if not response.ok:
        return {"ok": False, "error": f"API HTTP Error: {response.status_code}"}
        
    return response.json()

# ==========================================
# GEO LOGIC (Passes errors up smoothly)
# ==========================================

def geocode_address(address: str) -> Dict[str, Any]:
    data = ors_get("/geocode/search", {"text": address, "size": 1})
    
    # If the API key was missing, data is an error dictionary. Pass it up!
    if data.get("ok") is False:
        return data
        
    features = data.get("features", [])
    if not features:
        return {"ok": False, "error": f"No geocoding result for {address}"}
        
    feature = features[0]
    lon, lat = feature["geometry"]["coordinates"]
    return {
        "ok": True,
        "address": address,
        "label": feature["properties"].get("label", address),
        "lon": lon,
        "lat": lat,
    }


def get_matrix(locations: List[List[float]], profile: str = "driving-car") -> Dict[str, Any]:
    data = ors_post(
        f"/v2/matrix/{profile}",
        {"locations": locations, "metrics": ["distance", "duration"]},
    )
    
    if data.get("ok") is False:
        return data
        
    return {
        "ok": True,
        "distances": data.get("distances", []),
        "durations": data.get("durations", []),
    }


def get_directions(coordinates: List[List[float]], profile: str = "driving-car") -> Dict[str, Any]:
    data = ors_post(
        f"/v2/directions/{profile}/geojson",
        {"coordinates": coordinates, "instructions": True},
    )
    
    if data.get("ok") is False:
        return data
        
    features = data.get("features", [])
    if not features:
        return {"ok": False, "error": "No route returned"}
        
    summary = features[0].get("properties", {}).get("summary", {})
    return {
        "ok": True,
        "distance_m": summary.get("distance"),
        "duration_s": summary.get("duration"),
    }