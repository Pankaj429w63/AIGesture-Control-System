import joblib
import numpy as np
from typing import Optional, Tuple

class GestureClassifier:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """Return (label, confidence)"""
        proba = None
        try:
            proba = self.model.predict_proba([features])[0]
            idx = int(proba.argmax())
            label = self.model.classes_[idx]
            confidence = float(proba[idx])
        except Exception:
            pred = self.model.predict([features])[0]
            label = pred
            confidence = 1.0
        return label, confidence
