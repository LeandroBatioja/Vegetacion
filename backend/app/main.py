# backend/app/main.py
from fastapi import FastAPI
from backend.app.api import ndvi, detect  

app = FastAPI(title="API Vegetación NASA")

app.include_router(ndvi.router)
app.include_router(detect.router)
