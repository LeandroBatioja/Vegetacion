from app.services import ndvi_service

def test_tile_url():
    url = ndvi_service.get_tile_url(0, 0, "2025-09-17")
    assert "gibs.earthdata.nasa.gov" in url
