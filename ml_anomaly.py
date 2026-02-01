import numpy as np
from sklearn.ensemble import IsolationForest

class MLAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        self.trained = False

    def train(self, data):
        """
        data: list of normal sensor values (calibration data)
        """
        X = np.array(data).reshape(-1, 1)
        self.model.fit(X)
        self.trained = True

    def score(self, window):
        """
        Returns anomaly score for a window
        Higher = more anomalous
        """
        if not self.trained:
            return None

        X = np.array(window).reshape(-1, 1)
        scores = -self.model.decision_function(X)
        return round(float(scores.mean()), 3)