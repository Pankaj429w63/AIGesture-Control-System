import cv2
import numpy as np
from typing import List, Tuple, Optional
import os
import logging

try:
    import mediapipe as mp
    # Try multiple ways to access solutions
    try:
        _mp_hands = mp.solutions.hands
        _HAS_SOLUTIONS = True
    except AttributeError:
        # Try alternate access path
        try:
            from mediapipe.python.solutions import hands
            _mp_hands = hands
            _HAS_SOLUTIONS = True
        except ImportError:
            _HAS_SOLUTIONS = False
except Exception:
    _HAS_SOLUTIONS = False

_HAS_TASKS = False
try:
    # Tasks API
    from mediapipe.tasks.python.vision import hand_landmarker as _hand_landmarker_module
    from mediapipe.tasks.python.vision.core import image as _mp_image
    from mediapipe.tasks.python.core import base_options as _base_options
    _HAS_TASKS = True
except Exception:
    _HAS_TASKS = _HAS_TASKS or False


class SimpleHandDetector:
    """Fallback simple hand detector using OpenCV when MediaPipe is unavailable.
    
    Uses skin color detection to find hand regions and generates synthetic
    landmarks for compatibility with the rest of the system.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Using SimpleHandDetector (fallback) for hand detection")
        
    def detect(self, frame: np.ndarray) -> Optional[List[np.ndarray]]:
        """Detect hands using skin color segmentation."""
        if frame is None or frame.size == 0:
            return None
            
        # Convert to HSV for better skin detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create skin mask
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find largest contour (likely the hand)
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        if area < 500:  # Minimum hand size
            return None
        
        # Get bounding box of hand
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Generate synthetic landmarks (21 points for MediaPipe compatibility)
        # This is simplified - we'll place points around the hand region
        landmarks = self._generate_landmarks_from_region(x, y, w, h, frame.shape)
        
        return [landmarks] if landmarks is not None else None
    
    def _generate_landmarks_from_region(self, x: int, y: int, w: int, h: int, 
                                       frame_shape: Tuple[int, int, int]) -> Optional[np.ndarray]:
        """Generate synthetic 21 landmarks from hand bounding box."""
        landmarks = []
        
        # Hand center
        cx, cy = x + w // 2, y + h // 2
        
        # Generate 21 landmarks in a pattern (0-20 indices)
        # Wrist (0)
        landmarks.append([x + w // 2, y + h - 10, 0.8])
        
        # Thumb (1-4)
        landmarks.append([x + 10, y + h // 2, 0.8])
        landmarks.append([x + 15, y + h // 2 - 20, 0.8])
        landmarks.append([x + 20, y + h // 2 - 40, 0.8])
        landmarks.append([x + 25, y + h // 2 - 60, 0.8])
        
        # Index finger (5-8)
        landmarks.append([x + w // 4, y + 20, 0.8])
        landmarks.append([x + w // 4, y, 0.8])
        landmarks.append([x + w // 4 + 5, y - 30, 0.8])
        landmarks.append([x + w // 4 + 10, y - 60, 0.8])
        
        # Middle finger (9-12)
        landmarks.append([x + w // 2, y + 15, 0.8])
        landmarks.append([x + w // 2, y - 10, 0.8])
        landmarks.append([x + w // 2, y - 40, 0.8])
        landmarks.append([x + w // 2, y - 70, 0.8])
        
        # Ring finger (13-16)
        landmarks.append([x + 3 * w // 4, y + 20, 0.8])
        landmarks.append([x + 3 * w // 4, y, 0.8])
        landmarks.append([x + 3 * w // 4 - 5, y - 30, 0.8])
        landmarks.append([x + 3 * w // 4 - 10, y - 60, 0.8])
        
        # Pinky finger (17-20)
        landmarks.append([x + w - 10, y + 30, 0.8])
        landmarks.append([x + w - 15, y + 10, 0.8])
        landmarks.append([x + w - 20, y - 20, 0.8])
        landmarks.append([x + w - 25, y - 50, 0.8])
        
        # Normalize to 0-1 range
        landmarks = np.array(landmarks)
        landmarks[:, 0] /= frame_shape[1]
        landmarks[:, 1] /= frame_shape[0]
        
        return landmarks


class HandTracker:
    """Hand tracker with compatibility for MediaPipe Solutions and Tasks APIs.

    By default tries to use `mp.solutions.hands` (legacy API). If that's not
    available and the Tasks API is present, it will attempt to use the Tasks
    `HandLandmarker` instead. For the Tasks API a `model_path` pointing to a
    `hand_landmarker.task` bundle or model file is required unless you have a
    pre-bundled model available in your environment.
    """

    def __init__(
        self,
        max_num_hands: int = 2,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
        model_path: Optional[str] = None,
    ):
        self._mode = None
        self._solutions_hands = None
        self._tasks_landmarker = None

        # PREFER legacy API (no external model required)
        if _HAS_SOLUTIONS:
            try:
                self._mode = "solutions"
                self._solutions_hands = _mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=max_num_hands,
                    min_detection_confidence=detection_confidence,
                    min_tracking_confidence=tracking_confidence,
                )
                logging.getLogger(__name__).info("HandTracker: using legacy mp.solutions.hands API")
                return
            except Exception as e:
                logging.getLogger(__name__).warning(
                    "Failed to initialize MediaPipe solutions.hands: %s. Trying Tasks API...", e
                )
                self._mode = None
                self._solutions_hands = None

        if _HAS_TASKS:
            # Tasks API requires a model bundle path or buffer. Prefer explicit
            # model_path provided by caller or environment variable.
            mp_model = model_path or os.environ.get("MP_HAND_LANDMARKER_MODEL")
            if mp_model and os.path.exists(mp_model):
                try:
                    options = _hand_landmarker_module.HandLandmarkerOptions(
                        base_options=_base_options.BaseOptions(model_asset_path=mp_model),
                        running_mode=_hand_landmarker_module._RunningMode.IMAGE,
                        num_hands=max_num_hands,
                    )
                    self._tasks_landmarker = _hand_landmarker_module.HandLandmarker.create_from_options(options)
                    self._mode = "tasks"
                    logging.getLogger(__name__).info("HandTracker: using MediaPipe Tasks API with model %s", mp_model)
                    return
                except Exception as e:
                    logging.getLogger(__name__).warning(
                        "Failed to initialize MediaPipe Tasks HandLandmarker: %s", e
                    )
            else:
                logging.getLogger(__name__).warning(
                    "Tasks API requires model_path parameter or MP_HAND_LANDMARKER_MODEL env var. Skipping Tasks API."
                )

        # Fallback: use simple hand detector
        logging.getLogger(__name__).warning(
            "No MediaPipe API available. Using fallback SimpleHandDetector."
        )
        self._simple_detector = SimpleHandDetector()
        self._mode = "simple"

    def process_frame(self, frame) -> List[List[Tuple[float, float, float]]]:
        """Return list of hands; each hand is list of (x,y,z) tuples for 21 landmarks."""
        if self._mode == "solutions":
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self._solutions_hands.process(img_rgb)
            hands = []
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    landmarks = [(lm.x, lm.y, lm.z) for lm in handLms.landmark]
                    hands.append(landmarks)
            return hands

        if self._mode == "tasks":
            # Create a MediaPipe Tasks Image from numpy array (RGB expected)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # The Image constructor expects (image_format, numpy_array)
            mp_image = _mp_image.Image(_mp_image.ImageFormat.SRGB, img_rgb)
            result = self._tasks_landmarker.detect(mp_image)
            hands = []
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    landmarks = []
                    for lm in hand_landmarks:
                        # Normalized landmark: x,y are relative coordinates
                        landmarks.append((lm.x, lm.y, lm.z))
                    hands.append(landmarks)
            return hands

        if self._mode == "simple":
            # Use simple hand detector
            detected = self._simple_detector.detect(frame)
            if detected:
                hands = []
                for landmarks_array in detected:
                    landmarks = [(lm[0], lm[1], lm[2]) for lm in landmarks_array]
                    hands.append(landmarks)
                return hands
            return []

        # When disabled, return empty detections so the app keeps running.
        if self._mode == "disabled":
            return []
        return []
