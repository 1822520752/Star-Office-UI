#!/usr/bin/env python3
"""Star Office UI smoke test (non-destructive).

Usage:
  python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000

Optional env:
  SMOKE_AUTH_BEARER=xxxx   # if your gateway/proxy requires bearer auth
"""

import json
import os
import sys
import time
from typing import Optional
import argparse
import urllib.error
import urllib.request
from datetime import datetime

# Simple ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

if os.name == "nt":  # Windows might not support ANSI by default in older shells
    GREEN = RED = YELLOW = RESET = ""

def log_ok(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")

def log_fail(msg):
    print(f"{RED}[FAIL]{RESET} {msg}")

def log_warn(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")

def call_api(
    url: str,
    method: str = "GET",
    body: Optional[dict] = None,
    bearer: Optional[str] = None
):
    headers = {}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    if body:
        headers["Content-Type"] = "application/json"

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.getcode(), json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {"msg": str(e)}
    except Exception as e:
        return 0, {"msg": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:19000", help="Base URL of Star Office UI")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    bearer = os.environ.get("SMOKE_AUTH_BEARER")

    print(f"--- Star Office UI Smoke Test ---")
    print(f"Target: {base_url}")
    print(f"Time:   {datetime.now().isoformat()}\n")

    # 1. /health (basic existence)
    code, data = call_api(f"{base_url}/health")
    if code == 200:
        log_ok(f"/health (backend version: {data.get('version', 'unknown')})")
    else:
        log_fail(f"/health (code={code}, err={data.get('msg')})")
        sys.exit(1)

    # 2. /status (state consistency)
    code, data = call_api(f"{base_url}/status")
    if code == 200 and "state" in data:
        log_ok(f"/status (current state: {data['state']})")
    else:
        log_fail(f"/status (code={code})")

    # 3. /agents (multi-agent registry)
    code, data = call_api(f"{base_url}/agents")
    if code == 200 and isinstance(data, list):
        log_ok(f"/agents (count: {len(data)})")
    else:
        log_fail(f"/agents (code={code})")

    # 4. /memo (yesterday memo)
    code, data = call_api(f"{base_url}/memo")
    if code == 200:
        log_ok(f"/memo (available: {data.get('ok', False)})")
    else:
        log_warn(f"/memo returned {code} (expected if no memory files found)")

    # 5. /static/phaser-3.80.1.min.js (asset check)
    try:
        req = urllib.request.Request(f"{base_url}/static/phaser-3.80.1.min.js")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                log_ok(f"Frontend assets reachable (phaser.js)")
            else:
                log_fail(f"Frontend assets returned {response.getcode()}")
    except Exception as e:
        log_fail(f"Frontend assets unreachable: {e}")

    print("\n--- Smoke test finished ---")

if __name__ == "__main__":
    main()
