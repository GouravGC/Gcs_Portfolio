"""GitHub metadata utilities.

The portfolio does NOT depend on live GitHub API calls at page load. Instead,
this module provides an optional script (scripts/update_github_data.py) that
can refresh repository metadata into a local JSON file. The app reads only the
local, structured data, which makes deployment reliable and avoids rate limits.

Environment variables (optional):
    GITHUB_TOKEN  - a personal access token to raise API rate limits.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request

from .helpers import DATA_DIR

GITHUB_USER = "GouravGC"
REPOS_CACHE = DATA_DIR / "github_repos.json"


def _build_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_json(url: str) -> dict | list | None:
    req = request.Request(url, headers=_build_headers())
    with request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            return None
        return json.loads(resp.read().decode("utf-8"))


def fetch_user_repos(username: str = GITHUB_USER, per_page: int = 100) -> list[dict]:
    """Fetch all public repositories for a GitHub user via the API."""
    page = 1
    repos: list[dict] = []
    while True:
        url = (
            f"https://api.github.com/users/{username}/repos"
            f"?per_page={per_page}&page={page}&sort=updated"
        )
        batch = _fetch_json(url)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return repos


def fetch_repo_languages(username: str, repo_name: str) -> dict:
    """Fetch language usage percentages for a repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    data = _fetch_json(url)
    return data if isinstance(data, dict) else {}


def summarize_repo(repo: dict) -> dict:
    """Extract a portable summary of a repository for local caching."""
    return {
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "stargazers_count": repo.get("stargazers_count", 0),
        "forks_count": repo.get("forks_count", 0),
        "homepage": repo.get("homepage"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "license": (repo.get("license") or {}).get("spdx_id"),
        "default_branch": repo.get("default_branch"),
    }


def refresh_repo_cache(username: str = GITHUB_USER) -> Path:
    """Fetch all repos and write a local cache file. Returns the cache path."""
    repos = fetch_user_repos(username)
    summary = [summarize_repo(r) for r in repos]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPOS_CACHE, "w", encoding="utf-8") as f:
        json.dump({"username": username, "repos": summary}, f, indent=2)
    return REPOS_CACHE


def load_repo_cache() -> dict:
    """Load the local repo cache. Returns empty dict if unavailable."""
    if not REPOS_CACHE.exists():
        return {}
    with open(REPOS_CACHE, "r", encoding="utf-8") as f:
        return json.load(f)
