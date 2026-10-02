"""GitHub event decoding and API access."""

import hashlib
import base64
import json
import os
import re
import copy
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote
from urllib.error import HTTPError
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def request(method: str, path: str, body: dict | None) -> dict:
    token = os.environ["GITHUB_TOKEN"]
    data = json.dumps(body).encode() if body is not None else None
    req = Request("https://api.github.com" + path, data=data, method=method,
                  headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                           "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"})
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def read_event(payload: dict, api) -> dict | None:
    if payload.get("action") != "created" or payload.get("repository", {}).get("full_name", "").lower() != "noughtq/notebook":
        return None
    discussion = payload.get("discussion") or {}
    if discussion.get("category", {}).get("node_id") != "DIC_kwDOMAb9Zs4CfmpP":
        return None
    links = re.findall(r"https?://[^\s<>]+", discussion.get("body", ""))
    paths = [urlparse(link.rstrip(").,，")).path for link in links
             if urlparse(link.rstrip(").,，")).scheme == "https" and urlparse(link.rstrip(").,，")).netloc == "note.noughtq.top"]
    if len(set(paths)) != 1:
        return None
    comment = payload.get("comment")
    source = comment or discussion
    node = source.get("node_id")
    if not node:
        return None
    body = source.get("body", "")
    return {"repo": "NoughtQ/notebook", "discussion_id": discussion["node_id"],
            "discussion_number": discussion["number"], "comment_id": comment.get("node_id") if comment else None,
            "thread_root_id": comment.get("node_id") if comment else discussion["node_id"],
            "key": ("comment:" if comment else "discussion:") + node,
            "actor": source.get("user", {}).get("login", ""), "body": body,
            "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "created_at": source.get("created_at", ""), "url": source.get("html_url", ""),
            "page_path": paths[0].strip("/").removesuffix(".html")}


def read_thread(event: dict, api) -> list[dict]:
    query = """query($number:Int!,$after:String){repository(owner:"NoughtQ",name:"notebook"){
      discussion(number:$number){comments(first:100,after:$after){pageInfo{hasNextPage endCursor}
        nodes{id body author{login} createdAt replies(first:100){nodes{id body author{login} createdAt}}}}}}}"""
    after = None
    comments = []
    while True:
        data = api("POST", "/graphql", {"query": query, "variables": {"number": event["discussion_number"], "after": after}})
        connection = data["data"]["repository"]["discussion"]["comments"]
        comments.extend(connection["nodes"])
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]
    if event.get("comment_id") is None:
        return [item for comment in comments for item in [comment, *comment["replies"]["nodes"]]]
    root_id = event["thread_root_id"]
    for item in comments:
        if item["id"] == root_id or any(reply["id"] == root_id for reply in item["replies"]["nodes"]):
            event["thread_root_id"] = item["id"]
            return [item, *item["replies"]["nodes"]]
    return []


def save_state(api, state: dict, expected_sha: str) -> str:
    body = {"message": "bot: update state", "branch": "bot-state",
            "content": base64.b64encode((json.dumps(state, ensure_ascii=False, sort_keys=True) + "\n").encode()).decode()}
    if expected_sha:
        body["sha"] = expected_sha
    result = api("PUT", "/repos/NoughtQ/notebook/contents/state.json", body)
    return result["content"]["sha"]


def discover_events(api, state: dict, config: dict) -> list[dict]:
    if config["mode"] == "off":
        return []
    query = """query($after:String){repository(owner:"NoughtQ",name:"notebook"){
      discussions(first:100,after:$after,orderBy:{field:UPDATED_AT,direction:DESC}){
        pageInfo{hasNextPage endCursor} nodes{id number body createdAt url author{login}
          category{id} comments(first:100){pageInfo{hasNextPage endCursor}
            nodes{id body createdAt url author{login}
              replies(first:100){nodes{id body createdAt url author{login}}}}}}}}}}"""
    more_comments = """query($number:Int!,$after:String){repository(owner:"NoughtQ",name:"notebook"){
      discussion(number:$number){comments(first:100,after:$after){pageInfo{hasNextPage endCursor}
        nodes{id body createdAt url author{login}
          replies(first:100){nodes{id body createdAt url author{login}}}}}}}}}"""
    found = []
    after = None
    while True:
        data = api("POST", "/graphql", {"query": query, "variables": {"after": after}})
        connection = data["data"]["repository"]["discussions"]
        for discussion in connection["nodes"]:
            base = {"repository": {"full_name": "NoughtQ/notebook"},
                    "discussion": {"node_id": discussion["id"], "number": discussion["number"],
                                   "body": discussion["body"], "created_at": discussion["createdAt"],
                                   "html_url": discussion["url"], "user": discussion["author"],
                                   "category": {"node_id": discussion["category"]["id"]}}}
            direct = read_event({**base, "action": "created"}, api)
            if direct and direct["created_at"] >= config["enabled_at"]:
                found.append(direct)
            comments = discussion["comments"]
            nodes = list(comments["nodes"])
            cursor = comments["pageInfo"]
            while cursor["hasNextPage"]:
                data = api("POST", "/graphql", {"query": more_comments,
                            "variables": {"number": discussion["number"], "after": cursor["endCursor"]}})
                next_page = data["data"]["repository"]["discussion"]["comments"]
                nodes.extend(next_page["nodes"])
                cursor = next_page["pageInfo"]
            for comment in nodes:
                for item in [comment, *comment["replies"]["nodes"]]:
                    payload = {**base, "action": "created", "comment": {
                        "node_id": item["id"], "body": item["body"], "created_at": item["createdAt"],
                        "html_url": item["url"], "user": item["author"]}}
                    event = read_event(payload, api)
                    if event and event["created_at"] >= config["enabled_at"]:
                        event["thread_root_id"] = comment["id"]
                        found.append(event)
        if not connection["pageInfo"]["hasNextPage"]:
            break
        after = connection["pageInfo"]["endCursor"]
    found.sort(key=lambda item: (item["created_at"], item["key"]))
    # ponytail: full scan of the current Discussions corpus; add an indexed queue if API time becomes material.
    events = state.setdefault("events", {})
    for item in found:
        events.setdefault(item["key"], {"status": "pending", "pointer": {
            "discussion_number": item["discussion_number"], "comment_id": item["comment_id"]}})
    state["scan_watermark"] = datetime.now().astimezone().isoformat()
    now = datetime.now(timezone.utc)
    return [item for item in found if events[item["key"]]["status"] in {"pending", "retryable"} or (
        events[item["key"]]["status"] == "reserved" and
        events[item["key"]].get("reserved_at") and
        now - datetime.fromisoformat(events[item["key"]]["reserved_at"]) >= timedelta(minutes=15))]


def _fresh_event(event: dict, api) -> dict:
    if event.get("comment_id"):
        query = """query($id:ID!){node(id:$id){... on DiscussionComment{
          id body createdAt url author{login} discussion{id number body category{id}}}}}"""
        data = api("POST", "/graphql", {"query": query, "variables": {"id": event["comment_id"]}})
        node = data["data"]["node"]
        if not node:
            raise ValueError("question was deleted")
        discussion = node["discussion"]
        payload = {"action": "created", "repository": {"full_name": "NoughtQ/notebook"},
                   "discussion": {"node_id": discussion["id"], "number": discussion["number"],
                                  "body": discussion["body"], "category": {"node_id": discussion["category"]["id"]}},
                   "comment": {"node_id": node["id"], "body": node["body"], "created_at": node["createdAt"],
                               "html_url": node.get("url", ""), "user": node["author"]}}
    else:
        query = """query($id:ID!){node(id:$id){... on Discussion{
          id number body createdAt url author{login} category{id}}}}"""
        data = api("POST", "/graphql", {"query": query, "variables": {"id": event["discussion_id"]}})
        node = data["data"]["node"]
        if not node:
            raise ValueError("discussion was deleted")
        payload = {"action": "created", "repository": {"full_name": "NoughtQ/notebook"},
                   "discussion": {"node_id": node["id"], "number": node["number"], "body": node["body"],
                                  "created_at": node["createdAt"], "html_url": node["url"], "user": node["author"],
                                  "category": {"node_id": node["category"]["id"]}}}
    fresh = read_event(payload, api)
    if fresh is None:
        raise ValueError("discussion is no longer eligible")
    return fresh


def _correction_pr(verified: dict, event: dict, api, config: dict) -> int:
    from .patch import validate_edits

    edits = verified["result"]["edits"]
    if verified.get("build_status") != "passed":
        raise ValueError("correction build did not pass")
    root = Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd()))
    validate_edits(edits, root, set(config["public_paths"]))
    key = hashlib.sha256((event["thread_root_id"] + "|" + "|".join(
        edit["path"] + ":" + edit["old"] for edit in edits)).encode()).hexdigest()[:16]
    branch = f"bot/fix-{key}"
    marker = f"<!-- notebook-fix:{key} -->"
    prs = api("GET", "/repos/NoughtQ/notebook/pulls?state=all&head=" + quote("NoughtQ:" + branch), None)
    for pr in prs:
        if pr["user"]["login"].lower() == config["bot_login"].lower() and marker in pr.get("body", ""):
            if pr["state"] != "open":
                raise ValueError("the previous correction PR was closed")
            return pr["number"]
    try:
        api("POST", "/repos/NoughtQ/notebook/git/refs", {"ref": "refs/heads/" + branch,
                                                          "sha": verified["base_sha"]})
    except HTTPError as exc:
        if exc.code != 422:
            raise
    grouped = {}
    for edit in edits:
        grouped.setdefault(edit["path"], []).append(edit)
    for path, file_edits in grouped.items():
        main = api("GET", f"/repos/NoughtQ/notebook/contents/{quote(path)}?ref=main", None)
        current = api("GET", f"/repos/NoughtQ/notebook/contents/{quote(path)}?ref={quote(branch)}", None)
        original = base64.b64decode(main["content"]).decode("utf-8")
        if original != (root / path).read_text(encoding="utf-8"):
            raise ValueError("main content differs from trusted checkout")
        updated = original
        for edit in file_edits:
            if updated.count(edit["old"]) != 1:
                raise ValueError("source changed during PR creation")
            updated = updated.replace(edit["old"], edit["new"], 1)
        branch_text = base64.b64decode(current["content"]).decode("utf-8")
        if branch_text == updated:
            continue
        if branch_text != original:
            raise ValueError("bot branch was changed by someone else")
        api("PUT", f"/repos/NoughtQ/notebook/contents/{quote(path)}", {
            "message": "fix: correct note from discussion", "branch": branch, "sha": current["sha"],
            "content": base64.b64encode(updated.encode()).decode()})
    body = (f"来源：{event['url']}\n\n原因：{verified['result']['reason']}\n\n"
            f"证据：" + "、".join(source["url"] for source in verified["result"]["sources"]) +
            f"\n\n验证：public build passed; {verified['diff_stats']}\n\n{marker}")
    pr = api("POST", "/repos/NoughtQ/notebook/pulls", {"title": "fix: correct note from discussion",
                                                         "head": branch, "base": "main", "body": body, "draft": True})
    return pr["number"]


def publish(verified: dict, reservation: dict, state: dict, api, config: dict) -> dict:
    from .run import validate_config

    validate_config(config, publish=True)
    digest = hashlib.sha256(json.dumps(verified["result"], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if digest != verified.get("result_sha256"):
        raise ValueError("verified answer was modified")
    key = reservation["key"]
    if key != verified["key"]:
        raise ValueError("reservation and answer mismatch")
    state = copy.deepcopy(state)
    record = state["events"].get(key, {})
    if record.get("status") == "published":
        return state
    if record.get("reservation_id") != reservation["reservation_id"]:
        raise ValueError("reservation is no longer current")
    event = _fresh_event(reservation["event"], api)
    if event["body_sha256"] != verified["body_sha256"]:
        raise ValueError("question was edited")
    if api("GET", "/repos/NoughtQ/notebook/git/ref/heads/main", None)["object"]["sha"] != verified["base_sha"]:
        raise ValueError("notes changed since generation")
    thread = read_thread(event, api)
    if any(item.get("author", {}).get("login", "").lower() == "noughtq" and
           item.get("createdAt", "") > event["created_at"] for item in thread):
        raise ValueError("site owner took over this thread")
    marker = f"<!-- notebook-bot:{key} -->"
    bot = config["bot_login"].lower()
    existing = next((item for item in thread if item.get("author", {}).get("login", "").lower() == bot
                     and marker in item.get("body", "")), None)
    pr_number = record.get("pr_number")
    result = verified["result"]
    if result["action"] == "correction" and not pr_number:
        pr_number = _correction_pr(verified, event, api, config)
    if result["action"] == "skip":
        record["status"] = "skipped"
        return state
    if existing is None:
        sources = "\n".join(f"- [{source['title']}]({source['url']})" for source in result.get("sources", []))
        answer = result["answer_md"]
        if pr_number:
            answer += f"\n\n已提交纠错 PR #{pr_number}，待站长审核。"
        body = (answer + ("\n\n参考：\n" + sources if sources else "") +
                "\n\n本回复由笔记助手自动生成，笔记修改需经站长审核。\n" + marker)
        if len(body) > 6000:
            raise ValueError("published reply exceeds 6000 characters")
        query = """mutation($discussionId:ID!,$replyToId:ID,$body:String!){
          addDiscussionComment(input:{discussionId:$discussionId,replyToId:$replyToId,body:$body}){comment{id}}}"""
        response = api("POST", "/graphql", {"query": query, "variables": {
            "discussionId": event["discussion_id"], "replyToId": event["thread_root_id"] if event["comment_id"] else None,
            "body": body}})
        reply_id = response["data"]["addDiscussionComment"]["comment"]["id"]
    else:
        reply_id = existing["id"]
    record.update({"status": "published", "reply_id": reply_id, "pr_number": pr_number})
    return state
