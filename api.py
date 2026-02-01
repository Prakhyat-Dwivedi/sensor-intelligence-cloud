from fastapi import FastAPI
from pydantic import BaseModel

from analyzer import analyze
from confidence import compute_confidence
from explanation import explain
from ml_anomaly import MLAnomalyDetector
from health_index import compute_health_index, get_severity


app = FastAPI(title="Sensor Health API")

@app.get("/")
def root():
    return {
        "project": "Sentinel – Sensor Intelligence",
        "version": "1.0",
        "description": "Calibration-based multi-sensor health monitoring API",
        "status": "running"
    }


# =========================
# REQUEST MODEL
# =========================
class SensorRequest(BaseModel):
    sensor_type:str #battery|wifi| arduino
    window: list[float]
    base_mean: float
    base_var: float
    warn: float
    fault: float


# =========================
# ML SETUP (trained once)
# =========================
ml_detector = MLAnomalyDetector()
ml_detector.train([48, 49, 50, 51, 49, 50, 50, 49, 51])


# =========================
# API ENDPOINT
# =========================
@app.post("/analyze")
def analyze_sensor(req: SensorRequest):

    # --- Core analysis ---
    status = analyze(req.window, req.base_mean, req.base_var)

    avg = sum(req.window) / len(req.window)
    deviation = abs(avg - req.base_mean)

    confidence = compute_confidence(deviation, req.warn, req.fault)
    health_index = compute_health_index(confidence)
    severity = get_severity(status)

    ml_score = ml_detector.score(req.window)

    return {
        "status": status,
        "severity": severity,
        "confidence": round(confidence, 2),
        "health_index": round(health_index, 2),
        "ml_anomaly_score": round(ml_score, 3),
        "explanation": explain(status),
        "window_avg": round(avg, 2)
    }