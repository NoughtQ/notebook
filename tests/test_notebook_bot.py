import unittest
import tempfile
import copy
from datetime import datetime, timezone
from pathlib import Path

from notebook_bot.run import load_config, validate_config, admit
from notebook_bot.context import resolve_note, build_context
from notebook_bot.github import read_event, read_thread, save_state, discover_events


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


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 2, 12, tzinfo=timezone.utc)
        self.config = {"mode": "auto", "enabled_at": "2026-10-01T00:00:00Z",
                       "daily_limit": 20, "author_daily_limit": 3, "bot_login": "notebook-helper[bot]"}
        self.event = {"key": "comment:DC1", "actor": "reader", "body": "Where is the proof?",
                      "created_at": "2026-10-02T11:00:00Z", "thread_root_id": "ROOT",
                      "discussion_id": "D1", "comment_id": "DC1"}

    def test_duplicate_does_not_consume_second_reservation(self):
        state, first = admit(self.event, {}, self.config, self.now)
        again, second = admit(self.event, state, self.config, self.now)
        self.assertIsNotNone(first)
        self.assertIsNone(second)
        self.assertEqual(again["daily"], state["daily"])

    def test_scanned_pending_event_can_be_reserved(self):
        state = {"events": {self.event["key"]: {"status": "pending", "pointer": {"discussion_number": 1}}}}
        updated, reservation = admit(self.event, state, self.config, self.now)
        self.assertIsNotNone(reservation)
        self.assertEqual(updated["events"][self.event["key"]]["status"], "reserved")

    def test_expired_reservation_can_retry_once(self):
        state = {"events": {self.event["key"]: {"status": "reserved", "attempts": 1,
                                               "reserved_at": "2026-10-02T11:00:00+00:00"}}}
        updated, reservation = admit(self.event, state, self.config, self.now)
        self.assertEqual(reservation["attempt"], 2)
        self.assertEqual(updated["events"][self.event["key"]]["attempts"], 2)

    def test_author_and_global_caps_delay_without_charging(self):
        state = {}
        for number in range(3):
            event = {**self.event, "key": f"comment:{number}"}
            state, reservation = admit(event, state, self.config, self.now)
            self.assertIsNotNone(reservation)
        state2, fourth = admit({**self.event, "key": "comment:4"}, state, self.config, self.now)
        self.assertIsNone(fourth)
        self.assertEqual(state2["daily"], state["daily"])
        full = copy.deepcopy(state)
        full["daily"]["2026-10-02"]["total"] = 20
        self.assertIsNone(admit({**self.event, "key": "comment:5", "actor": "other"}, full, self.config, self.now)[1])

    def test_old_bot_and_off_events_are_ignored(self):
        for change in ({"created_at": "2026-09-30T00:00:00Z"}, {"actor": "notebook-helper[bot]"}):
            self.assertIsNone(admit({**self.event, **change}, {}, self.config, self.now)[1])
        self.assertIsNone(admit(self.event, {}, {**self.config, "mode": "off"}, self.now)[1])

    def test_time_comparison_accepts_equivalent_utc_formats(self):
        same_instant = {**self.event, "created_at": "2026-10-01T00:00:00+00:00"}
        self.assertIsNotNone(admit(same_instant, {}, self.config, self.now)[1])

    def test_mention_requires_standalone_ask_command(self):
        config = {**self.config, "mode": "mention"}
        self.assertIsNone(admit({**self.event, "body": "/asking about notes"}, {}, config, self.now)[1])
        self.assertIsNotNone(admit({**self.event, "body": "/ask\nWhat is this?"}, {}, config, self.now)[1])

    def test_owner_pauses_only_this_thread_and_can_resume(self):
        owner = {**self.event, "actor": "NoughtQ", "body": "I will answer", "key": "comment:owner"}
        state, reservation = admit(owner, {}, self.config, self.now)
        self.assertIsNone(reservation)
        self.assertIn("ROOT", state["paused_threads"])
        self.assertIsNone(admit(self.event, state, self.config, self.now)[1])
        other = {**self.event, "key": "comment:other", "thread_root_id": "OTHER"}
        self.assertIsNotNone(admit(other, state, self.config, self.now)[1])
        resume = {**owner, "key": "comment:resume", "body": "/bot resume"}
        state, _ = admit(resume, state, self.config, self.now)
        self.assertNotIn("ROOT", state["paused_threads"])

    def test_save_state_passes_cas_sha_to_api(self):
        seen = []
        def api(method, path, body):
            seen.append((method, path, body))
            return {"content": {"sha": "new-sha"}}
        new_sha = save_state(api, {"version": 1, "events": {}}, "old-sha")
        self.assertEqual(new_sha, "new-sha")
        self.assertEqual(seen[0][2]["sha"], "old-sha")

    def test_scan_keeps_new_comment_on_old_discussion(self):
        discussion = {"id": "D1", "number": 1, "body": "https://note.noughtq.top/math/toc/1",
                      "createdAt": "2025-01-01T00:00:00Z", "url": "https://github.com/NoughtQ/notebook/discussions/1",
                      "author": {"login": "reader"}, "category": {"id": "DIC_kwDOMAb9Zs4CfmpP"},
                      "comments": {"nodes": [{"id": "C1", "body": "Is this correct?",
                                              "createdAt": "2026-10-02T10:00:00Z", "url": "https://github.com/comment/1",
                                              "author": {"login": "reader"}, "replies": {"nodes": []}}],
                                   "pageInfo": {"hasNextPage": False, "endCursor": None}}}
        def api(method, path, body):
            return {"data": {"repository": {"discussions": {
                "nodes": [discussion], "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}
        state = {}
        events = discover_events(api, state, self.config)
        self.assertEqual([item["key"] for item in events], ["comment:C1"])
        self.assertEqual(state["events"]["comment:C1"]["status"], "pending")

    def test_scan_failure_does_not_advance_state(self):
        state = {"events": {}, "scan_watermark": "old"}
        def broken_api(method, path, body):
            raise TimeoutError("GitHub unavailable")
        with self.assertRaises(TimeoutError):
            discover_events(broken_api, state, self.config)
        self.assertEqual(state, {"events": {}, "scan_watermark": "old"})


if __name__ == "__main__":
    unittest.main()
