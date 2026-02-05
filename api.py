from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

# Allow frontend / phone access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# IN-MEMORY STORE
# ==========================
LATEST_DATA = {
    "battery": None,
    "wifi": None,
    "timestamp": None,
    "device_id": None
}

# ==========================
# ROOT (health check)
# ==========================
@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "version": "1.0",
        "status": "running"
    }

# ==========================
# INGEST ENDPOINT
# ==========================
@app.post("/ingest")
def ingest(data: dict):
    LATEST_DATA["battery"] = data.get("battery")
    LATEST_DATA["wifi"] = data.get("wifi")
    LATEST_DATA["device_id"] = data.get("device_id")
    LATEST_DATA["timestamp"] = time.time()

    return {
        "status": "ingested",
        "device_id": LATEST_DATA["device_id"]
    }

# ==========================
# BATTERY API
# ==========================
@app.get("/battery")
def battery():
    if not LATEST_DATA["battery"]:
        return {"error": "Battery data not available"}
    return LATEST_DATA["battery"]

# ==========================
# WIFI API
# ==========================
@app.get("/wifi")
def wifi():
    if not LATEST_DATA["wifi"]:
        return {"error": "WiFi data not available"}
    return LATEST_DATA["wifi"]
