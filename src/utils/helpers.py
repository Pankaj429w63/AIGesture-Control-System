from typing import List, Tuple
import numpy as np

def flatten_landmarks(landmarks: List[Tuple[float, float, float]]) -> np.ndarray:
    """Convert list of (x,y,z) landmarks to flat numpy array of length 63."""
    arr = np.array(landmarks).flatten()
    return arr
