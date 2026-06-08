# System Architecture

This project follows a modular architecture: detection, preprocessing, training, inference, controls, and authentication are separated into packages under `src/`.

Key components:
- `gesture_detection`: MediaPipe wrappers and feature extraction
- `training`: model training and selection
- `inference`: runtime model loader and prediction
- `controls`: platform integrations (volume/brightness/media)
- `authentication`: face-based enrollment and recognition
