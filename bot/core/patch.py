"""Apply small, exact replacements to approved public notes."""

import difflib
import re
from pathlib import Path


def _previews(edits: list[dict], root: Path, public_paths: set[str]) -> dict[Path, tuple[str, str]]:
    paths = {edit.get("path") for edit in edits}
    if not edits or len(paths) > 2:
        raise ValueError("correction must touch one or two files")
    previews = {}
    for name in paths:
        if not isinstance(name, str) or name not in public_paths or not name.startswith("docs/") or not name.endswith(".md"):
            raise ValueError("edit path is not an approved public note")
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to((root / "docs").resolve()):
            raise ValueError("unsafe edit path")
        before = path.read_text(encoding="utf-8")
        spans = []
        frontmatter_end = before.find("\n---\n", 4) + 5 if before.startswith("---\n") else 0
        for edit in [item for item in edits if item["path"] == name]:
            old, new = edit.get("old"), edit.get("new")
            if not isinstance(old, str) or not isinstance(new, str) or not old or old == new or before.count(old) != 1:
                raise ValueError("old text must be unique and change")
            if any(marker in old + new for marker in ("--8<--", "```bash", "```sh", "{%", "{{")) or re.search(r"</?[A-Za-z]", old + new):
                raise ValueError("edit includes executable or templated content")
            start = before.index(old)
            end = start + len(old)
            if start < frontmatter_end or before[:start].count("```") % 2:
                raise ValueError("front matter or code fence edit denied")
            spans.append((start, end, new))
        spans.sort()
        if any(left[1] > right[0] for left, right in zip(spans, spans[1:])):
            raise ValueError("overlapping edits")
        after = before
        for start, end, new in reversed(spans):
            after = after[:start] + new + after[end:]
        previews[path] = (before, after)
    lines = sum(1 for before, after in previews.values()
                for line in difflib.ndiff(before.splitlines(), after.splitlines()) if line.startswith(("+ ", "- ")))
    if lines > 80:
        raise ValueError("diff exceeds 80 changed lines")
    return previews


def validate_edits(edits: list[dict], root: Path, public_paths: set[str]) -> None:
    _previews(edits, root, public_paths)


def apply_edits(edits: list[dict], root: Path) -> dict:
    previews = _previews(edits, root, {edit["path"] for edit in edits})
    for path, (_, after) in previews.items():
        path.write_text(after, encoding="utf-8")
    lines = sum(1 for before, after in previews.values()
                for line in difflib.ndiff(before.splitlines(), after.splitlines()) if line.startswith(("+ ", "- ")))
    return {"files": len(previews), "lines": lines}
