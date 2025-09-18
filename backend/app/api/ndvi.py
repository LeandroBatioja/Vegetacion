from fastapi import APIRouter, Query
from app.services.ndvi_service import get_ndvi_area

router = APIRouter()

@router.get("/area")
def ndvi_area(
    bbox: str = Query(..., description="lon_min,lat_min,lon_max,lat_max"),
    start: str = Query(..., description="YYYY-MM-DD"),
    end: str = Query(..., description="YYYY-MM-DD")
):
    try:
        data = get_ndvi_area(bbox, start, end)
        return {"ndvi": data}
    except Exception as e:
        return {"error": str(e)}
