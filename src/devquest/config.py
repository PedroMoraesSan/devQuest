from pathlib import Path
from tomllib import loads

from devquest.database import BASE_DIR

CONFIG_PATH = BASE_DIR / "config.toml"

DEFAULTS = {
    "theme": "cyberpunk",
    "animations": True,
    "sounds": False,
    "default_branch": "main",
}


def _ensure_dir():
    BASE_DIR.mkdir(exist_ok=True)


def load_config() -> dict:
    _ensure_dir()

    if not CONFIG_PATH.exists():
        return DEFAULTS.copy()

    try:
        data = loads(CONFIG_PATH.read_text())
    except (OSError, ValueError):
        return DEFAULTS.copy()

    config = DEFAULTS.copy()
    config.update({k: data[k] for k in DEFAULTS if k in data})
    return config


def save_config(config: dict) -> None:
    _ensure_dir()

    merged = DEFAULTS.copy()
    merged.update(config)

    lines = [
        f'theme = "{merged["theme"]}"',
        f"animations = {'true' if merged['animations'] else 'false'}",
        f"sounds = {'true' if merged['sounds'] else 'false'}",
        f'default_branch = "{merged["default_branch"]}"',
        "",
    ]

    CONFIG_PATH.write_text("\n".join(lines))


def get(key: str):
    return load_config().get(key, DEFAULTS.get(key))


def set_value(key: str, value) -> None:
    if key not in DEFAULTS:
        raise KeyError(key)

    config = load_config()
    config[key] = value
    save_config(config)


def update(**kwargs) -> dict:
    config = load_config()
    for key, value in kwargs.items():
        if key in DEFAULTS:
            config[key] = value
    save_config(config)
    return config
