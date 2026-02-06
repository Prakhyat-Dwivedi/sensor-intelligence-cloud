from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# DEVICE STORE
# device_id -> latest data
# ==========================
DEVICES = {}

# ==========================
# ROOT
# ==========================
@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "status": "running"
    }

# ==========================
# INGEST (Laptop / Android)
# ==========================
@app.post("/ingest")
def ingest(data: dict):
    device_id = data.get("device_id", "unknown")

    DEVICES[device_id] = {
        "battery": data.get("battery"),
        "wifi": data.get("wifi"),
        "mobile": data.get("mobile"),
        "timestamp": time.time()
    }

    return {
        "status": "ingested",
        "device_id": device_id
    }

# ==========================
# BATTERY
# ==========================
@app.get("/battery")
def battery(device_id: str):
    data = DEVICES.get(device_id)

    if not data or not data.get("battery"):
        return {"error": "Battery data not available"}

    return data["battery"]

# ==========================
# WIFI
# ==========================
@app.get("/wifi")
def wifi(device_id: str):
    data = DEVICES.get(device_id)

    if not data or not data.get("wifi"):
        return {"error": "WiFi data not available"}

    return data["wifi"]

# ==========================
# MOBILE NETWORK
# ==========================
@app.get("/mobile")
def mobile(device_id: str):
    data = DEVICES.get(device_id)

    if not data or not data.get("mobile"):
        return {"error": "Mobile network data not available"}

    return data["mobile"]
