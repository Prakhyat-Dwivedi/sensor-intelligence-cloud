def compute_health_index(confidence: float) -> float:
    """
    Converts confidence (risk) into health index.
    Higher is better.
    """
    return round(max(0, 100 - confidence), 2)


def get_severity(status: str) -> str:
    """
    Maps health status to severity level.
    """
    if status == "HEALTHY":
        return "INFO"
    elif status in ("NOISY", "DRIFTING"):
        return "WARNING"
    elif status == "FAULTY":
        return "CRITICAL"
    else:
        return "UNKNOWN"