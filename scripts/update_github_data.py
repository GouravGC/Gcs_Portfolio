"""Refresh GitHub repository metadata and merge it into data/projects.json.

This script is meant to be run periodically (not at every page load) to avoid
GitHub API rate-limit issues and keep the portfolio available offline.

Usage (optional GitHub token to raise rate limit):
    GITHUB_TOKEN=ghp_xxx python scripts/update_github_data.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib import error, request

# Ensure the project root is importable regardless of how the script is invoked.
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from utils.helpers import ROOT_DIR, load_json, save_json

USERNAME = "GouravGC"
API = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
DATA_FILE = "data/projects.json"


def _fetch_json(url: str, token: str | None = None) -> list | dict:
    req = request.Request(url)
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN", "").strip() or None
    print(f"Fetching repositories for @{USERNAME} ...")
    try:
        repos = _fetch_json(API, token)
    except (error.URLError, error.HTTPError) as exc:
        print(f"GitHub API request failed: {exc}")
        sys.exit(1)

    if not isinstance(repos, list):
        print("Unexpected API response.")
        sys.exit(1)

    # Load existing curated project metadata.
    data = load_json(DATA_FILE)
    existing = {p["id"]: p for p in data.get("projects", [])}

    # Map repo name -> project id (reverse of the curated id convention).
    # We update only metadata fields that are safe to refresh from GitHub.
    refreshed = 0
    for repo in repos:
        repo_name = repo["name"]
        project = _find_project_by_repo(existing, repo_name)
        if not project:
            continue
        project["github_url"] = repo["html_url"]
        project["languages"] = _languages(repo, token)
        project["description"] = repo.get("description") or project.get("description", "")
        project["stars"] = repo.get("stargazers_count", 0)
        project["forks"] = repo.get("forks_count", 0)
        project["updated_at"] = repo.get("updated_at", "")
        refreshed += 1

    save_json(data, DATA_FILE)
    print(f"Refreshed metadata for {refreshed} projects.")
    print("Live demo URLs and curated descriptions were left untouched.")


def _find_project_by_repo(existing: dict, repo_name: str) -> dict | None:
    """Find a project whose repo name matches a GitHub repo name."""
    for project in existing.values():
        url = project.get("github_url", "")
        if url.rstrip("/").endswith("/" + repo_name):
            return project
    return None


def _languages(repo: dict, token: str | None) -> list[str]:
    lang_url = repo.get("languages_url")
    if not lang_url:
        return []
    try:
        langs = _fetch_json(lang_url, token)
        if isinstance(langs, dict):
            return list(langs.keys())
    except (error.URLError, error.HTTPError):
        pass
    return []


if __name__ == "__main__":
    main()
