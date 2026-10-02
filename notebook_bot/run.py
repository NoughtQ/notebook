"""CLI for the note assistant. Publishing is disabled until configured."""

import json
import os
import copy
import hashlib
from datetime import datetime, timezone, timedelta
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


def admit(event: dict, state: dict, config: dict, now: datetime) -> tuple[dict, dict | None]:
    state = copy.deepcopy(state)
    state.setdefault("version", 1)
    state.setdefault("events", {})
    state.setdefault("daily", {})
    state.setdefault("paused_threads", [])
    state.setdefault("pull_requests", {})
    state.setdefault("scan_watermark", "")
    mode = config["mode"]
    if mode == "off":
        return state, None
    created_at = event.get("created_at")
    if not created_at or datetime.fromisoformat(created_at.replace("Z", "+00:00")) < datetime.fromisoformat(config["enabled_at"].replace("Z", "+00:00")):
        return state, None
    actor = event.get("actor", "").lower()
    root = event.get("thread_root_id", "")
    if actor == "noughtq":
        if event.get("body", "").strip() == "/bot resume":
            state["paused_threads"] = [item for item in state["paused_threads"] if item != root]
        elif root not in state["paused_threads"]:
            state["paused_threads"].append(root)
        return state, None
    if actor == config.get("bot_login", "").lower() or actor.endswith("[bot]") or root in state["paused_threads"]:
        return state, None
    body = event.get("body", "").strip()
    if mode == "mention" and body.splitlines()[0].strip() != "/ask":
        return state, None
    if not body or len(body) < 5:
        return state, None
    key = event["key"]
    prior = state["events"].get(key, {})
    if prior.get("status") == "reserved" and prior.get("reserved_at"):
        since = datetime.fromisoformat(prior["reserved_at"])
        if now - since >= timedelta(minutes=15):
            prior["status"] = "retryable"
    if prior and (prior["status"] not in {"pending", "retryable"} or prior.get("attempts", 0) >= 2):
        return state, None
    date = now.astimezone(timezone.utc).date().isoformat()
    daily = state["daily"].setdefault(date, {"total": 0, "authors": {}})
    if daily["total"] >= config["daily_limit"] or daily["authors"].get(actor, 0) >= config["author_daily_limit"]:
        return state, None
    daily["total"] += 1
    daily["authors"][actor] = daily["authors"].get(actor, 0) + 1
    attempt = prior.get("attempts", 0) + 1
    reservation_id = hashlib.sha256(f"{key}:{attempt}:{date}".encode()).hexdigest()[:24]
    reservation = {"event": event, "key": key, "date": date, "attempt": attempt,
                   "reservation_id": reservation_id, "run_id": os.getenv("GITHUB_RUN_ID", "local"),
                   "script_sha": os.getenv("GITHUB_SHA", "")}
    state["events"][key] = {"status": "reserved", "reservation_id": reservation_id,
                             "reserved_at": now.isoformat(), "attempts": attempt, "reply_id": prior.get("reply_id"),
                             "pr_number": prior.get("pr_number")}
    return state, reservation
