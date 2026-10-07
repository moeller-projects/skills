#!/usr/bin/env python3
"""normalize-work-item.py
Purpose: Normalize a raw Azure DevOps work item payload into the shared work-item contract shape.
Inputs: Raw Azure DevOps work item JSON on stdin.
Outputs: Normalized work item JSON on stdout.
Side effects: None.
Requires Python 3.9+, standard library only. Run with: python scripts/normalize-work-item.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "div", "ul", "ol", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def normalize_html(value: str) -> str:
    if not value:
        return ""
    parser = TextExtractor()
    parser.feed(value)
    text = html.unescape("".join(parser.parts))
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return lib.redact_text(text.strip()) or ""


_HTML_FIELD_NAMES = {
    "System.Description",
    "Microsoft.VSTS.Common.AcceptanceCriteria",
    "Custom.AcceptanceCriteria",
    "Microsoft.VSTS.TCM.ReproSteps",
    "Custom.ReproSteps",
    "Microsoft.VSTS.TCM.SystemInfo",
    "Custom.SystemInfo",
}


def normalize_history_value(value: object, field_name: str) -> object:
    if isinstance(value, str):
        if field_name in _HTML_FIELD_NAMES:
            return normalize_html(value)
        return lib.redact_text(value) or ""
    if isinstance(value, list):
        return [normalize_history_value(item, field_name) for item in value]
    if isinstance(value, dict):
        return {
            key: normalize_history_value(item, field_name)
            for key, item in value.items()
        }
    return value


def normalize_identifier(value: object) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def normalize_history(updates: object) -> list[dict]:
    if not isinstance(updates, list):
        return []
    history = []
    for update in updates:
        if not isinstance(update, dict):
            continue
        changed_fields = []
        fields = update.get("fields")
        if isinstance(fields, dict):
            for reference_name, values in fields.items():
                if not isinstance(values, dict):
                    continue
                change = {"reference_name": reference_name}
                for source_name, output_name in (("oldValue", "old_value"), ("newValue", "new_value")):
                    if source_name in values:
                        change[output_name] = normalize_history_value(values[source_name], reference_name)
                changed_fields.append(change)
        revised_by = update.get("revisedBy")
        if isinstance(revised_by, dict):
            revised_by = revised_by.get("displayName") or revised_by.get("name")
        history.append({
            "update_id": normalize_identifier(update.get("id")),
            "revision": normalize_identifier(update.get("rev")),
            "revised_by": lib.redact_text(revised_by) if isinstance(revised_by, str) else None,
            "revised_date": update.get("revisedDate"),
            "changed_fields": changed_fields,
        })
    return history


def normalize_related_work(relations: object) -> list[dict]:
    if not isinstance(relations, list):
        return []
    related_work = []
    for relation in relations:
        if not isinstance(relation, dict) or relation.get("rel") != "System.LinkTypes.Related":
            continue
        related_work.append({
            "rel": relation["rel"],
            "url": lib.redact_text(relation.get("url")) if isinstance(relation.get("url"), str) else None,
            "attributes": normalize_history_value(relation.get("attributes"), "")
            if isinstance(relation.get("attributes"), dict)
            else {},
        })
    return related_work


def main() -> None:
    payload = json.load(sys.stdin)
    fields = payload.get("fields", {})
    work_item_type = fields.get("System.WorkItemType", "")

    def get_field(*names: str) -> str:
        for name in names:
            value = fields.get(name)
            if value is not None:
                return str(value)
        return ""

    repro = ""
    system_info = ""
    if work_item_type == "Bug":
        repro = normalize_html(get_field("Microsoft.VSTS.TCM.ReproSteps", "Custom.ReproSteps"))
        system_info = normalize_html(get_field("Microsoft.VSTS.TCM.SystemInfo", "Custom.SystemInfo"))

    work_item_id = payload.get("id")
    if isinstance(work_item_id, str) and work_item_id.isdigit():
        work_item_id = int(work_item_id)
    elif not isinstance(work_item_id, int):
        work_item_id = None

    normalized = {
        "id": work_item_id,
        "type": work_item_type,
        "title": lib.redact_text(get_field("System.Title")) or "",
        "description": normalize_html(get_field("System.Description")),
        "acceptance_criteria": normalize_html(get_field("Microsoft.VSTS.Common.AcceptanceCriteria", "Custom.AcceptanceCriteria")),
        "repro_steps": repro,
        "system_info": system_info,
        "tags": get_field("System.Tags"),
        "comments": [
            {
                "id": comment.get("id"),
                "author": lib.redact_text(
                    ((comment.get("createdBy") or {}).get("displayName", ""))
                    if isinstance(comment.get("createdBy") or {}, dict)
                    else ""
                ) or "",
                "content": normalize_html(comment.get("text", "")),
                "created_date": comment.get("createdDate"),
                "modified_date": comment.get("modifiedDate"),
            }
            for comment in payload.get("comments", [])
            if isinstance(comment, dict)
        ],
        "history": normalize_history(payload.get("updates")),
        "related_work": normalize_related_work(payload.get("relations")),
    }
    json.dump(normalized, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
