from app.clients.appeears_client import fetch_ndvi_from_nasa

def get_ndvi_area(bbox: str, start: str, end: str):
    """
    Retorna datos NDVI de la NASA para un área y rango de fechas
    """
    data = fetch_ndvi_from_nasa(bbox, start, end)
    # Aquí podrías procesar JSON y convertirlo en una matriz o dataframe
    return data
