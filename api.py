from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

# --------------------------
# CORS (Frontend / Phone)
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# IN-MEMORY STATE (SAFE)
# --------------------------
LATEST_DATA = {
    "battery": None,
    "wifi": None,
    "timestamp": None
}

# --------------------------
# ROOT (Health Check)
# --------------------------
@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "version": "1.0",
        "status": "running"
    }

# --------------------------
# INGEST (DEVICE AGENT)
# --------------------------
@app.post("/ingest")
def ingest(data: dict):
    # Update battery ONLY if present
    if data.get("battery") is not None:
        LATEST_DATA["battery"] = data["battery"]

    # Update wifi ONLY if present
    if data.get("wifi") is not None:
        LATEST_DATA["wifi"] = data["wifi"]

    LATEST_DATA["timestamp"] = time.time()

    return {
        "status": "ingested",
        "timestamp": LATEST_DATA["timestamp"]
    }

# --------------------------
# BATTERY ENDPOINT
# --------------------------
@app.get("/battery")
def battery():
    if LATEST_DATA["battery"] is None:
        return {
            "available": False,
            "message": "Waiting for device battery data"
        }
    return LATEST_DATA["battery"]

# --------------------------
# WIFI ENDPOINT
# --------------------------
@app.get("/wifi")
def wifi():
    if LATEST_DATA["wifi"] is None:
        return {
            "connected": False,
            "message": "Waiting for device WiFi data"
        }
    return LATEST_DATA["wifi"]
