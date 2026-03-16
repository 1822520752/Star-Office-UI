#!/usr/bin/env python3
"""Star Office UI smoke test (non-destructive).

Usage:
  python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000

Optional env:
  SMOKE_AUTH_BEARER=xxxx   # if your gateway/proxy requires bearer auth
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request


REQUIRED_ENDPOINTS = [
    ("GET", "/", 200),
    ("GET", "/health", 200),
    ("GET", "/status", 200),
    ("GET", "/agents", 200),
    ("GET", "/yesterday-memo", 200),
]


def req(
    method: str,
    url: str,
    body: dict | None = None,
    token: str = "",
    timeout: float = 8,
    retries: int = 0,
) -> tuple[int, str]:
    data = None
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    for attempt in range(max(0, retries) + 1):
        r = urllib.request.Request(url=url, method=method, data=data, headers=headers)
        try:
            with urllib.request.urlopen(r, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
                return resp.status, raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
            code = e.code
            if code >= 500 and attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            return code, raw
        except Exception as e:
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            return 0, str(e)


def validate_json(path: str, body: str) -> tuple[bool, str]:
    if path not in {"/health", "/status", "/agents", "/yesterday-memo"}:
        return True, ""

    try:
        data = json.loads(body)
    except Exception as e:
        return False, f"{path}: invalid json ({e})"

    if path == "/health":
        for k in ("status", "service", "timestamp"):
            if not isinstance(data, dict) or k not in data:
                return False, f"{path}: missing json field {k}"
        return True, ""

    if path == "/status":
        for k in ("state", "detail", "progress", "updated_at"):
            if not isinstance(data, dict) or k not in data:
                return False, f"{path}: missing json field {k}"
        return True, ""

    if path == "/agents":
        if not isinstance(data, list):
            return False, f"{path}: expected json list"
        if not any(isinstance(x, dict) and x.get("isMain") for x in data):
            return False, f"{path}: expected at least one main agent"
        return True, ""

    if path == "/yesterday-memo":
        if not isinstance(data, dict) or "success" not in data:
            return False, f"{path}: missing json field success"
        return True, ""

    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:19000", help="Base URL of Star Office UI service")
    ap.add_argument("--timeout", type=float, default=8, help="HTTP timeout seconds")
    ap.add_argument("--retries", type=int, default=0, help="Retries for network/5xx failures")
    ap.add_argument("--skip-set-state", action="store_true", help="Skip POST /set_state probe")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    token = os.getenv("SMOKE_AUTH_BEARER", "").strip()

    failures: list[str] = []
    print(f"[smoke] base={base}")

    for method, path, expected in REQUIRED_ENDPOINTS:
        code, body = req(method, base + path, token=token, timeout=args.timeout, retries=args.retries)
        if code != expected:
            failures.append(f"{method} {path}: expected {expected}, got {code}, body={body[:200]}")
        else:
            print(f"  OK  {method} {path} -> {code}")
            ok, msg = validate_json(path, body)
            if not ok:
                failures.append(msg)

    # non-destructive state update probe
    if not args.skip_set_state:
        code, body = req(
            "POST",
            base + "/set_state",
            {"state": "idle", "detail": "smoke-check"},
            token=token,
            timeout=args.timeout,
            retries=args.retries,
        )
        if code != 200:
            failures.append(f"POST /set_state failed: {code}, body={body[:200]}")
        else:
            print("  OK  POST /set_state -> 200")

    if failures:
        print("\n[smoke] FAIL")
        for f in failures:
            print(" -", f)
        return 1

    print("\n[smoke] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
