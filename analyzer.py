def analyze(window, base_mean, base_var,
            drift_thresh=2,
            noise_factor=4,
            fault_limit=200):

    if not window:
        return "NO_DATA"

    avg = sum(window) / len(window)
    var = sum((v - avg) ** 2 for v in window) / len(window)

    if max(abs(v) for v in window) > fault_limit:
        return "FAULTY"

    if abs(avg - base_mean) > drift_thresh:
        return "DRIFTING"

    if var > base_var * noise_factor:
        return "NOISY"

    return "HEALTHY"