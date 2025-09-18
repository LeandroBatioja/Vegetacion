import requests
from app.utils.config import get_settings

settings = get_settings()

def fetch_ndvi_from_nasa(bbox, start, end):
    """
    bbox = "lon_min,lat_min,lon_max,lat_max"
    start, end = "YYYY-MM-DD"
    """
    url = f"https://appeears.earthdatacloud.nasa.gov/api/ndvi"
    params = {
        "bbox": bbox,
        "start": start,
        "end": end
    }
    headers = {
        "Authorization": f"Bearer {settings.earthdata_token}"
    }

    response = requests.get(url, params=params, headers=headers, timeout=60)
    response.raise_for_status()  # Lanza error si no es 200
    return response.json()
