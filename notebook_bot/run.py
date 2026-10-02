"""CLI for the note assistant. Publishing is disabled until configured."""

import json
import os
import copy
import hashlib
import shutil
import subprocess
import tempfile
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


def verify(candidate: dict, root: Path, config: dict) -> dict:
    from .patch import validate_edits, apply_edits

    context, event = candidate["context"], candidate["event"]
    result = copy.deepcopy(candidate["result"])
    base_sha = context.get("base_sha", "")
    if base_sha:
        current_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        if current_sha != base_sha:
            raise ValueError("note base changed; regenerate answer")
    stats = {"files": 0, "lines": 0}
    build_status = "not-needed"
    if result["action"] == "correction":
        try:
            validate_edits(result["edits"], root, set(config["public_paths"]))
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp)
                for name in config["public_paths"]:
                    source = root / name
                    if source.is_file():
                        destination = target / name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, destination)
                shutil.copytree(root / "scripts", target / "scripts")
                (target / "notebook_bot").mkdir()
                (target / "notebook_bot/config.json").write_text(json.dumps(config), encoding="utf-8")
                stats = apply_edits(result["edits"], target)
                completed = subprocess.run(["bash", str(target / "scripts/build-notes.sh"), "public", str(target / "site")],
                                           cwd=target, capture_output=True, text=True, timeout=120)
                if completed.returncode:
                    raise ValueError("public build failed: " + completed.stderr[-500:])
            build_status = "passed"
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            result["action"] = "clarify"
            result["edits"] = []
            result["answer_md"] = "这处可能需要修正，但补丁未通过检查，暂不提交 PR。" + str(exc)[:300]
            stats = {"files": 0, "lines": 0}
            build_status = "failed"
    result_sha = hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {"key": context["key"], "base_sha": base_sha, "body_sha256": event.get("body_sha256", ""),
            "result_sha256": result_sha, "allowed_paths": config["public_paths"],
            "diff_stats": stats, "build_status": build_status, "result": result}
