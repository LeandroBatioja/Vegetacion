import requests
from io import BytesIO

GIBS_URL = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"

def fetch_gibs_image(bbox: str, date: str, layer="MODIS_Terra_CorrectedReflectance_TrueColor", width=512, height=512):
    """
    Devuelve la imagen satelital de la NASA GIBS
    """
    west, south, east, north = map(float, bbox.split(","))
    params = {
        "SERVICE": "WMS",
        "REQUEST": "GetMap",
        "VERSION": "1.3.0",
        "LAYERS": layer,
        "STYLES": "",
        "FORMAT": "image/png",
        "TRANSPARENT": "TRUE",
        "HEIGHT": height,
        "WIDTH": width,
        "CRS": "EPSG:4326",
        "BBOX": f"{south},{west},{north},{east}",
        "TIME": date
    }

    try:
        response = requests.get(GIBS_URL, params=params, timeout=120)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.RequestException as e:
        print(f"Error fetching GIBS image: {e}")
        return None
