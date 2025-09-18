import requests

BACKEND_URL = "http://127.0.0.1:8000"  # Ajusta si tu backend corre en otra IP/puerto

def get_ndvi(bbox, start, end):
    url = f"{BACKEND_URL}/ndvi/area"
    params = {"bbox": bbox, "start": start, "end": end}
    try:
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json().get("ndvi", {})
    except Exception as e:
        return {"error": str(e)}

def get_flowering(bbox, start, end, ndvi_threshold):
    url = f"{BACKEND_URL}/detect/flower"
    params = {"bbox": bbox, "start": start, "end": end, "ndvi_threshold": ndvi_threshold}
    try:
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        return resp.json().get("flowering", {})
    except Exception as e:
        return {"error": str(e)}
