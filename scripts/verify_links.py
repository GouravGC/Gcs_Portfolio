"""GET-based link verification for the portfolio.

Checks every external URL (GitHub profile, LinkedIn, project GitHub repos,
and live demo URLs) with bounded, strict settings so a single unreachable URL
can never block verification of the rest, and the script always terminates.

Verification rules:
  * GET requests only (no HEAD — many Streamlit/Flask apps reject HEAD).
  * Max 12 seconds per request.
  * Max 1 retry with a 2 second delay.
  * Max 3 redirects per URL (prevents infinite Streamlit redirect loops).
  * Overall deadline of 180 seconds for the whole run.
  * Each URL is isolated: a timeout/redirect-loop/DNS/HTTP failure on one URL
    simply returns False and the script moves on.
  * A final summary is always printed.

Usage:
    python scripts/verify_links.py
"""
from __future__ import annotations

import json
import socket
import sys
import time
from pathlib import Path
from urllib import error, request

# Ensure the project root is importable regardless of how the script is invoked.
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from utils.helpers import load_profile, load_projects

# Bounded verification settings.
TIMEOUT = 12          # seconds per request (strict; no waiting on cold starts)
RETRIES = 1           # maximum number of retries per URL
DELAY = 2             # seconds between retries
MAX_REDIRECTS = 3     # redirect cap to avoid infinite loops
OVERALL_BUDGET = 180  # seconds for the entire verification run


class _CappedRedirectHandler(request.HTTPRedirectHandler):
    """Follow redirects up to MAX_REDIRECTS.

    A fresh instance is created per request, so the hop counter is isolated per
    URL. Exceeding the cap raises an HTTPError, which is treated as a failure.
    """

    MAX_REDIRECTS = MAX_REDIRECTS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hops = 0

    def redirect_request(self, req, fp, code, msg, headers, new_url):
        if self._hops >= self.MAX_REDIRECTS:
            raise error.HTTPError(
                req.full_url, code, "Too many redirects", headers, fp
            )
        self._hops += 1
        return super().redirect_request(req, fp, code, msg, headers, new_url)


def check_url(url: str, timeout: int = TIMEOUT, retries: int = RETRIES) -> bool:
    """Return True if a GET request resolves to HTTP 2xx/3xx.

    Every failure type (HTTP error, timeout, redirect loop, DNS/network error)
    is caught and returns False. We never use HEAD.
    """
    if not url:
        return False
    for attempt in range(retries + 1):
        try:
            opener = request.build_opener(_CappedRedirectHandler)
            req = request.Request(
                url, method="GET", headers={"User-Agent": "portfolio-verifier"}
            )
            with opener.open(req, timeout=timeout) as resp:
                return 200 <= resp.status < 400
        except error.HTTPError:
            return False
        except (error.URLError, TimeoutError, OSError, socket.timeout):
            if attempt < retries:
                time.sleep(DELAY)
            else:
                return False
    return False


def _deadline_exceeded(deadline: float) -> bool:
    """Return True if the overall verification budget has been exceeded."""
    return time.monotonic() > deadline


def main() -> None:
    print("GET-based Link Verification")
    print("===========================")
    profile = load_profile()
    results: list[dict] = []
    deadline = time.monotonic() + OVERALL_BUDGET

    # GitHub profile
    gh = profile.get("github", "")
    ok = check_url(gh)
    results.append({"type": "profile", "key": "github", "url": gh, "ok": ok})
    print(f"[{'OK' if ok else 'FAIL'}] profile/github: {gh}")

    # LinkedIn
    li = profile.get("linkedin", "")
    ok = check_url(li)
    results.append({"type": "profile", "key": "linkedin", "url": li, "ok": ok})
    print(f"[{'OK' if ok else 'FAIL'}] profile/linkedin: {li}")

    # Projects
    for p in load_projects():
        if _deadline_exceeded(deadline):
            print("\nOverall verification budget exceeded; stopping early.")
            break
        pid = p.get("id")
        gurl = p.get("github_url", "")
        gok = check_url(gurl)
        results.append({"type": "project", "key": f"{pid}:github", "url": gurl, "ok": gok})
        print(f"[{'OK' if gok else 'FAIL'}] {pid}/github: {gurl}")

        demo = p.get("live_demo_url")
        if demo:
            dok = check_url(demo)
            results.append({"type": "project", "key": f"{pid}:demo", "url": demo, "ok": dok})
            print(f"[{'OK' if dok else 'FAIL'}] {pid}/demo: {demo}")
        else:
            results.append({"type": "project", "key": f"{pid}:demo", "url": None, "ok": None})
            print(f"[SKIP] {pid}/demo: none")

    # Summary
    verified_demos = [
        r for r in results
        if r["type"] == "project" and r["key"].endswith(":demo") and r["ok"] is True
    ]
    failed = [r for r in results if r["ok"] is False]
    print("\n===========================")
    print(f"Total URLs checked: {len(results)}")
    print(f"Verified live demos: {len(verified_demos)}")
    print(f"Failed/Unreachable: {len(failed)}")
    for r in failed:
        print(f"  - {r['key']}: {r['url']}")

    # Write a machine-readable report
    out = _PROJECT_ROOT / "data" / "_link_verification_report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nReport written to {out}")

    # Non-zero exit if any project GitHub URL failed verification.
    project_gh_fail = [
        r for r in results
        if r["type"] == "project" and r["key"].endswith(":github") and r["ok"] is False
    ]
    if project_gh_fail:
        print("\nWARNING: Some project GitHub URLs failed verification.")
        sys.exit(1)
    print("\nAll project GitHub URLs verified successfully.")


if __name__ == "__main__":
    main()
