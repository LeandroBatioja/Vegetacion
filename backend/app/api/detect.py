from fastapi import APIRouter, Query
from app.services.bloom_service import detect_flowering

router = APIRouter()

@router.get("/flower")
def flower_area(
    bbox: str = Query(..., description="lon_min,lat_min,lon_max,lat_max"),
    start: str = Query(..., description="YYYY-MM-DD"),
    end: str = Query(..., description="YYYY-MM-DD"),
    ndvi_threshold: float = Query(0.35)
):
    try:
        data = detect_flowering(bbox, start, end, ndvi_threshold)
        return {"flowering": data}
    except Exception as e:
        return {"error": str(e)}
