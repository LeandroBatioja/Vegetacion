from app.services.ndvi_service import get_ndvi_area

def detect_flowering(bbox: str, start: str, end: str, ndvi_threshold: float):
    """
    Retorna áreas donde NDVI supera threshold, simulando floración
    """
    ndvi_data = get_ndvi_area(bbox, start, end)
    
    # Ejemplo simple: filtrar pixeles NDVI > ndvi_threshold
    flowering_areas = [
        point for point in ndvi_data.get("values", []) 
        if point.get("ndvi", 0) >= ndvi_threshold
    ]
    return flowering_areas
