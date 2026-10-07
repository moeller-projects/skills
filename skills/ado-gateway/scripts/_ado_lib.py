#!/usr/bin/env python3
"""_ado_lib.py — shared helpers for ado-gateway scripts.

Purpose: Centralize environment checks, authenticated Azure DevOps HTTP calls,
secret redaction, and structured BLOCKER/ERROR output for all ado-gateway scripts.
Inputs: Imported by sibling scripts; reads AZURE_DEVOPS_PAT from the environment by name only.
Outputs: Structured BLOCKER/ERROR text on stderr with exit code 1 on failure.
Side effects: None by itself; http_request performs network I/O when called.

Requires Python 3.9+, standard library only. Not meant to be run directly.
"""

from __future__ import annotations

import base64
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

API_VERSION = "7.1"
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 2
RETRY_MAX_SECONDS = 60
REQUEST_TIMEOUT_SECONDS = 30

_BEARER_PATTERN = re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._-]+")
_TOKEN_PATTERN = re.compile(
    r"\b(?:ghp_[A-Za-z0-9]+|AZURE_DEVOPS_PAT|[A-Za-z0-9]{20,}\.[A-Za-z0-9._-]{10,})\b"
)

class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Prevent urllib from forwarding the PAT Authorization header on redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_HTTP_OPENER = urllib.request.build_opener(_NoRedirectHandler())



_PR_URL_PATTERN = re.compile(
    r"^https://dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/]+)/pullrequest/([0-9]+)(\?.*)?$"
)
PR_URL_HINT = "https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<id>"


def emit_blocker(code: str, required_input: list[str], next_question: str) -> None:
    """Emit the structured BLOCKER shape on stderr and exit 1."""
    print("BLOCKER:", file=sys.stderr)
    print(f"code: {code}", file=sys.stderr)
    print("required_input:", file=sys.stderr)
    for item in required_input:
        print(f"- {item}", file=sys.stderr)
    print(f"next_question: {next_question}", file=sys.stderr)
    sys.exit(1)


def emit_error(code: str, stage: str, message: str, recovery: str) -> None:
    """Emit the structured ERROR shape on stderr and exit 1."""
    print("ERROR:", file=sys.stderr)
    print(f"code: {code}", file=sys.stderr)
    print(f"stage: {stage}", file=sys.stderr)
    print(f"message: {message}", file=sys.stderr)
    print(f"recovery: {recovery}", file=sys.stderr)
    sys.exit(1)


def require_pat() -> str:
    """Return the PAT from the environment, or BLOCKER-exit when missing.

    The secret is only ever referenced by its environment variable name.
    """
    pat = os.environ.get("AZURE_DEVOPS_PAT", "")
    if not pat:
        emit_blocker(
            "MISSING_AUTH",
            ["AZURE_DEVOPS_PAT"],
            "Provide an Azure DevOps PAT through AZURE_DEVOPS_PAT and retry.",
        )
    return pat


def redact_text(text: str | None) -> str | None:
    """Redact credential-shaped values; mirrors the redact_stdin/jq redact_text rules."""
    if text is None:
        return None
    text = _BEARER_PATTERN.sub(r"\1[REDACTED]", text)
    return _TOKEN_PATTERN.sub("[REDACTED]", text)


def normalize_repo_root_path(path: str | None) -> str | None:
    """Normalize a repo-root-relative path; None/empty/traversal → None.

    Only explicit "." / ".." segments are rejected; dotted filenames stay valid.
    """
    if path is None or path == "":
        return None
    segments = [s for s in path.lstrip("/").split("/") if s]
    if any(s in (".", "..") for s in segments):
        return None
    if not segments:
        return None
    return "/" + "/".join(segments)


def parse_pull_request_url(url: str) -> dict[str, Any] | None:
    """Parse an ADO PR URL into identifiers; None when the URL does not match."""
    match = _PR_URL_PATTERN.match(url)
    if not match:
        return None
    organization, project, repository_id, pull_request_id, _ = match.groups()
    return {
        "organization": organization,
        "project": project,
        "repository_id": repository_id,
        "pull_request_id": int(pull_request_id),
    }


def http_request(
    method: str,
    url: str,
    *,
    content_type: str | None = None,
    body: bytes | None = None,
    label: str,
    stage: str,
    error_code: str,
    error_message: str,
    error_recovery: str,
) -> bytes:
    """Execute an authenticated ADO HTTP request with bounded retries.

    Mirrors the curl policy: up to 5 retries, 2s delay, 60s overall retry budget.
    On exhaustion, emits the structured ERROR shape and exits 1.
    """
    pat = require_pat()
    auth_header = base64.b64encode(f":{pat}".encode("utf-8")).decode("ascii")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {auth_header}",
    }
    if content_type is not None:
        headers["Content-Type"] = content_type

    started = time.monotonic()
    attempt = 0
    while True:
        attempt += 1
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with _HTTP_OPENER.open(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            # 4xx (except 408/429) is not transient; fail without retrying.
            if exc.code < 500 and exc.code not in (408, 429):
                emit_error(error_code, stage, error_message, error_recovery)
            last_error: BaseException = exc
        except (http.client.IncompleteRead, urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            last_error = exc

        if attempt > MAX_RETRIES or (time.monotonic() - started) > RETRY_MAX_SECONDS:
            _ = last_error
            emit_error(error_code, stage, error_message, error_recovery)
        time.sleep(RETRY_DELAY_SECONDS)


def http_get_json(url: str, *, label: str, error_code: str, error_message: str, error_recovery: str) -> Any:
    """GET a JSON document from the ADO API."""
    raw = http_request(
        "GET",
        url,
        label=label,
        stage="fetch",
        error_code=error_code,
        error_message=error_message,
        error_recovery=error_recovery,
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        emit_error(
            "PARSE_FAILED",
            "parse",
            f"Failed to parse the {label} response as JSON.",
            "Check that the URL points at the Azure DevOps REST API and retry.",
        )


def http_write_json(
    method: str,
    content_type: str,
    url: str,
    body: bytes,
    *,
    label: str,
) -> str:
    """Execute a guarded write call and return the redacted response text."""
    raw = http_request(
        method,
        url,
        content_type=content_type,
        body=body,
        label=label,
        stage="write",
        error_code="WRITE_FAILED",
        error_message=f"Failed to execute {label} after retries.",
        error_recovery="Check AZURE_DEVOPS_PAT permissions, identifiers, request body, and network connectivity.",
    )
    redacted = redact_text(raw.decode("utf-8", errors="replace"))
    return redacted if redacted is not None else ""
