"""Bounded OpenAI research and structured answer generation."""

import json
import re
from pathlib import Path
from urllib.parse import urlparse


SOURCE = {"type": "object", "additionalProperties": False,
          "properties": {name: {"type": "string"} for name in ("id", "url", "title", "excerpt")},
          "required": ["id", "url", "title", "excerpt"]}
CLAIM = {"type": "object", "additionalProperties": False,
         "properties": {"text": {"type": "string"}, "source_ids": {"type": "array", "items": {"type": "string"}}},
         "required": ["text", "source_ids"]}
EDIT = {"type": "object", "additionalProperties": False,
        "properties": {name: {"type": "string"} for name in ("path", "old", "new")},
        "required": ["path", "old", "new"]}
RESULT_SCHEMA = {"type": "object", "additionalProperties": False,
                 "properties": {"action": {"type": "string", "enum": ["skip", "clarify", "answer", "correction"]},
                                "answer_md": {"type": "string"},
                                "sources": {"type": "array", "items": SOURCE},
                                "claims": {"type": "array", "items": CLAIM},
                                "edits": {"type": "array", "items": EDIT},
                                "reason": {"type": "string"},
                                "verification": {"type": "string", "enum": ["pass", "reject", "uncertain"]}},
                 "required": ["action", "answer_md", "sources", "claims", "edits", "reason", "verification"]}


def validate_result(result: dict, context: dict, observed_sources: list[dict]) -> None:
    if result.get("action") not in {"skip", "clarify", "answer", "correction"}:
        raise ValueError("invalid action")
    if len(result.get("answer_md", "")) > 6000:
        raise ValueError("answer exceeds limit")
    observed = {source["id"]: source for source in observed_sources}
    for source in result.get("sources", []):
        url = urlparse(source["url"])
        if url.scheme not in {"http", "https"} or not url.netloc or source["id"] not in observed or observed[source["id"]]["url"] != source["url"]:
            raise ValueError("unobserved or unsafe source")
    chosen = {source["id"] for source in result.get("sources", [])}
    for claim in result.get("claims", []):
        if not claim.get("source_ids") or any(source_id not in chosen for source_id in claim["source_ids"]):
            raise ValueError("unsupported claim")
    if result["action"] in {"answer", "correction"} and not chosen:
        raise ValueError("answer lacks sources")
    if result["action"] == "correction":
        if not result.get("edits") or not result.get("reason") or not result.get("claims"):
            raise ValueError("correction lacks evidence or edit")
        if any("图片未核验" in limitation for limitation in context.get("limitations", [])):
            raise ValueError("image-dependent correction requires review")
    elif result.get("edits"):
        raise ValueError("non-correction cannot edit")


def _sources(response) -> list[dict]:
    sources = []
    for item in response.output:
        for content in getattr(item, "content", []):
            for annotation in getattr(content, "annotations", []):
                if getattr(annotation, "type", "") != "url_citation":
                    continue
                url = annotation.url
                if url not in {source["url"] for source in sources}:
                    sources.append({"id": f"src-{len(sources) + 1}", "url": url,
                                    "title": getattr(annotation, "title", url),
                                    "excerpt": response.output_text[:700]})
    return sources


def _completed(response) -> str:
    if response.status != "completed" or not response.output_text:
        raise ValueError("OpenAI response incomplete or refused")
    if any(getattr(content, "type", "") == "refusal" for item in response.output
           for content in getattr(item, "content", [])):
        raise ValueError("OpenAI refused")
    return response.output_text


def generate(context: dict, config: dict, client) -> dict:
    if len(json.dumps(context, ensure_ascii=False)) > 60000:
        raise ValueError("context exceeds request limit")
    model = config["model"]
    prompt = Path(__file__).with_name("prompt.md").read_text(encoding="utf-8")
    research = client.responses.create(model=model, store=False, max_output_tokens=4096,
                                       max_tool_calls=3, tools=[{"type": "web_search"}],
                                       tool_choice="required", instructions=prompt,
                                       input=json.dumps({"question": context["question"], "notes": context["notes"],
                                                         "limitations": context.get("limitations", [])}, ensure_ascii=False))
    research_text = _completed(research)
    sources = _sources(research)
    note_sources = [{"id": f"note-{index + 1}", "url": "https://note.noughtq.top/" + note["path"][5:-3],
                     "title": note["path"], "excerpt": note["text"][:700]}
                    for index, note in enumerate(context["notes"])]
    observed = sources + note_sources
    styles = json.loads(Path(__file__).with_name("style.json").read_text(encoding="utf-8"))
    terms = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]+|[\u4e00-\u9fff]{2,}", context["question"].lower()))
    examples = sorted(styles, key=lambda item: sum(term in item["question"].lower() for term in terms), reverse=True)[:3]
    material = {"context": context, "research": research_text[:12000], "observed_sources": observed,
                "style_examples": [{"question": item["question"], "reply": item["reply"]} for item in examples]}
    if len(json.dumps(material, ensure_ascii=False)) > 60000:
        raise ValueError("research context exceeds request limit")
    answer = client.responses.create(model=model, store=False, max_output_tokens=4096,
                                     instructions=prompt, input=json.dumps(material, ensure_ascii=False),
                                     text={"format": {"type": "json_schema", "name": "note_answer",
                                                      "strict": True, "schema": RESULT_SCHEMA}})
    result = json.loads(_completed(answer))
    validate_result(result, context, observed)
    if result["action"] == "correction":
        verification = client.responses.create(model=model, store=False, max_output_tokens=4096,
                                               instructions="独立核验纠错：比较笔记原文、题目假设和来源摘录。只输出 JSON：verification 为 pass/reject/uncertain，reason 为简短理由。证据不足选 uncertain。",
                                               input=json.dumps({"result": result, "notes": context["notes"], "sources": observed}, ensure_ascii=False),
                                               text={"format": {"type": "json_schema", "name": "note_verification",
                                                                "strict": True, "schema": {"type": "object", "additionalProperties": False,
                                                                                           "properties": {"verification": {"type": "string", "enum": ["pass", "reject", "uncertain"]},
                                                                                                          "reason": {"type": "string"}},
                                                                                           "required": ["verification", "reason"]}}})
        verdict = json.loads(_completed(verification))
        result["verification"] = verdict["verification"]
        if verdict["verification"] != "pass":
            result["action"] = "clarify"
            result["edits"] = []
            result["answer_md"] = "这处可能需要修正，但目前证据不足以确认。" + verdict["reason"]
    return result
