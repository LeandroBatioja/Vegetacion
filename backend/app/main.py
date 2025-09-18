from fastapi import FastAPI
from app.api import ndvi, detect

app = FastAPI(title="NDVI & Flowering API")

app.include_router(ndvi.router, prefix="/ndvi")
app.include_router(detect.router, prefix="/detect")
