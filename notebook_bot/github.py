"""GitHub event decoding and API access."""

import hashlib
import base64
import json
import os
import re
from datetime import datetime
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
    return [item for item in found if events[item["key"]]["status"] in {"pending", "retryable"}]
