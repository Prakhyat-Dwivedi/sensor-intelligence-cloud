from fastapi import FastAPI, Query
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
        "status": "running",
        "devices": list(DEVICES.keys())
    }

# ==========================
# INGEST (Android / Laptop)
# ==========================
@app.post("/ingest")
def ingest(data: dict):
    device_id = data.get("device_id") or "unknown"

    DEVICES[device_id] = {
        "battery": data.get("battery"),
        "wifi": data.get("wifi"),
        "mobile": data.get("mobile"),   # mobile speed support
        "timestamp": time.time()
    }

    return {
        "status": "ingested",
        "device_id": device_id
    }

# ==========================
# INTERNAL HELPER
# ==========================
def get_device_data(device_id: str):
    return DEVICES.get(device_id)

# ==========================
# BATTERY
# ==========================
@app.get("/battery")
def battery(device_id: str = Query("laptop")):
    data = get_device_data(device_id)

    if not data or not data.get("battery"):
        return {
            "available": False,
            "end_percent": 0,
            "charging": False
        }

    return data["battery"]

# ==========================
# WIFI
# ==========================
@app.get("/wifi")
def wifi(device_id: str = Query("laptop")):
    data = get_device_data(device_id)

    if not data or not data.get("wifi"):
        return {
            "connected": False,
            "signal_percent": 0,
            "ssid": "N/A"
        }

    return data["wifi"]

# ==========================
# MOBILE NETWORK (Speed Test)
# ==========================
@app.get("/mobile")
def mobile(device_id: str = Query("laptop")):
    data = get_device_data(device_id)

    if not data or not data.get("mobile"):
        return {
            "connected": False,
            "network_type": "N/A",
            "download_mbps": 0,
            "upload_mbps": 0,
            "latency_ms": 0
        }

    return data["mobile"]
