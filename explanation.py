EXPLANATIONS = {
    "HEALTHY": "Sensor operating within calibrated limits.",
    "DRIFTING": "Sustained deviation detected from baseline.",
    "NOISY": "High variance indicates noisy signal.",
    "FAULTY": "Deviation exceeds fault threshold."
}

def explain(status):
    return EXPLANATIONS.get(status, "Unknown state")