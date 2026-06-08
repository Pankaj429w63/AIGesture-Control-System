"""Collect hand landmarks from webcam and save to CSV for labels."""
import sys
from pathlib import Path
import cv2
import csv
import os
from typing import List

# Ensure project root is on sys.path so `src` imports work when running script directly
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.gesture_detection.hand_tracker import HandTracker
from src.gesture_detection.landmark_extractor import landmarks_to_vector

def collect(label: str, out_csv: str = "dataset/gesture_landmarks.csv", max_samples: int = 500):
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    ht = HandTracker()
    cap = cv2.VideoCapture(0)
    saved = 0
    header_written = False
    with open(out_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        while saved < max_samples:
            ret, frame = cap.read()
            if not ret:
                break
            hands = ht.process_frame(frame)
            if hands:
                vec = landmarks_to_vector(hands[0])
                row = list(vec) + [label]
                if not header_written and f.tell() == 0:
                    cols = [f"x{i}" for i in range(len(vec))] + ["label"]
                    writer.writerow(cols)
                    header_written = True
                writer.writerow(row)
                saved += 1
                cv2.putText(frame, f"Saved: {saved}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
            cv2.imshow("Collect - Press q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("label")
    p.add_argument("--out", default="dataset/gesture_landmarks.csv")
    p.add_argument("--max", type=int, default=200)
    args = p.parse_args()
    collect(args.label, args.out, args.max)
