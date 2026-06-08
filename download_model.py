#!/usr/bin/env python3
"""Download MediaPipe hand landmarker model."""
import os
import sys
from pathlib import Path

try:
    from mediapipe.tasks.python.vision import hand_landmarker
    from mediapipe.tasks.python.core import base_options
except ImportError:
    print("ERROR: mediapipe not installed")
    sys.exit(1)

# Try to create a dummy HandLandmarker to trigger model download
try:
    model_path = Path("models/mediapipe/hand_landmarker.task")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use MediaPipe's built-in model fetching
    print("Fetching MediaPipe hand landmarker model...")
    import tempfile
    import shutil
    import urllib.request
    
    # Try the official path
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker.task"
    alt_url = "https://ai.google.dev/static/mediapipe/models/hand_landmarker.task"
    
    for attempt, try_url in enumerate([url, alt_url], 1):
        try:
            print(f"Attempt {attempt}: {try_url}")
            with urllib.request.urlopen(try_url, timeout=30) as response:
                with open(model_path, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"✓ Downloaded hand_landmarker.task to {model_path}")
                sys.exit(0)
        except Exception as e:
            print(f"  Failed: {e}")
    
    # Fallback: Use pip to install the bundled model
    print("\nTrying pip install with bundled model...")
    os.system("pip install -q --upgrade mediapipe-model-bundle")
    
    # Check if model now exists in site-packages
    import mediapipe
    mp_path = Path(mediapipe.__file__).parent
    bundled_model = mp_path / "tasks" / "hand_landmarker.task"
    
    if bundled_model.exists():
        shutil.copy(bundled_model, model_path)
        print(f"✓ Copied bundled model to {model_path}")
    else:
        print("ERROR: Could not find or download hand_landmarker.task")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
