from fastapi import FastAPI, Request
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

# ==========================
# ROOT
# ==========================
@app.get("/")
def root():
    return {"status": "running"}

# ==========================
# INGEST (ANDROID SENDS DATA)
# ==========================
@app.post("/ingest")
def ingest(data: dict):
    device_id = data.get("device_id", "unknown")

    DEVICES[device_id] = {
        "battery": data.get("battery"),
        "wifi": data.get("wifi"),
        "timestamp": time.time()
    }

    return {"status": "ok", "device": device_id}

# ==========================
# AUTO DEVICE DETECTION
# ==========================
def resolve_device(request: Request):
    ua = request.headers.get("user-agent", "").lower()
    if "android" in ua:
        return "android"
    return "laptop"

# ==========================
# BATTERY
# ==========================
@app.get("/battery")
def battery(request: Request):
    device = resolve_device(request)
    data = DEVICES.get(device)

    if not data or not data["battery"]:
        return {"error": "Battery data not available"}

    return data["battery"]

# ==========================
# WIFI
# ==========================
@app.get("/wifi")
def wifi(request: Request):
    device = resolve_device(request)
    data = DEVICES.get(device)

    if not data or not data["wifi"]:
        return {"error": "WiFi data not available"}

    return data["wifi"]
