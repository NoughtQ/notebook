"""CLI for the note assistant. Publishing is disabled until configured."""

import json
import os
from pathlib import Path


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    config["model"] = os.getenv("OPENAI_MODEL", "")
    config["enabled_at"] = os.getenv("BOT_ENABLED_AT", "")
    return config


def validate_config(config: dict, publish: bool) -> None:
    if config.get("mode") not in {"off", "dry-run", "mention", "auto"}:
        raise ValueError("invalid bot mode")
    if publish and (
        config["mode"] not in {"mention", "auto"}
        or not config.get("model")
        or not config.get("enabled_at")
        or not config.get("public_paths")
    ):
        raise ValueError("publishing requires mode, model, enabled_at and public_paths")
