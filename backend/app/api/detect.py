# app/api/detect.py
from fastapi import APIRouter, Query
from app.services.ndvi_service import get_ndvi_area
from app.services.flower_service import detect_flower

router = APIRouter(prefix="/api/detect", tags=["Floración"])

@router.get("/flower")
def flower_detection(
    bbox: str = Query(..., description="min_lon,min_lat,max_lon,max_lat"),
    start: str = Query(..., description="Fecha inicio YYYY-MM-DD"),
    end: str = Query(..., description="Fecha fin YYYY-MM-DD"),
    ndvi_threshold: float = Query(0.35, description="Umbral NDVI")
):
    bbox_list = list(map(float, bbox.split(",")))
    ndvi_data = get_ndvi_area(bbox_list, start, end)
    flowers = detect_flower(ndvi_data["points"], ndvi_threshold)
    return flowers
