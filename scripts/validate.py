"""Validation / QC script for the portfolio.

Checks:
  - JSON data files are valid and well-formed.
  - All project ids are unique.
  - Every GitHub URL is syntactically valid.
  - Every live demo URL that is marked verified is syntactically valid.
  - No fabricated/personal data placeholders are silently empty.
  - Resume content can be assembled from the data layer.
  - All UI modules import cleanly (without launching Streamlit).

Usage:
    python scripts/validate.py
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

# Ensure the project root is importable regardless of how the script is invoked.
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from utils.helpers import ROOT_DIR, load_certifications, load_profile, load_projects

FAILURES: list[str] = []


def check(cond: bool, msg: str):
    if not cond:
        FAILURES.append(msg)
        print(f"  [FAIL] {msg}")
    else:
        print(f"  [OK]   {msg}")


def validate_json_files():
    print("\n== JSON Data Files ==")
    for rel in ["data/projects.json", "data/profile.json", "data/skills.json", "data/certifications.json"]:
        path = ROOT_DIR / rel
        check(path.exists(), f"{rel} exists")
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            check(True, f"{rel} is valid JSON")
        except Exception as exc:
            check(False, f"{rel} parse error: {exc}")


def validate_projects():
    print("\n== Projects ==")
    projects = load_projects()
    ids = [p["id"] for p in projects]
    check(len(ids) == len(set(ids)), "project ids are unique")
    check(len(projects) > 0, f"{len(projects)} projects loaded")

    for p in projects:
        gurl = p.get("github_url", "")
        check(_is_valid_url(gurl), f"{p['id']}: valid github_url")
        demo = p.get("live_demo_url")
        if demo:
            if p.get("demo_verified"):
                check(_is_valid_url(demo), f"{p['id']}: verified demo URL is valid")
            else:
                check(_is_valid_url(demo), f"{p['id']}: demo URL is valid (unverified)")


def validate_profile():
    print("\n== Profile ===")
    profile = load_profile()
    name = profile.get("name", "")
    check(bool(name), "profile has a name")

    # Placeholders must be clearly marked, not silently empty.
    email = profile.get("email", "")
    check(("[ADD_" in email.upper()) or email, "email present or clearly marked placeholder")
    location = profile.get("location", "")
    check(("[ADD_" in location.upper()) or location, "location present or clearly marked placeholder")


def validate_resume():
    print("\n== Resume Assembly ==")
    try:
        from resume.resume_template import build_resume_content

        content = build_resume_content()
        check(bool(content["name"]), "resume has a name")
        check(len(content["project_entries"]) > 0, "resume has selected projects")
        check(bool(content["summary"]), "resume has a summary")
    except Exception as exc:
        check(False, f"resume assembly failed: {exc}")


def validate_imports():
    print("\n== Module Imports ==")
    modules = [
        "utils.helpers",
        "utils.validation",
        "utils.github",
        "components.ui",
        "components.navbar",
        "components.footer",
        "components.project_card",
        "components.skill_card",
        "components.metrics",
        "components.timeline",
        "components.detail_sections",
        "resume.resume_template",
    ]
    for mod in modules:
        try:
            importlib.import_module(mod)
            print(f"  [OK]   {mod}")
        except Exception as exc:
            check(False, f"{mod} import failed: {exc}")


def _is_valid_url(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("https", "http") and bool(parsed.netloc)
    except Exception:
        return False


def main():
    print("Portfolio Validation / QC")
    print("=========================")
    validate_json_files()
    validate_projects()
    validate_profile()
    validate_resume()
    validate_imports()

    print("\n=========================")
    if FAILURES:
        print(f"Validation FAILED with {len(FAILURES)} issue(s).")
        sys.exit(1)
    print("Validation PASSED.")


if __name__ == "__main__":
    main()
