import keyboard
import logging

logger = logging.getLogger(__name__)

class KeyboardActions:
    def send_key(self, key: str):
        try:
            keyboard.send(key)
        except Exception as e:
            logger.exception("Failed to send key %s: %s", key, e)
