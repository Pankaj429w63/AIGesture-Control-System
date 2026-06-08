r"""Manual control demo to test Volume and Brightness controllers.

Run with: python scripts\manual_control.py

Key controls while the camera window is focused:
  u - volume up
  j - volume down
  m - toggle mute
  i - brightness up
  k - brightness down
  q or ESC - quit
"""
import cv2
import time
import logging
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controls.volume_control import VolumeController
from src.controls.brightness_control import BrightnessController

logger = logging.getLogger("manual_control")
logging.basicConfig(level=logging.INFO)


def main():
    vc = VolumeController()
    bc = BrightnessController()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Could not open camera")
        return

    last_time = time.time()
    fps = 0
    muted = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        dt = now - last_time
        if dt > 0:
            fps = 1.0 / dt
        last_time = now

        cv2.putText(frame, f"Manual control - FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.putText(frame, "Keys: u/j vol up/down | i/k bright up/down | m mute | q quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("Manual Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break
        elif key == ord('u'):
            logger.info("Volume up")
            vc.increase(0.05)
        elif key == ord('j'):
            logger.info("Volume down")
            vc.decrease(0.05)
        elif key == ord('m'):
            try:
                if muted:
                    vc.unmute()
                    muted = False
                    logger.info("Unmuted")
                else:
                    vc.mute()
                    muted = True
                    logger.info("Muted")
            except Exception as e:
                logger.exception("Mute toggle failed: %s", e)
        elif key == ord('i'):
            logger.info("Brightness up")
            bc.increase(10)
        elif key == ord('k'):
            logger.info("Brightness down")
            bc.decrease(10)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
