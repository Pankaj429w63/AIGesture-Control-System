import yaml
from typing import Any, Dict
from pathlib import Path

def load_config(path: str = "config/config.yaml") -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg
