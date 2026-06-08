r"""Automated demo that simulates gesture actions to test controllers without camera.

Usage:
  python scripts\auto_demo.py [--delay N] [--repeat]

It walks through configured gestures and triggers their mapped actions
with a short delay so you can observe volume/brightness changes.
"""
import time
import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import load_config
from src.controls.volume_control import VolumeController
from src.controls.brightness_control import BrightnessController
from src.controls.media_control import MediaController

logger = logging.getLogger("auto_demo")
logging.basicConfig(level=logging.INFO)


def run_sequence(delay: float = 2.0, repeat: bool = False):
    cfg = load_config()
    gestures = cfg.get("controls", {}).get("gestures", {})

    vol = VolumeController()
    bri = BrightnessController()
    media = MediaController()

    actions = []
    for gesture, action in gestures.items():
        actions.append((gesture, action))

    logger.info("Starting automated demo: %d actions, delay=%s", len(actions), delay)
    try:
        while True:
            for gesture, action in actions:
                logger.info("Simulate gesture '%s' -> action '%s'", gesture, action)
                if action == "volume_increase":
                    vol.increase(0.08)
                elif action == "volume_decrease":
                    vol.decrease(0.08)
                elif action == "mute":
                    vol.mute()
                elif action == "unmute":
                    vol.unmute()
                elif action == "brightness_increase":
                    bri.increase(10)
                elif action == "brightness_decrease":
                    bri.decrease(10)
                elif action == "play_pause":
                    media.play_pause()
                elif action == "next_track":
                    media.next_track()
                elif action == "previous_track":
                    media.previous_track()
                else:
                    logger.info("Action '%s' not handled by auto_demo", action)
                time.sleep(delay)
            if not repeat:
                break
    except KeyboardInterrupt:
        logger.info("Auto demo interrupted by user")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--delay", type=float, default=2.0, help="Seconds between actions")
    p.add_argument("--repeat", action="store_true", help="Repeat sequence until interrupted")
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_sequence(delay=args.delay, repeat=args.repeat)
