"""Configuration loader — reads config/*.json, caches in-process."""
import json
from pathlib import Path
from typing import Any

_CONFIG_DIR = Path(__file__).parent.parent.parent.parent / "config"
_cache: dict[str, Any] = {}


def get_config(name: str) -> dict[str, Any]:
    """Load and cache a config file by name (without .json extension)."""
    if name not in _cache:
        path = _CONFIG_DIR / f"{name}.json"
        _cache[name] = json.loads(path.read_text(encoding="utf-8"))
    return _cache[name]


def cfg(name: str, key: str, default: Any = None) -> Any:
    """Get a single key from a config file with an optional default."""
    return get_config(name).get(key, default)


def reload() -> None:
    """Clear config cache — use in tests to isolate config state."""
    _cache.clear()
