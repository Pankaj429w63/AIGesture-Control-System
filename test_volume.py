#!/usr/bin/env python3
"""Diagnostic script to test volume control."""
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

print("=" * 60)
print("Volume Control Diagnostic")
print("=" * 60)

# Test pycaw availability
try:
    from pycaw.pycaw import AudioUtilities
    print("✓ pycaw imported successfully")
except ImportError as e:
    print(f"✗ pycaw not available: {e}")
    sys.exit(1)

# Test comtypes
try:
    import comtypes
    print(f"✓ comtypes imported successfully (version: {comtypes.__version__ if hasattr(comtypes, '__version__') else 'unknown'})")
except ImportError as e:
    print(f"✗ comtypes not available: {e}")
    sys.exit(1)

# Try to get audio devices
try:
    devices = AudioUtilities.GetSpeakers()
    print(f"✓ Got speakers device: {devices}")
except Exception as e:
    print(f"✗ Failed to get speakers: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try to initialize COM
try:
    from comtypes import CoInitialize, CoUninitialize
    CoInitialize()
    print("✓ COM initialized successfully")
except Exception as e:
    print(f"✗ COM initialization failed: {e}")
    import traceback
    traceback.print_exc()

# Try to get volume interface
try:
    interface = devices.Activate(
        "BC2F7FB4-96CF-11D0-AD0E-00A0C9034A3B",  # IAudioEndpointVolume IID
        comtypes.CLSCTX_ALL,
        None
    )
    print(f"✓ Got audio interface: {interface}")
    print(f"  Interface type: {type(interface)}")
except Exception as e:
    print(f"✗ Failed to get audio interface: {e}")
    import traceback
    traceback.print_exc()

# Try to import VolumeController
try:
    from src.controls.volume_control import VolumeController
    print("✓ VolumeController imported")
    
    # Try to create instance
    vol = VolumeController()
    print(f"✓ VolumeController created: {vol}")
    
    # Try to get current volume
    try:
        current = vol.get_volume()
        print(f"✓ Current volume: {current}%")
    except Exception as e:
        print(f"✗ Failed to get current volume: {e}")
        
    # Try to increase volume slightly
    try:
        vol.increase()
        print(f"✓ Volume increased")
        current = vol.get_volume()
        print(f"  New volume: {current}%")
    except Exception as e:
        print(f"✗ Failed to increase volume: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"✗ VolumeController not available: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
