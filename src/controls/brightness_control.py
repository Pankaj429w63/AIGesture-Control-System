import screen_brightness_control as sbc
import logging

logger = logging.getLogger(__name__)

class BrightnessController:
    def increase(self, step: int = 15):
        try:
            current = sbc.get_brightness()[0]
            new = min(100, int(current) + step)
            sbc.set_brightness(new)
            logger.info(f"Brightness increased: {int(current)}% → {new}%")
        except Exception as e:
            logger.exception("Brightness increase failed: %s", e)

    def decrease(self, step: int = 15):
        try:
            current = sbc.get_brightness()[0]
            new = max(0, int(current) - step)
            sbc.set_brightness(new)
            logger.info(f"Brightness decreased: {int(current)}% → {new}%")
        except Exception as e:
            logger.exception("Brightness decrease failed: %s", e)
