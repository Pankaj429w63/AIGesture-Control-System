python - <<'PY'
from src.controls.volume_control import VolumeController
v = VolumeController()
print("volume interface object:", v.volume)
print("current (0-1):", v.get_volume())
ok = v.set_volume(0.5)
print("set to 50% ok:", ok, "new:", v.get_volume())
v.increase(0.05)
print("after increase:", v.get_volume())
v.decrease(0.1)
print("after decrease:", v.get_volume())
PY