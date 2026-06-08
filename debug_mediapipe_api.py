#!/usr/bin/env python3
"""Check what MediaPipe APIs are being detected."""
import sys

print("Checking MediaPipe API detection...")

# Exactly replicate the hand_tracker.py import logic
try:
    import mediapipe as mp
    print(f"✓ MediaPipe imported: {mp.__version__}")
    # Try multiple ways to access solutions
    try:
        _mp_hands = mp.solutions.hands
        _HAS_SOLUTIONS = True
        print(f"✓ mp.solutions.hands available: {_mp_hands}")
    except AttributeError as e:
        print(f"  mp.solutions.hands failed: {e}")
        # Try alternate access path
        try:
            from mediapipe.python.solutions import hands
            _mp_hands = hands
            _HAS_SOLUTIONS = True
            print(f"✓ mediapipe.python.solutions.hands available: {_mp_hands}")
        except ImportError as e2:
            print(f"  mediapipe.python.solutions.hands failed: {e2}")
            _HAS_SOLUTIONS = False
except Exception as e:
    print(f"✗ MediaPipe import failed: {e}")
    _HAS_SOLUTIONS = False

_HAS_TASKS = False
try:
    # Tasks API
    from mediapipe.tasks.python.vision import hand_landmarker as _hand_landmarker_module
    from mediapipe.tasks.python.vision.core import image as _mp_image
    from mediapipe.tasks.python.core import base_options as _base_options
    _HAS_TASKS = True
    print(f"✓ Tasks API available")
except Exception as e:
    print(f"  Tasks API not available: {e}")
    _HAS_TASKS = False

print()
print(f"_HAS_SOLUTIONS: {_HAS_SOLUTIONS}")
print(f"_HAS_TASKS: {_HAS_TASKS}")
print()

if _HAS_SOLUTIONS:
    print("✓ Can use legacy API (mp.solutions.hands)")
else:
    print("✗ Cannot use legacy API")

if _HAS_TASKS:
    print("✓ Can use Tasks API (but requires model file)")
else:
    print("✗ Cannot use Tasks API")

if not _HAS_SOLUTIONS and not _HAS_TASKS:
    print("✗✗ NO APIs available!")
    sys.exit(1)
