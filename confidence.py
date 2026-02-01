def compute_confidence(deviation, warn, fault):
    if deviation < warn:
        return 30 + (deviation / warn) * 30
    elif deviation < fault:
        return 60 + (deviation - warn) / (fault - warn) * 30
    else:
        return min(100, 90 + deviation)