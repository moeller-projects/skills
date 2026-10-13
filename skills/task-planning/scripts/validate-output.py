#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Task Planning task-breakdown output against the required sections and task fields.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stderr when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
Use --help to print usage without reading or validating input.
"""

import re
import sys


def validate(text: str) -> list[str]:
    errors: list[str] = []

    for section in ("tasks:", "dependencies:", "risks:", "critical_path:", "unknowns:", "validation:"):
        if re.search(rf"^{re.escape(section)}", text, re.MULTILINE) is None:
            errors.append(f"missing section: {section}")

    # Parse each task as a local block.  Field counts across the whole document
    # can accidentally satisfy the wrong task, so every requirement is checked
    # between this task's id and the next task id.
    tasks_match = re.search(r"^tasks:\s*\n(?P<body>.*?)(?=^[a-z][a-zA-Z_-]*:|\Z)", text, re.MULTILINE | re.DOTALL)
    tasks_body = tasks_match.group("body") if tasks_match else ""
    task_matches = list(re.finditer(r"^- id:\s*(T-[0-9]+)\s*$", tasks_body, re.MULTILINE))
    malformed_starts = re.findall(r"^- id:\s*(\S.*)$", tasks_body, re.MULTILINE)
    task_ids = [match.group(1) for match in task_matches]
    if not task_ids:
        errors.append("tasks must include at least one substantive task")
    if len(task_ids) != len(set(task_ids)):
        errors.append("task ids must be unique")
    if len(malformed_starts) != len(task_ids):
        errors.append("every task must use a valid - id: T-XX declaration")
    known = set(task_ids)
    dependency_graph: dict[str, list[str]] = {}
    for index, match in enumerate(task_matches):
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(tasks_body)
        block = tasks_body[match.start():end]
        dependency_match = re.search(r"^[ \t]+depends_on:\s*(.*)$", block, re.MULTILINE)
        if not dependency_match:
            dependency_graph[match.group(1)] = []
        else:
            value = dependency_match.group(1).strip()
            if not re.fullmatch(r"\[\s*(?:T-[0-9]+(?:\s*,\s*T-[0-9]+)*)?\s*\]", value):
                errors.append(f"{match.group(1)} depends_on must be a bracketed task-id list")
                dependency_graph[match.group(1)] = []
            else:
                dependency_graph[match.group(1)] = re.findall(r"T-[0-9]+", value)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(task_id: str) -> None:
        if task_id in visiting:
            errors.append(f"dependency graph contains a cycle at {task_id}")
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in dependency_graph.get(task_id, []):
            if dependency in known:
                visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in task_ids:
        visit(task_id)
    for index, match in enumerate(task_matches):
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(tasks_body)
        block = tasks_body[match.start():end]
        task_id = match.group(1)
        if not re.search(r"^[ \t]+title:\s*\S", block, re.MULTILINE):
            errors.append(f"{task_id} must have a substantive title")
        if not re.search(r"^[ \t]+done_when:\s*\S", block, re.MULTILINE):
            errors.append(f"{task_id} must have a done_when condition")
        if not re.search(r"^[ \t]+estimate:\s*[SML]\s*$", block, re.MULTILINE) and not re.search(r"^[ \t]+timebox:\s*\S", block, re.MULTILINE):
            errors.append(f"{task_id} must have an estimate (S/M/L) or a timebox")
        if not re.search(r"^[ \t]+estimate_reliability:\s*(?:high|low)\s*$", block, re.MULTILINE):
            errors.append(f"{task_id} must have estimate_reliability: high|low")
        depends = re.search(r"^[ \t]+depends_on:\s*(.*)$", block, re.MULTILINE)
        if not depends:
            errors.append(f"{task_id} must have depends_on")
        else:
            for dep in re.findall(r"T-[0-9]+", depends.group(1)):
                if dep not in known:
                    errors.append(f"{task_id} depends_on unknown task {dep}")

    critical = re.search(r"^critical_path:\s*\n(?P<body>.*?)(?=^[a-z][a-zA-Z_-]*:|\Z)", text, re.MULTILINE | re.DOTALL)
    if critical:
        path_ids = re.findall(r"\bT-[0-9]+\b", critical.group("body"))
        for referenced in path_ids:
            if referenced not in known:
                errors.append(f"critical_path references unknown task {referenced}")
        if not path_ids and task_ids:
            errors.append("critical_path must list planned task ids")
        for source, target in zip(path_ids, path_ids[1:]):
            if source not in dependency_graph.get(target, []):
                errors.append(f"critical_path edge {source} → {target} is not a declared dependency")
    dependencies_match = re.search(r"^dependencies:\s*\n(?P<body>.*?)(?=^[a-z][a-zA-Z_-]*:|\Z)", text, re.MULTILINE | re.DOTALL)
    if dependencies_match:
        dependency_text = dependencies_match.group("body")
        if not re.fullmatch(r"\s*-\s*(?:none|no dependencies)\s*", dependency_text, re.IGNORECASE):
            for source, target in re.findall(r"\b(T-[0-9]+)\s*(?:→|->)\s*(T-[0-9]+)\b", dependency_text):
                if source not in known or target not in known:
                    errors.append(f"dependencies section references unknown task in {source} → {target}")
                elif source not in dependency_graph.get(target, []):
                    errors.append(f"dependencies edge {source} → {target} contradicts {target} depends_on")
    return errors

def main() -> None:
    if "--help" in sys.argv[1:]:
        print("Usage: python scripts/validate-output.py < output.txt")
        print("Validate Task Planning output from standard input.")
        return
    errors = validate(sys.stdin.read())
    if errors:
        print("INVALID output:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
