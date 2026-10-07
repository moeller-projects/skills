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
        "state": get_field("System.State"),
    }
    json.dump(normalized, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
