from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import logging

logger = logging.getLogger(__name__)


class VolumeController:
    def __init__(self):
        self.volume = None
        try:
            # Ensure COM is initialized on this thread
            try:
                comtypes.CoInitialize()
            except Exception:
                # it's safe to continue if already initialized
                pass

            devices = AudioUtilities.GetSpeakers()
            if devices is None:
                logger.error("No speaker device found; volume control disabled")
                return

            # Try multiple ways to obtain IAudioEndpointVolume
            tried = []
            # 1) Direct property (pycaw newer wrappers)
            try:
                if hasattr(devices, 'EndpointVolume'):
                    self.volume = devices.EndpointVolume
                    logger.info("VolumeController: using devices.EndpointVolume")
                else:
                    tried.append('devices.EndpointVolume missing')
            except Exception as ex:
                tried.append(f'devices.EndpointVolume error: {ex}')

            # 2) Activate via wrapper (common pattern)
            if self.volume is None:
                try:
                    if hasattr(devices, 'Activate'):
                        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                        logger.info("VolumeController: using devices.Activate()")
                    elif hasattr(devices, '_dev') and hasattr(devices._dev, 'Activate'):
                        interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                        logger.info("VolumeController: using devices._dev.Activate()")
                    else:
                        tried.append('no Activate() available on device wrapper')
                except Exception as ex:
                    tried.append(f'Activate error: {ex}')

            if self.volume is None:
                logger.warning("Failed to initialize IAudioEndpointVolume. Tried: %s", tried)
        except Exception as e:
            logger.exception("Failed to initialize volume controller: %s", e)

    def get_volume(self) -> float:
        """Return master volume scalar between 0.0 and 1.0, or -1 on failure."""
        try:
            if self.volume is None:
                return -1.0
            return float(self.volume.GetMasterVolumeLevelScalar())
        except Exception as e:
            logger.exception("Get volume failed: %s", e)
            return -1.0

    def set_volume(self, value: float):
        """Set master volume scalar (0.0 - 1.0)."""
        try:
            if self.volume is None:
                logger.warning("Volume interface not available")
                return False
            v = max(0.0, min(1.0, float(value)))
            # If self.volume is a COM pointer, call SetMasterVolumeLevelScalar
            if hasattr(self.volume, 'SetMasterVolumeLevelScalar'):
                self.volume.SetMasterVolumeLevelScalar(v, None)
            else:
                # if it's already a pointer-like object, try calling method
                try:
                    self.volume.SetMasterVolumeLevelScalar(v, None)
                except Exception:
                    logger.exception("SetMasterVolumeLevelScalar failed")
                    return False
            logger.info("Volume set to %.2f", v)
            return True
        except Exception as e:
            logger.exception("Set volume failed: %s", e)
            return False

    def increase(self, step: float = 0.05):
        try:
            cur = self.get_volume()
            if cur < 0:
                logger.warning("Volume interface not available")
                return
            new = min(1.0, cur + step)
            self.set_volume(new)
            logger.info(f"Volume increased: {cur:.0%} → {new:.0%}")
        except Exception as e:
            logger.exception("Volume increase failed: %s", e)

    def decrease(self, step: float = 0.05):
        try:
            cur = self.get_volume()
            if cur < 0:
                logger.warning("Volume interface not available")
                return
            new = max(0.0, cur - step)
            self.set_volume(new)
            logger.info(f"Volume decreased: {cur:.0%} → {new:.0%}")
        except Exception as e:
            logger.exception("Volume decrease failed: %s", e)

    def mute(self):
        try:
            if self.volume is None:
                logger.warning("Volume interface not available")
                return
            self.volume.SetMute(1, None)
        except Exception as e:
            logger.exception("Mute failed: %s", e)

    def unmute(self):
        try:
            if self.volume is None:
                logger.warning("Volume interface not available")
                return
            self.volume.SetMute(0, None)
        except Exception as e:
            logger.exception("Unmute failed: %s", e)
