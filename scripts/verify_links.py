"""GET-based link verification for the portfolio.

Verifies every external URL used by the portfolio (GitHub repos, live demos,
LinkedIn, GitHub profile) using a GET request with retries and a generous
timeout to allow for Streamlit cold-starts.

Usage:
    python scripts/verify_links.py
"""
from __future__ import annotations

import json
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

TIMEOUT = 45
RETRIES = 2
DELAY = 8  # seconds between retries (allow Streamlit cold-start)


def check_url(url: str, timeout: int = TIMEOUT, retries: int = RETRIES) -> bool:
    """Return True if a GET request returns an HTTP 2xx/3xx status.

    Uses GET (not HEAD) because many Streamlit/Flask apps reject HEAD or
    return non-2xx for it. Retries with a delay to allow cold starts.
    """
    if not url:
        return False
    for attempt in range(retries + 1):
        try:
            req = request.Request(url, method="GET", headers={"User-Agent": "portfolio-verifier"})
            with request.urlopen(req, timeout=timeout) as resp:
                return 200 <= resp.status < 400
        except (error.URLError, error.HTTPError, TimeoutError, OSError):
            if attempt < retries:
                time.sleep(DELAY)
            else:
                return False
    return False


def main() -> None:
    print("GET-based Link Verification")
    print("===========================")
    profile = load_profile()

    results = []

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

    # Non-zero exit if any project github or verified demo fails
    project_gh_fail = [
        r for r in results
        if r["type"] == "project" and r["key"].endswith(":github") and r["ok"] is False
    ]
    verified_demo_fail = [
        r for r in results
        if r["type"] == "project" and r["key"].endswith(":demo") and r["ok"] is False
    ]
    if project_gh_fail or verified_demo_fail:
        print("\nWARNING: Some project GitHub/demo URLs failed verification.")
        sys.exit(1)
    print("\nAll project GitHub URLs and demos verified successfully.")


if __name__ == "__main__":
    main()
