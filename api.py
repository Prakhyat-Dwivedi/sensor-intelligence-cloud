from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LATEST_DATA = {}

@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "version": "1.0",
        "status": "running"
    }

@app.post("/ingest")
def ingest(data: dict):
    device_id = data.get("device_id", "default")
    LATEST_DATA[device_id] = {
        "battery": data.get("battery"),
        "wifi": data.get("wifi"),
        "timestamp": time.time()
    }
    return {"status": "ingested"}

@app.get("/battery")
def battery(device_id: str = "default"):
    if device_id not in LATEST_DATA:
        return {"available": False}

    battery = LATEST_DATA[device_id]["battery"]
    if not battery or not battery.get("available"):
        return {"available": False}

    return {
        "available": True,
        "percent": battery["percent"],
        "charging": battery["charging"]
    }

@app.get("/wifi")
def wifi(device_id: str = "default"):
    if device_id not in LATEST_DATA:
        return {"connected": False}

    return LATEST_DATA[device_id]["wifi"]
