"""CLI for the note assistant. Publishing is disabled until configured."""

import json
import os
import copy
import hashlib
import shutil
import subprocess
import tempfile
import argparse
import base64
import re
import time
from importlib.metadata import version
from urllib.request import urlopen
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    config["mode"] = os.getenv("NOTE_BOT_MODE", config["mode"])
    config["model"] = os.getenv("OPENROUTER_MODEL", "")
    config["enabled_at"] = os.getenv("BOT_ENABLED_AT", "")
    config["bot_login"] = os.getenv("BOT_LOGIN", "")
    return config


def validate_config(config: dict, publish: bool) -> None:
    if config.get("mode") not in {"off", "dry-run", "mention", "auto"}:
        raise ValueError("invalid bot mode")
    if config["mode"] != "off" and not config.get("enabled_at"):
        raise ValueError("BOT_ENABLED_AT is required before scanning questions")
    if publish and (
        config["mode"] not in {"mention", "auto"}
        or not config.get("model")
        or not config.get("enabled_at")
        or not config.get("public_paths")
        or not config.get("bot_login")
    ):
        raise ValueError("publishing requires mode, model, enabled_at, bot_login and public_paths")


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
    if not body:
        return state, None
    if mode == "mention" and body.splitlines()[0].strip() != "/ask":
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
    patch_status = "not-needed"
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
                stats = apply_edits(result["edits"], target)
            patch_status = "passed"
        except (ValueError, OSError) as exc:
            result["action"] = "clarify"
            result["edits"] = []
            result["answer_md"] = "这处可能需要修正，但补丁未通过检查，暂不提交 PR。" + str(exc)[:300]
            stats = {"files": 0, "lines": 0}
            patch_status = "failed"
    result_sha = hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {"key": context["key"], "base_sha": base_sha, "body_sha256": event.get("body_sha256", ""),
            "result_sha256": result_sha, "allowed_paths": config["public_paths"],
            "diff_stats": stats, "patch_status": patch_status, "result": result}


def evaluate(cases: list[dict], config: dict, output_dir: Path, client=None) -> dict:
    """Run read-only, snapshot-pinned evaluation; factual grades require a human."""
    from collections import Counter
    from urllib.parse import urlparse
    from .model import generate

    required = {"id", "discussion_url", "source_sha", "question", "category",
                "expected_facts", "expected_action", "evidence_urls", "page_path", "created_at"}
    if len(cases) != 30 or Counter(case.get("category") for case in cases) != {
            "correction": 10, "explanation": 10, "ambiguity": 5, "insufficient": 5}:
        raise ValueError("evaluation requires 30 reviewed cases in the 10/10/5/5 split")
    style_urls = {item["discussion_url"] for item in json.loads(
        (Path(__file__).resolve().parents[1] / "data/style.json").read_text(encoding="utf-8"))}
    if len({case.get("id") for case in cases}) != 30 or any(
        not required <= case.keys() or case["discussion_url"] in style_urls or
        not re.fullmatch(r"[0-9a-f]{40}", case["source_sha"]) or
        case["page_path"] not in config.get("eval_public_paths", []) or
        not case["expected_facts"] or not case["evidence_urls"] or
        any(urlparse(url).scheme != "https" for url in case["evidence_urls"])
        for case in cases
    ):
        raise ValueError("evaluation cases are incomplete, overlapping with style, or outside public notes")
    root = Path.cwd()
    snapshots = {}
    for case in cases:
        commit_time = subprocess.check_output(["git", "show", "-s", "--format=%cI", case["source_sha"]], cwd=root, text=True).strip()
        if datetime.fromisoformat(commit_time) > datetime.fromisoformat(case["created_at"].replace("Z", "+00:00")):
            raise ValueError("snapshot postdates question")
        note = subprocess.check_output(["git", "show", f"{case['source_sha']}:{case['page_path']}"], cwd=root, text=True)
        if re.search(r"(?m)^password\s*:", note) or "--8<--" in note:
            raise ValueError("snapshot includes unreviewed content")
        snapshots[case["id"]] = note[:20_000]
    if client is None:
        if not os.getenv("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY is required for live evaluation")
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1",
                        max_retries=0, timeout=90)
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path = output_dir / "results.jsonl"
    prior = [json.loads(line) for line in results_path.read_text(encoding="utf-8").splitlines()] if results_path.exists() else []
    done = {item["id"] for item in prior}
    today = datetime.now(timezone.utc).date().isoformat()
    remaining = max(0, config["daily_limit"] - sum(item.get("run_date") == today for item in prior))
    for case in [item for item in cases if item["id"] not in done][:remaining]:
        context = {"key": case["id"], "question": case["question"],
                   "notes": [{"path": case["page_path"], "text": snapshots[case["id"]],
                              "sha256": hashlib.sha256(snapshots[case["id"]].encode()).hexdigest()}],
                   "thread": [], "limitations": [], "base_sha": case["source_sha"]}
        started = time.monotonic()
        result = generate(context, config, client)
        row = {"id": case["id"], "run_date": today, "model": config["model"],
               "source_sha": case["source_sha"], "action": result["action"],
               "expected_action": case["expected_action"], "answer_md": result["answer_md"],
               "expected_facts": case["expected_facts"], "evidence_urls": case["evidence_urls"],
               "claims": result["claims"], "sources": result["sources"],
               "usage": result.get("_meta", {}), "latency_seconds": round(time.monotonic() - started, 2),
               "human_grade": None, "needs_human_review": True}
        with results_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        prior.append(row)
    summary = {"total": 30, "evaluated": len(prior), "remaining": 30 - len(prior),
               "human_review_required": True, "model": config["model"],
               "action_matches": sum(item["action"] == item["expected_action"] for item in prior),
               "input_tokens": sum(item.get("usage", {}).get("input_tokens", 0) for item in prior),
               "output_tokens": sum(item.get("usage", {}).get("output_tokens", 0) for item in prior),
               "search_calls": sum(item.get("usage", {}).get("search_calls", 0) for item in prior),
               "openai_sdk_version": version("openai"),
               "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
               "prompt_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] / "data/prompt.md").read_bytes()).hexdigest()}
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def _load_state(api) -> tuple[dict, str]:
    try:
        data = api("GET", "/repos/NoughtQ/notebook/contents/state.json?ref=bot-state", None)
    except HTTPError as exc:
        if exc.code != 404:
            raise
        return {}, ""
    return json.loads(base64.b64decode(data["content"])), data["sha"]


def _bootstrap_state_branch(api) -> None:
    sha = api("GET", "/repos/NoughtQ/notebook/git/ref/heads/main", None)["object"]["sha"]
    try:
        api("POST", "/repos/NoughtQ/notebook/git/refs", {"ref": "refs/heads/bot-state", "sha": sha})
    except HTTPError as exc:
        if exc.code != 422:
            raise


def _thread_context(thread: list[dict], comment_id: str) -> list[dict]:
    current = next((item for item in thread if item["id"] == comment_id), None)
    if current is None:
        return []
    if current["id"] == thread[0]["id"]:
        return thread[:1]
    key = lambda item: (item.get("createdAt", ""), item["id"])
    previous = sorted((item for item in thread[1:] if key(item) <= key(current)), key=key)
    return [thread[0], *previous[-5:]]


def _prepare(payload: dict, root: Path, config: dict, api, may_publish: bool) -> dict:
    from .context import build_context
    from .github import read_event, read_thread, discover_events, save_state

    validate_config(config, publish=may_publish and config["mode"] in {"mention", "auto"})

    state, sha = _load_state(api) if may_publish and config["mode"] in {"mention", "auto"} else ({}, "")
    fresh = read_event(payload, api)
    discovered = discover_events(api, state, config)
    candidates = {item["key"]: item for item in discovered}
    if fresh:
        candidates[fresh["key"]] = fresh
    selected = None
    for event in sorted(candidates.values(), key=lambda item: (item["created_at"], item["key"])):
        record = state.get("events", {}).get(event["key"], {})
        cached = record.get("verified")
        if cached and record.get("reservation"):
            current_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            if cached["base_sha"] == current_sha and cached["body_sha256"] == event["body_sha256"]:
                selected = {"skip": False, "retry_publish": True,
                            "verified": cached, "reservation": record["reservation"]}
                break
            record.pop("verified", None)
            record.pop("reservation", None)
        thread = read_thread(event, api) if event.get("comment_id") else []
        if event.get("comment_id"):
            thread = _thread_context(thread, event["comment_id"])
        if event.get("comment_id") and not thread:
            state.setdefault("events", {}).setdefault(event["key"], {})["status"] = "skipped"
            continue
        context = build_context(event, thread, root, config)
        if not context["notes"]:
            state.setdefault("events", {}).setdefault(event["key"], {})["status"] = "skipped"
            continue
        state, reservation = admit(event, state, config, datetime.now(timezone.utc))
        if reservation:
            selected = {"skip": False, "event": event, "reservation": reservation,
                        "context": context}
            break
    if may_publish and config["mode"] in {"mention", "auto"}:
        if not sha:
            _bootstrap_state_branch(api)
        save_state(api, state, sha)
    return selected or {"skip": True}


def main() -> None:
    parser = argparse.ArgumentParser(description="Notebook Discussion assistant")
    parser.add_argument("stage", choices=["prepare", "generate", "verify", "publish", "reconcile", "evaluate"])
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    config = load_config(root / "bot/data/config.json")
    if args.stage == "evaluate":
        cases = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(json.dumps(evaluate(cases, config, args.output), ensure_ascii=False))
        return
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if args.stage == "prepare":
        from .github import request
        output = _prepare(payload, root, config, request, args.publish)
    elif args.stage == "generate":
        if payload.get("skip") or payload.get("retry_publish"):
            output = payload
        else:
            from openai import OpenAI
            from .model import generate
            client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1",
                            max_retries=0, timeout=90)
            output = {**payload, "result": generate(payload["context"], config, client)}
    elif args.stage == "verify":
        output = ({"verified": payload["verified"], "reservation": payload["reservation"]}
                  if payload.get("retry_publish") else
                  {"verified": verify(payload, root, config), "reservation": payload["reservation"]})
    elif args.stage == "publish":
        if not args.publish:
            raise ValueError("--publish required")
        from .github import request, publish, save_state
        validate_config(config, publish=True)
        if hashlib.sha256(json.dumps(payload["verified"]["result"], ensure_ascii=False, sort_keys=True).encode()).hexdigest() != payload["verified"]["result_sha256"]:
            raise ValueError("verified answer was modified")
        state, sha = _load_state(request)
        if not sha:
            raise ValueError("bot-state is missing")
        record = state["events"].get(payload["reservation"]["key"], {})
        if record.get("status") == "reserved" and record.get("reservation_id") == payload["reservation"]["reservation_id"] and not record.get("verified"):
            record["verified"] = payload["verified"]
            record["reservation"] = payload["reservation"]
            sha = save_state(request, state, sha)
        new_state = publish(payload["verified"], payload["reservation"], state, request, config)
        if new_state != state:
            save_state(request, new_state, sha)
        output = {"status": new_state["events"][payload["reservation"]["key"]]["status"]}
    elif args.stage == "reconcile":
        from .github import request, reconcile, save_state
        if config["mode"] not in {"mention", "auto"}:
            output = {"skip": True}
        else:
            state, sha = _load_state(request)
            if not sha:
                raise ValueError("bot-state is missing")
            def site_get(url):
                if not url.startswith(config["site_url"].rstrip("/") + "/"):
                    raise ValueError("site URL is outside configured domain")
                try:
                    with urlopen(url, timeout=15) as response:
                        return response.status, response.read(2_000_000).decode("utf-8")
                except HTTPError as exc:
                    return exc.code, ""
            new_state = reconcile(state, request, site_get, config)
            if new_state != state:
                save_state(request, new_state, sha)
            output = {"pull_requests": new_state.get("pull_requests", {})}
    else:
        raise ValueError(f"{args.stage} is implemented in a later task")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
