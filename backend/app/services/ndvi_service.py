# app/services/ndvi_service.py
from datetime import datetime, timedelta
import random

def get_ndvi_area(bbox, start_date, end_date):
    """
    Simula la obtención de datos NDVI para un bounding box y rango de fechas.
    bbox = [min_lon, min_lat, max_lon, max_lat]
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = (end - start).days + 1

    points = []
    time_series = {}

    # Generamos datos aleatorios
    for i in range(50):  # 50 puntos aleatorios
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        ndvi_val = round(random.uniform(0, 1), 2)
        points.append({"lat": lat, "lon": lon, "ndvi": ndvi_val})

    for d in range(delta):
        day = (start + timedelta(days=d)).strftime("%Y-%m-%d")
        ts_points = []
        for p in points:
            ndvi_val = round(random.uniform(0, 1), 2)
            ts_points.append({"lat": p["lat"], "lon": p["lon"], "ndvi": ndvi_val})
        time_series[day] = ts_points

    avg_ndvi = round(sum(p["ndvi"] for p in points)/len(points), 2) if points else 0

    return {"points": points, "time_series": time_series, "average_ndvi": avg_ndvi}
