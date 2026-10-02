import unittest
import tempfile
from pathlib import Path

from notebook_bot.run import load_config, validate_config
from notebook_bot.context import resolve_note, build_context
from notebook_bot.github import read_event, read_thread


class ConfigTests(unittest.TestCase):
    def test_defaults_are_non_publishing(self):
        config = load_config(Path("notebook_bot/config.json"))
        self.assertEqual(
            (config["mode"], config["daily_limit"], config["author_daily_limit"]),
            ("dry-run", 20, 3),
        )

    def test_publish_requires_model_and_public_paths(self):
        config = load_config(Path("notebook_bot/config.json"))
        with self.assertRaises(ValueError):
            validate_config({**config, "model": "", "public_paths": []}, publish=True)


class ContextTests(unittest.TestCase):
    def test_public_page_mapping_rejects_traversal_and_unlisted_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "docs/math/toc/1.md"
            note.parent.mkdir(parents=True)
            note.write_text("# 定义\n公开内容", encoding="utf-8")
            allow = {"docs/math/toc/1.md"}
            self.assertEqual(resolve_note("math/toc/1", root, allow), note)
            self.assertEqual(resolve_note("/math/toc/1.html", root, allow), note)
            self.assertIsNone(resolve_note("../../passwords.yml", root, allow))
            self.assertIsNone(resolve_note("%2e%2e/passwords.yml", root, allow))
            self.assertIsNone(resolve_note("math/toc/1", root, set()))
            note.unlink()
            note.symlink_to(root / "private.md")
            self.assertIsNone(resolve_note("math/toc/1", root, allow))

    def test_event_uses_discussion_node_and_valid_site_path(self):
        payload = {
            "action": "created", "repository": {"full_name": "NoughtQ/notebook"},
            "discussion": {"node_id": "D_131", "number": 131,
                           "body": "https://note.noughtq.top/math/toc/1",
                           "category": {"node_id": "DIC_kwDOMAb9Zs4CfmpP"}},
            "comment": {"node_id": "DC_9", "body": "定义是否有误？",
                        "created_at": "2026-10-02T00:00:00Z", "html_url": "https://github.com/NoughtQ/notebook/discussions/131#discussioncomment-9",
                        "user": {"login": "reader"}},
        }
        event = read_event(payload, None)
        self.assertEqual((event["key"], event["page_path"], event["thread_root_id"]),
                         ("comment:DC_9", "math/toc/1", "DC_9"))
        payload["discussion"]["body"] = "https://evil.example/math/toc/1"
        self.assertIsNone(read_event(payload, None))

    def test_unlisted_include_cannot_enter_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "docs/math/toc/1.md"
            note.parent.mkdir(parents=True)
            note.write_text("# 定义\n--8<-- \"../private.md\"\n公开内容", encoding="utf-8")
            (root / "docs/private.md").write_text("SECRET", encoding="utf-8")
            config = {"public_paths": ["docs/math/toc/1.md"], "site_url": "https://note.noughtq.top"}
            event = {"key": "comment:1", "page_path": "math/toc/1", "body": "定义", "thread_root_id": "1"}
            result = build_context(event, [], root, config)
            self.assertNotIn("SECRET", str(result))
            self.assertTrue(result["limitations"])

    def test_encrypted_include_stays_private_even_if_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "docs/math/toc/1.md"
            page.parent.mkdir(parents=True)
            page.write_text('--8<-- "private.md"', encoding="utf-8")
            (page.parent / "private.md").write_text("---\npassword: hidden\n---\nSECRET", encoding="utf-8")
            config = {"public_paths": ["docs/math/toc/1.md", "docs/math/toc/private.md"]}
            event = {"key": "comment:1", "page_path": "math/toc/1", "body": "question"}
            result = build_context(event, [], root, config)
            self.assertNotIn("SECRET", str(result))

    def test_paginated_reply_finds_its_top_level_thread(self):
        pages = [
            {"nodes": [], "pageInfo": {"hasNextPage": True, "endCursor": "next"}},
            {"nodes": [{"id": "ROOT", "body": "Question", "author": {"login": "reader"},
                        "replies": {"nodes": [{"id": "REPLY", "body": "More detail", "author": {"login": "reader"}}]}}],
             "pageInfo": {"hasNextPage": False, "endCursor": "end"}},
        ]
        def api(method, path, body):
            self.assertEqual((method, path), ("POST", "/graphql"))
            return {"data": {"repository": {"discussion": {"comments": pages.pop(0)}}}}
        event = {"discussion_number": 131, "thread_root_id": "REPLY"}
        thread = read_thread(event, api)
        self.assertEqual((event["thread_root_id"], [item["id"] for item in thread]),
                         ("ROOT", ["ROOT", "REPLY"]))


if __name__ == "__main__":
    unittest.main()
