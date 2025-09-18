from typing import Tuple

def parse_bbox(bbox: str) -> Tuple[float, float, float, float]:
    """
    Convierte un string bbox '-78.6,-0.2,-78.5,0.0' en tupla de floats
    """
    try:
        west, south, east, north = map(float, bbox.split(","))
        return west, south, east, north
    except ValueError:
        raise ValueError("BBox debe tener el formato 'west,south,east,north'")

def validate_dates(start: str, end: str):
    """
    Validación básica de fechas YYYY-MM-DD
    """
    import datetime
    try:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha de fin")
        return start_date, end_date
    except ValueError:
        raise ValueError("Las fechas deben tener formato YYYY-MM-DD")
