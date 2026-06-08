import time
import cv2
import argparse
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger
from src.gesture_detection.hand_tracker import HandTracker
from src.gesture_detection.landmark_extractor import landmarks_to_vector
from src.inference.predict import InferenceEngine
from src.controls.volume_control import VolumeController
from src.controls.brightness_control import BrightnessController
from src.controls.media_control import MediaController
from src.authentication.face_auth import authenticate_with_camera

def main(mp_model: str = None, no_auth: bool = False):
    cfg = load_config()
    logger = setup_logger("main", cfg.get("logging", {}).get("file"))
    if not no_auth and cfg.get("auth", {}).get("face_required", False):
        try:
            ok, user = authenticate_with_camera()
            if not ok:
                logger.warning("User not authenticated - exiting")
                return
            logger.info(f"Authenticated: {user}")
        except Exception as e:
            logger.exception("Authentication failed: %s", e)

    ht = HandTracker(model_path=mp_model) if mp_model else HandTracker()
    ie = InferenceEngine()
    vol = VolumeController()
    bri = BrightnessController()
    media = MediaController()

    # If no trained model is available, fall back to interactive manual control
    if ie.model is None:
        logger.warning("No trained model found at %s; falling back to manual control.\nRun 'python scripts/manual_control.py' if you prefer to run it separately.", ie.path)
        try:
            import runpy
            runpy.run_path("scripts/manual_control.py", run_name="__main__")
        except Exception as e:
            logger.exception("Failed to start manual control fallback: %s", e)
        return

    cap = cv2.VideoCapture(0)
    last_action_time = 0
    cooldown = cfg.get("model", {}).get("gesture_cooldown_seconds", 1.0)

    fps_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        hands = ht.process_frame(frame)
        if hands:
            features = landmarks_to_vector(hands[0])
            label, conf = ie.predict(features)
            now = time.time()
            if conf >= cfg["model"]["confidence_threshold"] and (now - last_action_time) > cooldown:
                action = cfg["controls"]["gestures"].get(label, None)
                if action:
                    logger.info(f"🎯 Detected: {label} -> {action} (conf={conf:.2%})")
                    if action == "volume_increase":
                        vol.increase()
                    elif action == "volume_decrease":
                        vol.decrease()
                    elif action == "mute":
                        vol.mute()
                    elif action == "play_pause":
                        media.play_pause()
                    elif action == "next_track":
                        media.next_track()
                    elif action == "previous_track":
                        media.previous_track()
                    elif action == "brightness_increase":
                        bri.increase()
                    elif action == "brightness_decrease":
                        bri.decrease()
                    last_action_time = now
                    status_text = f"✓ {label.upper()}"
                    color = (0, 255, 0)  # Green
                else:
                    status_text = f"? {label.upper()}"
                    color = (0, 165, 255)  # Orange
            else:
                status_text = f"{label} ({conf:.0%})"
                color = (100, 100, 255)  # Red
            cv2.putText(frame, status_text, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # FPS
        fps = 1.0 / (time.time() - fps_time)
        fps_time = time.time()
        cv2.putText(frame, f"FPS: {int(fps)}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255),2)
        cv2.imshow("AI Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release(); cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp-model", dest="mp_model", help="Path to MediaPipe hand_landmarker.task model bundle")
    parser.add_argument("--no-auth", dest="no_auth", action="store_true", help="Skip face authentication")
    args = parser.parse_args()
    main(mp_model=args.mp_model, no_auth=args.no_auth)
