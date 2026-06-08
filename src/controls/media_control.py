import pyautogui
import logging

logger = logging.getLogger(__name__)

class MediaController:
    def play_pause(self):
        try:
            pyautogui.press('playpause')
            logger.info("Media: play/pause")
        except Exception:
            try:
                pyautogui.press('space')
                logger.info("Media: play/pause (fallback)")
            except Exception as e:
                logger.exception("Play/pause failed: %s", e)

    def next_track(self):
        try:
            pyautogui.press('nexttrack')
            logger.info("Media: next track")
        except Exception:
            try:
                pyautogui.hotkey('ctrl', 'right')
                logger.info("Media: next track (fallback)")
            except Exception as e:
                logger.exception("Next track failed: %s", e)

    def previous_track(self):
        try:
            pyautogui.press('prevtrack')
            logger.info("Media: previous track")
        except Exception:
            try:
                pyautogui.hotkey('ctrl', 'left')
                logger.info("Media: previous track (fallback)")
            except Exception as e:
                logger.exception("Previous track failed: %s", e)
