from typing import List, Tuple
import numpy as np

def landmarks_to_vector(landmarks: List[Tuple[float, float, float]]) -> np.ndarray:
    """Convert 21 (x,y,z) landmarks to a 63-length numpy array."""
    if len(landmarks) != 21:
        raise ValueError("Expected 21 landmarks per hand")
    arr = np.array(landmarks).reshape(-1)
    return arr
