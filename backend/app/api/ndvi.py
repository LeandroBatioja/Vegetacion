# app/api/ndvi.py
from fastapi import APIRouter, Query
from app.services.ndvi_service import get_ndvi_area

router = APIRouter(prefix="/api/ndvi", tags=["NDVI"])

@router.get("/area")
def ndvi_area(
    bbox: str = Query(..., description="min_lon,min_lat,max_lon,max_lat"),
    start: str = Query(..., description="Fecha inicio YYYY-MM-DD"),
    end: str = Query(..., description="Fecha fin YYYY-MM-DD")
):
    bbox_list = list(map(float, bbox.split(",")))
    data = get_ndvi_area(bbox_list, start, end)
    return data
