import time
import cv2
from src.gesture_detection.hand_tracker import HandTracker
from src.inference.predict import InferenceEngine
from src.gesture_detection.landmark_extractor import landmarks_to_vector

MODEL_PATH = "models/mediapipe/hand_landmarker.task"

def main():
    ht = HandTracker(model_path=MODEL_PATH)
    ie = InferenceEngine()
    cap = cv2.VideoCapture(0)
    start = time.time()
    duration = 10.0  # seconds
    print("Starting headless demo for", duration, "seconds")
    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            print("No frame from camera, exiting")
            break
        hands = ht.process_frame(frame)
        if hands:
            features = landmarks_to_vector(hands[0])
            label, conf = ie.predict(features)
            print(f"Detected: {label} (conf={conf:.3f})")
        time.sleep(0.05)
    cap.release()
    print("Headless demo finished")

if __name__ == '__main__':
    main()
