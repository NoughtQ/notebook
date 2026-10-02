"""Resolve public discussion pages to their checked-in Markdown."""

import hashlib
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml


def resolve_note(page_path: str, root: Path, public_paths: set[str]) -> Path | None:
    page = unquote(page_path).split("?", 1)[0].split("#", 1)[0].strip("/")
    if page.endswith(".html"):
        page = page[:-5]
    if page.endswith(".md"):
        page = page[:-3]
    if not page or any(part in {".", "..", ""} for part in page.split("/")):
        return None
    names = [f"docs/{page}.md", f"docs/{page}/index.md"]
    matches = []
    docs = (root / "docs").resolve()
    for name in names:
        path = root / name
        if name in public_paths and path.is_file() and path.resolve().is_relative_to(docs):
            matches.append(path)
    return matches[0] if len(matches) == 1 else None


def _public_text(path: Path, root: Path, allowed: set[str], limitations: list[str], seen: frozenset[Path] = frozenset()) -> str:
    if path in seen or len(seen) >= 3:
        limitations.append("包含文件层级过深或循环引用")
        return ""
    seen = seen | {path}
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            meta = yaml.safe_load(text[4:end]) or {}
            if isinstance(meta, dict) and (meta.get("password") or meta.get("encrypted")):
                limitations.append(f"加密页面未读取: {path.relative_to(root.resolve())}")
                return ""

    def include(match: re.Match) -> str:
        target = (path.parent / match.group(1)).resolve()
        try:
            name = target.relative_to(root.resolve()).as_posix()
        except ValueError:
            name = ""
        if name not in allowed or not target.is_file() or target.suffix != ".md":
            limitations.append("有未授权的包含文件，已略去")
            return "[包含文件已略去]"
        return _public_text(target, root, allowed, limitations, seen)

    text = re.sub(r'--8<--\s*["\']([^"\']+)["\']', include, text)
    for target in re.findall(r'!\[[^]]*\]\(([^)]+)\)', text):
        image = (path.parent / target).resolve()
        try:
            name = image.relative_to(root.resolve()).as_posix()
        except ValueError:
            name = ""
        if name not in allowed or image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"} or not image.is_file() or image.stat().st_size > 2 * 1024 * 1024:
            limitations.append(f"图片未核验: {target}")
    return text


def build_context(event: dict, thread: list[dict], root: Path, config: dict) -> dict:
    allowed = set(config["public_paths"])
    note = resolve_note(event["page_path"], root, allowed)
    limitations: list[str] = []
    notes = []
    if note is None:
        limitations.append("页面未列入公开清单或路径不明确")
    else:
        text = _public_text(note, root, allowed, limitations)
        if text:
            if len(text) > 50000:
                blocks = re.split(r"(?=^#{1,6} )", text, flags=re.M)
                question = event.get("body", "").lower()
                blocks.sort(key=lambda block: sum(word in block.lower() for word in re.findall(r"[\w\u4e00-\u9fff]{2,}", question)), reverse=True)
                text = "\n".join(block for block in blocks if len(block) <= 20000)[:50000]
                limitations.append("长笔记已截取相关章节")
            notes.append({"path": note.relative_to(root).as_posix(), "heading": "", "text": text,
                          "sha256": hashlib.sha256(note.read_bytes()).hexdigest()})
    try:
        base_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        base_sha = ""
    return {"key": event["key"], "base_sha": base_sha, "question": event.get("body", ""),
            "thread": thread[-12:], "notes": notes, "images": [], "limitations": limitations,
            "style_examples": []}
