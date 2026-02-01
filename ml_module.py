import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyModel:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05)

    def train(self, samples):
        self.model.fit(np.array(samples).reshape(-1, 1))

    def score(self, value):
        return -self.model.decision_function([[value]])[0]