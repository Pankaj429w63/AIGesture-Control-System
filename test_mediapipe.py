#!/usr/bin/env python3
"""Diagnostic script to check MediaPipe availability."""
import sys

print("=" * 60)
print("MediaPipe Availability Check")
print("=" * 60)

# Check MediaPipe installation
try:
    import mediapipe as mp
    print(f"✓ MediaPipe imported: {mp.__version__}")
except ImportError as e:
    print(f"✗ MediaPipe not available: {e}")
    sys.exit(1)

# Check Solutions API
try:
    from mediapipe.python.solutions import hands
    print(f"✓ Solutions API available: mediapipe.python.solutions.hands")
except ImportError:
    try:
        hands = mp.solutions.hands
        print(f"✓ Solutions API available: mp.solutions.hands")
    except AttributeError as e:
        print(f"✗ Solutions API not available: {e}")
        hands = None

# Check Tasks API
try:
    from mediapipe.tasks.python.vision import hand_landmarker
    print(f"✓ Tasks API available: mediapipe.tasks.python.vision.hand_landmarker")
except ImportError as e:
    print(f"✗ Tasks API not available: {e}")
    hand_landmarker = None

# Try to create a hands detector with solutions
if hands:
    try:
        hand_detector = hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        print(f"✓ Successfully created hands detector with Solutions API")
        hand_detector.close()
    except Exception as e:
        print(f"✗ Failed to create hands detector: {e}")

print("=" * 60)
print("Summary:")
print(f"  Solutions API: {'AVAILABLE' if hands else 'NOT AVAILABLE'}")
print(f"  Tasks API: {'AVAILABLE' if hand_landmarker else 'NOT AVAILABLE'}")
print("=" * 60)
