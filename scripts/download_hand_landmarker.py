#!/usr/bin/env python3
import os
import sys
import urllib.request
import shutil

CANDIDATE_URLS = [
    "https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task",
    "https://storage.googleapis.com/mediapipe-tasks/models/hand_landmarker.task",
    "https://github.com/google/mediapipe/raw/master/mediapipe/tasks/desktop/vision/hand_landmarker/hand_landmarker.task",
]

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "mediapipe")
OUT_PATH = os.path.join(OUT_DIR, "hand_landmarker.task")


def download(url, out_path):
    print(f"Trying: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "python-urllib/3"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = resp.getheader('Content-Length')
            if total:
                total = int(total)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'wb') as out:
                shutil.copyfileobj(resp, out)
        print(f"Downloaded to {out_path}")
        return True
    except Exception as e:
        print(f"Failed to download from {url}: {e}")
        return False


if __name__ == '__main__':
    if os.path.exists(OUT_PATH):
        print(f"Model already exists at {OUT_PATH}")
        sys.exit(0)

    for url in CANDIDATE_URLS:
        ok = download(url, OUT_PATH)
        if ok:
            print("Download succeeded.")
            sys.exit(0)

    print("All candidate URLs failed. Please download hand_landmarker.task manually and place it at:")
    print(OUT_PATH)
    sys.exit(2)
