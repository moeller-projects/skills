#!/usr/bin/env python3
"""parse-git-remote.py
Purpose: Parse Azure DevOps git remote identifiers without network access.
Inputs: One remote URL on stdin; never pass a credential-bearing URL in argv.
Outputs: Identifier JSON on stdout; structured BLOCKER output on stderr.
Side effects: None.
Requires Python 3.9+, standard library only. Run with: git remote get-url origin | python scripts/parse-git-remote.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def _valid_identifier(value: str) -> bool:
    return bool(value.strip()) and len(value) <= 256 and value not in (".", "..") and not any(
        ord(ch) < 32 or ord(ch) == 127 or ch in "/\\?#%" for ch in value
    )


def _decode(parts: list[str]) -> list[str] | None:
    values = [urllib.parse.unquote(part) for part in parts]
    return values if all(_valid_identifier(value) for value in values) else None


def _path_parts(path: str) -> list[str]:
    return [part for part in path.strip("/").split("/")]


def parse_remote(raw: str) -> dict | None:
    remote = raw.strip()
    if not remote:
        return None
    try:
        parsed = urllib.parse.urlsplit(remote)
    except ValueError:
        return None
    if parsed.query or parsed.fragment:
        return None
    host = (parsed.hostname or "").lower()
    path = parsed.path
    parts = _path_parts(path)
    kind = None
    inferred = False
    identifiers = None

    if parsed.scheme.lower() == "https" and host == "dev.azure.com":
        if len(parts) == 4 and parts[2] == "_git":
            kind = "https"
            identifiers = _decode([parts[0], parts[1], parts[3]])
        elif len(parts) == 3 and parts[1] == "_git":
            kind = "https-org-shorthand"
            identifiers = _decode([parts[0], parts[2]])
            inferred = True
            if identifiers:
                identifiers.insert(1, identifiers[1])
    elif parsed.scheme.lower() == "https" and host.endswith(".visualstudio.com"):
        organization = host[: -len(".visualstudio.com")]
        if len(parts) == 2 and parts[0] == "_git":
            kind = "legacy-https-org-shorthand"
            decoded = _decode([parts[1]])
            inferred = True
            identifiers = [organization, decoded[0], decoded[0]] if decoded and _valid_identifier(organization) else None
        elif len(parts) == 3 and parts[1] == "_git":
            kind = "legacy-https"
            identifiers = _decode([organization, parts[0], parts[2]])
        elif len(parts) == 4 and parts[0] == "DefaultCollection" and parts[2] == "_git":
            kind = "legacy-https"
            identifiers = _decode([organization, parts[1], parts[3]])

    if parsed.scheme.lower() == "ssh" and host == "ssh.dev.azure.com":
        if len(parts) == 4 and parts[0] == "v3":
            kind = "ssh"
            identifiers = _decode(parts[1:])
    elif parsed.scheme.lower() == "" and "@" in remote:
        user_host, separator, ssh_path = remote.rpartition(":")
        if separator:
            user, at, remote_host = user_host.rpartition("@")
            ssh_parts = _path_parts(ssh_path)
            if at and remote_host.lower() == "ssh.dev.azure.com" and len(ssh_parts) == 4 and ssh_parts[0] == "v3":
                kind = "ssh"
                identifiers = _decode(ssh_parts[1:])
            elif at and remote_host.lower() == "vs-ssh.visualstudio.com" and len(ssh_parts) == 4 and ssh_parts[0] == "v3":
                kind = "legacy-ssh"
                identifiers = _decode(ssh_parts[1:])

    if not kind or not identifiers:
        return None
    organization, project, repository_id = identifiers
    return {
        "organization": organization,
        "project": project,
        "repository_id": repository_id,
        "remote_url_kind": kind,
        "inferred_project": inferred,
    }


def main(argv: list[str]) -> int:
    if argv == ["--help"]:
        print("usage: git remote get-url <remote> | python parse-git-remote.py")
        print("Reads one Azure DevOps remote URL from stdin; never pass it as an argument.")
        return 0
    if argv:
        print("usage: git remote get-url <remote> | python parse-git-remote.py", file=sys.stderr)
        return 1
    result = parse_remote(sys.stdin.read())
    if result is None:
        lib.emit_blocker(
            "INVALID_REMOTE_URL",
            ["an Azure DevOps git remote URL"],
            "Is this repository hosted on Azure DevOps? Provide the pull request URL or id instead.",
        )
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
