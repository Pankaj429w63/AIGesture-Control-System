import cv2
import os
import numpy as np
from typing import Tuple

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def enroll_user(username: str, out_dir: str = "data/face_db", samples: int = 20):
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    saved = 0
    user_dir = os.path.join(out_dir, username)
    os.makedirs(user_dir, exist_ok=True)
    while saved < samples:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            face = gray[y:y+h, x:x+w]
            path = os.path.join(user_dir, f"{saved}.png")
            cv2.imwrite(path, face)
            saved += 1
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.imshow("Enroll", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release(); cv2.destroyAllWindows()

def train_lbph(face_db: str = "data/face_db", model_out: str = "models/face_recognizer.yml"):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}
    current_label = 0
    for user in os.listdir(face_db):
        path = os.path.join(face_db, user)
        if not os.path.isdir(path):
            continue
        label_map[current_label] = user
        for img in os.listdir(path):
            imgp = os.path.join(path, img)
            gray = cv2.imread(imgp, cv2.IMREAD_GRAYSCALE)
            faces.append(gray)
            labels.append(current_label)
        current_label += 1
    recognizer.train(faces, np.array(labels))
    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    recognizer.write(model_out)
    return label_map

def authenticate_with_camera(model_path: str = "models/face_recognizer.yml", label_map: dict = None, threshold: int = 60) -> Tuple[bool, str]:
    if not os.path.exists(model_path):
        # Don't raise here; return not-authenticated so the app can continue.
        # Calling code may log or act on failure.
        return False, ""
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)
    authenticated = (False, "")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            face = gray[y:y+h, x:x+w]
            label, conf = recognizer.predict(face)
            name = label_map.get(label, str(label)) if label_map else str(label)
            if conf < threshold:
                cap.release(); cv2.destroyAllWindows()
                return True, name
        cv2.imshow("Authenticate - Press q to cancel", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release(); cv2.destroyAllWindows()
    return False, ""
