import unittest
import tempfile
import copy
import json
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from notebook_bot.run import load_config, validate_config, admit, verify, evaluate
from notebook_bot.context import resolve_note, build_context
from notebook_bot.github import read_event, read_thread, save_state, discover_events, publish, reconcile
from notebook_bot.model import generate, validate_result
from notebook_bot.patch import validate_edits, apply_edits


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
        event = {"discussion_number": 131, "comment_id": "REPLY", "thread_root_id": "REPLY"}
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


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.context = {"key": "comment:C1", "question": "Is this theorem right?",
                        "notes": [{"path": "docs/math/toc/1.md", "text": "# Theorem\nA implies B", "sha256": "abc"}],
                        "thread": [], "limitations": [], "style_examples": []}
        self.source = {"id": "src-1", "url": "https://example.edu/book", "title": "Book", "excerpt": "A implies B"}
        self.result = {"action": "correction", "answer_md": "这个地方确实写反了，感谢指出。",
                       "sources": [self.source], "claims": [{"text": "原文有误", "source_ids": ["src-1"]}],
                       "edits": [{"path": "docs/math/toc/1.md", "old": "A implies B", "new": "B implies A"}],
                       "reason": "与原始定义相反", "verification": "pass"}

    def test_rejects_claim_with_unobserved_source(self):
        with self.assertRaises(ValueError):
            validate_result(self.result, self.context, [])

    def test_rejects_overlong_reply_and_unsupported_url(self):
        with self.assertRaises(ValueError):
            validate_result({**self.result, "answer_md": "a" * 6001}, self.context, [self.source])
        forged = {**self.result, "sources": [{**self.source, "url": "file:///etc/passwd"}]}
        with self.assertRaises(ValueError):
            validate_result(forged, self.context, [self.source])

    def test_refusal_or_incomplete_output_fails_closed(self):
        responses = [SimpleNamespace(status="incomplete", output_text="", output=[])]
        calls = []
        client = SimpleNamespace(responses=SimpleNamespace(create=lambda **kw: (calls.append(kw), responses.pop(0))[1]))
        with self.assertRaises(ValueError):
            generate(self.context, {"model": "test-model"}, client)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["max_tool_calls"], 3)

    def test_search_then_structured_answer_has_real_source(self):
        annotation = SimpleNamespace(type="url_citation", url="https://example.edu/book", title="Book")
        search = SimpleNamespace(status="completed", output_text="A implies B [source]",
                                 output=[SimpleNamespace(type="message", content=[SimpleNamespace(annotations=[annotation])])])
        result = {**self.result, "action": "answer", "edits": [], "verification": "pass"}
        answer = SimpleNamespace(status="completed", output_text=json.dumps(result), output=[])
        calls = []
        responses = [search, answer]
        client = SimpleNamespace(responses=SimpleNamespace(create=lambda **kw: (calls.append(kw), responses.pop(0))[1]))
        actual = generate(self.context, {"model": "test-model"}, client)
        self.assertEqual(actual["action"], "answer")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["tools"], [{"type": "web_search"}])
        self.assertNotIn("tools", calls[1])

    def test_generated_prompt_includes_author_style_examples(self):
        search = SimpleNamespace(status="completed", output_text="Research", output=[])
        result = {**self.result, "action": "clarify", "sources": [], "claims": [], "edits": []}
        answer = SimpleNamespace(status="completed", output_text=json.dumps(result), output=[])
        calls, responses = [], [search, answer]
        client = SimpleNamespace(responses=SimpleNamespace(create=lambda **kw: (calls.append(kw), responses.pop(0))[1]))
        generate(self.context, {"model": "test-model"}, client)
        self.assertGreater(len(json.loads(calls[1]["input"])["style_examples"]), 0)


class PatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.note = self.root / "docs/math/toc/1.md"
        self.note.parent.mkdir(parents=True)
        self.note.write_text("---\ntitle: Test\n---\nA or B\n", encoding="utf-8")
        self.allowed = {"docs/math/toc/1.md"}

    def test_exact_single_replacement_succeeds(self):
        edit = {"path": "docs/math/toc/1.md", "old": "A or B", "new": "A and B"}
        validate_edits([edit], self.root, self.allowed)
        stats = apply_edits([edit], self.root)
        self.assertIn("A and B", self.note.read_text())
        self.assertEqual(stats["files"], 1)

    def test_ambiguous_and_missing_old_text_fail_without_changes(self):
        edit = {"path": "docs/math/toc/1.md", "old": "A or B", "new": "A and B"}
        self.note.write_text("A or B\nA or B\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_edits([edit], self.root, self.allowed)
        self.note.write_text("A and B\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_edits([edit], self.root, self.allowed)
        self.assertEqual(self.note.read_text(), "A and B\n")

    def test_rejects_nonpublic_symlink_frontmatter_and_large_diff(self):
        bad = {"path": ".github/workflows/deploy.yml", "old": "a", "new": "b"}
        with self.assertRaises(ValueError):
            validate_edits([bad], self.root, self.allowed)
        with self.assertRaises(ValueError):
            validate_edits([{"path": "docs/math/toc/1.md", "old": "title: Test", "new": "title: Better"}], self.root, self.allowed)
        with self.assertRaises(ValueError):
            validate_edits([{"path": "docs/math/toc/1.md", "old": "A or B", "new": "\n".join("line" for _ in range(81))}], self.root, self.allowed)
        other = self.root / "docs/math/toc/other.md"
        other.symlink_to(self.note)
        with self.assertRaises(ValueError):
            validate_edits([{"path": "docs/math/toc/other.md", "old": "A or B", "new": "A and B"}], self.root,
                           self.allowed | {"docs/math/toc/other.md"})

    def test_verify_answer_does_not_modify_source(self):
        candidate = {"context": {"key": "comment:C1", "base_sha": "", "question": "why?"},
                     "result": {"action": "answer", "answer_md": "Because.", "edits": []},
                     "event": {"body_sha256": "abc"}}
        result = verify(candidate, self.root, {"public_paths": list(self.allowed)})
        self.assertEqual(result["diff_stats"], {"files": 0, "lines": 0})
        self.assertEqual(self.note.read_text(), "---\ntitle: Test\n---\nA or B\n")


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.config = {"mode": "auto", "model": "test", "enabled_at": "2026-10-01T00:00:00Z",
                       "public_paths": ["docs/math/toc/1.md"], "bot_login": "notebook-helper[bot]"}
        self.event = {"key": "comment:C1", "discussion_id": "D1", "discussion_number": 1,
                      "comment_id": "C1", "thread_root_id": "C1", "body": "Is this right?",
                      "body_sha256": hashlib.sha256(b"Is this right?").hexdigest(), "actor": "reader", "created_at": "2026-10-02T00:00:00Z"}
        self.reservation = {"key": "comment:C1", "reservation_id": "R1", "event": self.event}
        self.state = {"events": {"comment:C1": {"status": "reserved", "reservation_id": "R1", "attempts": 1}}}
        self.verified = {"key": "comment:C1", "base_sha": "BASE", "body_sha256": self.event["body_sha256"],
                         "allowed_paths": ["docs/math/toc/1.md"], "result": {"action": "answer",
                         "answer_md": "是的，定义成立。", "sources": [{"id": "note-1", "url": "https://note.noughtq.top/math/toc/1",
                         "title": "笔记", "excerpt": "定义"}], "claims": [], "edits": [], "reason": "", "verification": "pass"}}
        self.verified["result_sha256"] = hashlib.sha256(
            json.dumps(self.verified["result"], ensure_ascii=False, sort_keys=True).encode()).hexdigest()

    def fake_api(self, *, stale=False, timeout_after_post=False, forged=False):
        comments = [{"id": "C1", "body": "Is this right?", "author": {"login": "reader"},
                     "createdAt": "2026-10-02T00:00:00Z", "replies": {"nodes": []}}]
        if forged:
            comments[0]["replies"]["nodes"].append({"id": "fake", "body": "<!-- notebook-bot:comment:C1 -->",
                                                      "author": {"login": "reader"}, "createdAt": "2026-10-02T00:01:00Z"})
        posts = []
        def api(method, path, body):
            if method == "GET" and path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": "OTHER" if stale else "BASE"}}
            if path == "/graphql" and "node(id:" in body.get("query", ""):
                return {"data": {"node": {"id": "C1", "body": "Is this right?", "createdAt": "2026-10-02T00:00:00Z",
                                          "author": {"login": "reader"}, "discussion": {"id": "D1", "number": 1,
                                          "body": "https://note.noughtq.top/math/toc/1", "category": {"id": "DIC_kwDOMAb9Zs4CfmpP"}}}}}
            if path == "/graphql" and "discussion(number:" in body.get("query", ""):
                return {"data": {"repository": {"discussion": {"comments": {"nodes": comments,
                    "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}}
            if path == "/graphql" and "addDiscussionComment" in body.get("query", ""):
                node = {"id": "BOT1", "body": body["variables"]["body"],
                        "author": {"login": "notebook-helper[bot]"}, "createdAt": "2026-10-02T00:02:00Z"}
                comments[0]["replies"]["nodes"].append(node)
                posts.append(node)
                if timeout_after_post and len(posts) == 1:
                    raise TimeoutError("response lost")
                return {"data": {"addDiscussionComment": {"comment": {"id": "BOT1"}}}}
            raise AssertionError((method, path))
        return api, posts

    def test_post_timeout_recovers_from_real_bot_reply(self):
        api, posts = self.fake_api(timeout_after_post=True, forged=True)
        with self.assertRaises(TimeoutError):
            publish(self.verified, self.reservation, self.state, api, self.config)
        recovered = publish(self.verified, self.reservation, self.state, api, self.config)
        self.assertEqual(len(posts), 1)
        self.assertEqual(recovered["events"]["comment:C1"]["reply_id"], "BOT1")

    def test_stale_source_prevents_post(self):
        api, posts = self.fake_api(stale=True)
        with self.assertRaises(ValueError):
            publish(self.verified, self.reservation, self.state, api, self.config)
        self.assertEqual(posts, [])

    def test_modified_artifact_cannot_publish(self):
        api, posts = self.fake_api()
        changed = {**self.verified, "result": {**self.verified["result"], "answer_md": "tampered"}}
        with self.assertRaises(ValueError):
            publish(changed, self.reservation, self.state, api, self.config)
        self.assertEqual(posts, [])

    def test_correction_opens_draft_pr_and_reuses_it_after_retry(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"GITHUB_WORKSPACE": tmp}):
            note = Path(tmp) / "docs/math/toc/1.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Claim\nA or B\n", encoding="utf-8")
            api_base, posts = self.fake_api()
            branches, prs = {}, []
            def api(method, path, body):
                if "/pulls?" in path:
                    return prs
                if path.endswith("/git/refs") and method == "POST":
                    branches[body["ref"]] = "A or B"
                    return {"ref": body["ref"]}
                if "/contents/docs/math/toc/1.md" in path:
                    if method == "GET":
                        content = "A or B" if path.endswith("ref=main") else branches[next(iter(branches))]
                        original = note.read_text() if path.endswith("ref=main") else note.read_text().replace("A or B", content)
                        return {"sha": "blob", "content": __import__("base64").b64encode(original.encode()).decode()}
                    branches[next(iter(branches))] = "A and B"
                    return {"content": {"sha": "new"}}
                if path.endswith("/pulls") and method == "POST":
                    pr = {"number": 7, "state": "open", "body": body["body"],
                          "user": {"login": "notebook-helper[bot]"}}
                    prs.append(pr)
                    self.assertTrue(body["draft"])
                    return pr
                return api_base(method, path, body)
            result = {**self.verified["result"], "action": "correction", "reason": "逻辑符号写错",
                      "edits": [{"path": "docs/math/toc/1.md", "old": "A or B", "new": "A and B"}]}
            verified = {**self.verified, "result": result, "build_status": "passed",
                        "diff_stats": {"files": 1, "lines": 2}}
            verified["result_sha256"] = hashlib.sha256(
                json.dumps(result, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            first = publish(verified, self.reservation, self.state, api, self.config)
            again = publish(verified, self.reservation, self.state, api, self.config)
            self.assertEqual((first["events"]["comment:C1"]["pr_number"], len(prs), len(posts)), (7, 1, 1))
            self.assertEqual(again["events"]["comment:C1"]["pr_number"], 7)
            self.assertEqual(note.read_text(), "# Claim\nA or B\n")


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.posts = []
        self.state = {"events": {"comment:C1": {"status": "published", "pr_number": 7,
                       "discussion_id": "D1", "discussion_number": 1, "thread_root_id": "C1", "page_path": "math/toc/1",
                       "expected_text": "A and B"}}, "pull_requests": {}}
        self.config = {"bot_login": "notebook-helper[bot]", "site_url": "https://note.noughtq.top"}

    def api(self, method, path, body):
        if path.endswith("/pulls/7"):
            return {"number": 7, "state": self.pr_state, "merged": self.merged,
                    "merge_commit_sha": "MERGE", "user": {"login": "notebook-helper[bot]"},
                    "body": "<!-- notebook-fix:1234567890abcdef -->"}
        if "/compare/" in path:
            return {"status": self.compare_status}
        if path == "/graphql" and "discussion(number:" in body.get("query", ""):
            comment = {"id": "C1", "body": "Question", "author": {"login": "reader"},
                       "replies": {"nodes": [{"id": "BOT", "body": "Earlier bot answer",
                                               "author": {"login": "notebook-helper[bot]"}}]}}
            connection = {"nodes": [comment], "pageInfo": {"hasNextPage": False, "endCursor": None}}
            return {"data": {"repository": {"discussion": {"comments": connection}}}}
        if path == "/graphql" and "addDiscussionComment" in body.get("query", ""):
            self.posts.append(body["variables"]["body"])
            return {"data": {"addDiscussionComment": {"comment": {"id": "NOTICE"}}}}
        raise AssertionError((method, path))

    def site_get(self, url):
        if url.endswith("bot-deploy.json"):
            return 200, json.dumps({"source_sha": self.deploy_sha})
        return self.page_status, self.page_body

    def test_closed_unmerged_and_failed_deploy_do_not_claim_live(self):
        self.pr_state, self.merged, self.compare_status = "closed", False, "behind"
        self.deploy_sha, self.page_status, self.page_body = "OLD", 200, "A and B"
        closed = reconcile(self.state, self.api, self.site_get, self.config)
        self.assertEqual(closed["pull_requests"]["7"]["status"], "rejected")
        self.pr_state, self.merged = "closed", True
        merged = reconcile(self.state, self.api, self.site_get, self.config)
        self.assertEqual(merged["pull_requests"]["7"]["status"], "pending_deploy")
        self.assertEqual(self.posts, [])

    def test_only_confirmed_site_change_gets_one_notice(self):
        self.pr_state, self.merged, self.compare_status = "closed", True, "ahead"
        self.deploy_sha, self.page_status, self.page_body = "DEPLOY", 200, "<p>A and B</p>"
        updated = reconcile(self.state, self.api, self.site_get, self.config)
        self.assertEqual(updated["pull_requests"]["7"]["status"], "deployed")
        self.assertEqual(len(self.posts), 1)
        self.assertIn("已上线", self.posts[0])
        reconcile(updated, self.api, self.site_get, self.config)
        self.assertEqual(len(self.posts), 1)


class EvaluationTests(unittest.TestCase):
    def test_incomplete_or_style_leaking_dataset_fails_before_model_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = {"model": "test", "public_paths": ["docs/math/toc/1.md"]}
            with self.assertRaises(ValueError):
                evaluate([], config, root)
            style = json.loads(Path("notebook_bot/style.json").read_text())
            case = {"id": "one", "discussion_url": style[0]["discussion_url"],
                    "source_sha": "abc", "question": "Q", "category": "explanation",
                    "expected_facts": ["A"], "expected_action": "answer",
                    "evidence_urls": ["https://example.edu"], "page_path": "docs/math/toc/1.md"}
            with self.assertRaises(ValueError):
                evaluate([case] * 30, config, root)


if __name__ == "__main__":
    unittest.main()
