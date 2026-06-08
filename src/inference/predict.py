import joblib
import numpy as np
from typing import Tuple
from src.utils.config_loader import load_config
import logging

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, model_path: str = None):
        cfg = load_config()
        self.path = model_path or cfg["model"]["save_path"]
        try:
            data = joblib.load(self.path)
            self.model = data.get("model") if isinstance(data, dict) else data
            self.scaler = data.get("scaler") if isinstance(data, dict) else None
            self.conf_threshold = cfg["model"].get("confidence_threshold", 0.5)
        except Exception as e:
            logger.warning("Failed to load model from %s: %s", self.path, e)
            self.model = None
            self.scaler = None
            self.conf_threshold = cfg["model"].get("confidence_threshold", 0.5)

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        x = features.reshape(1, -1)
        if self.scaler is not None:
            x = self.scaler.transform(x)
        if self.model is None:
            return "__no_model__", 0.0
        try:
            proba = self.model.predict_proba(x)[0]
            idx = int(proba.argmax())
            label = self.model.classes_[idx]
            conf = float(proba[idx])
        except Exception:
            label = self.model.predict(x)[0]
            conf = 1.0
        return label, conf
