# app/services/flower_service.py

def detect_flower(ndvi_points, threshold=0.35):
    """
    Detecta puntos con NDVI mayor que threshold como floración.
    """
    flowers = [p for p in ndvi_points if p["ndvi"] >= threshold]
    bloom_percent = round(len(flowers)/len(ndvi_points)*100, 2) if ndvi_points else 0
    return {"flowers": flowers, "bloom_percent": bloom_percent}
