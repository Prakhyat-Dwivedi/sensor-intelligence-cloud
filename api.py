from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Sentinel – Sensor Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# DEVICE STORE
# ==========================
DEVICES = {}

@app.get("/")
def root():
    return {"status": "running"}

# ==========================
# INGEST
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

    return {"status": "ingested", "device_id": device_id}


# ==========================
# BATTERY (FIXED)
# ==========================
@app.get("/battery")
def battery(device_id: str = Query(...)):
    data = DEVICES.get(device_id)

    if not data or not data.get("battery"):
        return {"error": "Battery data not available"}

    return data["battery"]


# ==========================
# WIFI (FIXED)
# ==========================
@app.get("/wifi")
def wifi(device_id: str = Query(...)):
    data = DEVICES.get(device_id)

    if not data or not data.get("wifi"):
        return {"error": "WiFi data not available"}

    return data["wifi"]


# ==========================
# MOBILE
# ==========================
@app.get("/mobile")
def mobile(device_id: str = Query(...)):
    data = DEVICES.get(device_id)

    if not data or not data.get("mobile"):
        return {"error": "Mobile data not available"}

    return data["mobile"]
