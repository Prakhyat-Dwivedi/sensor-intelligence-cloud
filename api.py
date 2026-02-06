from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

# ==========================
# CORS (phone + web allowed)
# ==========================
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
    "device_id": None,
    "timestamp": None,
    "battery": None,
    "wifi": None,
    "mobile": None
}

# ==========================
# ROOT (health check)
# ==========================
@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "version": "1.1",
        "status": "running",
        "last_update": LATEST_DATA["timestamp"]
    }

# ==========================
# INGEST ENDPOINT
# ==========================
@app.post("/ingest")
def ingest(data: dict):
    LATEST_DATA["device_id"] = data.get("device_id")
    LATEST_DATA["battery"] = data.get("battery")
    LATEST_DATA["wifi"] = data.get("wifi")
    LATEST_DATA["mobile"] = data.get("mobile")
    LATEST_DATA["timestamp"] = time.time()

    return {
        "status": "ingested",
        "device_id": LATEST_DATA["device_id"],
        "timestamp": LATEST_DATA["timestamp"]
    }

# ==========================
# BATTERY API
# ==========================
@app.get("/battery")
def battery():
    if not LATEST_DATA["battery"]:
        return {"error": "Battery data not available"}
    return {
        "device_id": LATEST_DATA["device_id"],
        "timestamp": LATEST_DATA["timestamp"],
        "battery": LATEST_DATA["battery"]
    }

# ==========================
# WIFI API
# ==========================
@app.get("/wifi")
def wifi():
    if not LATEST_DATA["wifi"]:
        return {"error": "WiFi data not available"}
    return {
        "device_id": LATEST_DATA["device_id"],
        "timestamp": LATEST_DATA["timestamp"],
        "wifi": LATEST_DATA["wifi"]
    }

# ==========================
# MOBILE NETWORK API
# ==========================
@app.get("/mobile")
def mobile():
    if not LATEST_DATA["mobile"]:
        return {"error": "Mobile network data not available"}
    return {
        "device_id": LATEST_DATA["device_id"],
        "timestamp": LATEST_DATA["timestamp"],
        "mobile": LATEST_DATA["mobile"]
    }

# ==========================
# COMBINED STATUS API
# ==========================
@app.get("/status")
def status():
    return {
        "device_id": LATEST_DATA["device_id"],
        "timestamp": LATEST_DATA["timestamp"],
        "battery": LATEST_DATA["battery"],
        "wifi": LATEST_DATA["wifi"],
        "mobile": LATEST_DATA["mobile"]
    }
