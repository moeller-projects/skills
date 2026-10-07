#!/usr/bin/env python3
"""validate-output.py

Purpose: Validate Repo Engine output against the repo-map, entrypoint, convention, hotspot, and artifact contract.
Inputs: Contract text on stdin.
Outputs: "OK" on stdout when valid; validation errors on stdout when invalid.
Side effects: None.

Requires Python 3.9+, standard library only. Run with: python scripts/validate-output.py
"""

import re
import sys


def main() -> None:
    input_text = sys.stdin.buffer.read().decode("utf-8")
    errors: list[str] = []

    for section in ["^repo_map:", "^entrypoints:", "^conventions:", "^hotspots:", "^agent_artifacts:"]:
        if re.search(section, input_text, re.MULTILINE) is None:
            errors.append(f"missing section: {section.removeprefix('^')}")

    if re.search(r"^- .+ — .+", input_text, re.MULTILINE) is None:
        errors.append("repo_map entries must include a one-line description")

    if re.search(r"^hotspots:", input_text, re.MULTILINE) is None:
        errors.append("missing hotspots section")
    elif re.search(r"^- .+ — .+", input_text, re.MULTILINE) is None:
        errors.append("hotspots must include a concrete reason")

    if errors:
        print("INVALID output:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("OK")


if __name__ == "__main__":
    main()
