"""Validation / quality-control utilities.

Provides functions to validate the JSON data files, project schemas, links, and
placeholders. Used by scripts/validate.py and callable from tests.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib import request

from .helpers import (
    ROOT_DIR,
    is_placeholder,
    load_certifications,
    load_profile,
    load_projects,
    load_skills,
)

http_client = request


def _validate_json_syntax() -> list[str]:
    errors: list[str] = []
    json_files = [
        "data/profile.json",
        "data/skills.json",
        "data/projects.json",
        "data/certifications.json",
    ]
    for rel in json_files:
        path = ROOT_DIR / rel
        try:
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            errors.append(f"[json] Missing file: {rel}")
        except json.JSONDecodeError as exc:
            errors.append(f"[json] Invalid JSON in {rel}: {exc}")
    return errors


def _validate_required_fields() -> list[str]:
    errors: list[str] = []
    # Profile
    profile = load_profile()
    for field in ["name", "professional_title", "github"]:
        if not profile.get(field):
            errors.append(f"[profile] Missing required field: {field}")

    # Projects
    projects = load_projects()
    if not projects:
        errors.append("[projects] No projects found.")
    seen_ids = set()
    for p in projects:
        pid = p.get("id")
        if not pid:
            errors.append("[projects] A project is missing 'id'.")
        elif pid in seen_ids:
            errors.append(f"[projects] Duplicate project id: {pid}")
        seen_ids.add(pid)
        for field in ["name", "short_description", "category", "github_url"]:
            if not p.get(field):
                errors.append(f"[projects:{pid}] Missing field: {field}")
        if not isinstance(p.get("category"), list):
            errors.append(f"[projects:{pid}] 'category' must be a list.")
    return errors


def _validate_links() -> list[str]:
    errors: list[str] = []
    profile = load_profile()
    for key in ["github", "linkedin"]:
        url = profile.get(key)
        if url and "PLACEHOLDER" not in url and not url.startswith("http"):
            errors.append(f"[profile:{key}] Not an http(s) URL: {url}")

    for p in load_projects():
        pid = p.get("id")
        gh = p.get("github_url")
        if gh and not (gh.startswith("https://github.com/")):
            errors.append(f"[projects:{pid}] GitHub URL not from github.com: {gh}")
        demo = p.get("live_demo_url")
        if demo and not demo.startswith("http"):
            errors.append(f"[projects:{pid}] Live demo URL not http(s): {demo}")
        if p.get("demo_verified") and not demo:
            errors.append(f"[projects:{pid}] demo_verified=true but no live_demo_url.")
    return errors


def _validate_skills() -> list[str]:
    errors: list[str] = []
    data = load_skills()
    for category in data.get("categories", []):
        for skill in category.get("skills", []):
            if not skill.get("name"):
                errors.append("[skills] A skill is missing its name.")
            ev = skill.get("evidence")
            if ev not in ("project_demonstrated", "technical_knowledge"):
                errors.append(f"[skills:{skill.get('name')}] Invalid evidence: {ev}")
    return errors


def _validate_placeholders() -> list[str]:
    errors: list[str] = []
    profile = load_profile()
    for field in ["email", "phone", "location"]:
        if is_placeholder(profile.get(field)):
            # Placeholders are expected for unverified personal data; report as info.
            errors.append(f"[profile:{field}] Placeholder present (expected).")
    return errors


def validate_data(include_network: bool = False) -> list[str]:
    """Run all validation checks and return a list of error strings."""
    errors: list[str] = []
    errors += _validate_json_syntax()
    errors += _validate_required_fields()
    errors += _validate_links()
    errors += _validate_skills()
    errors += _validate_placeholders()
    if include_network:
        errors += _validate_network_links()
    return errors


def check_url(url: str, timeout: int = 10) -> bool:
    """Return True if a URL returns an HTTP 2xx/3xx status."""
    try:
        req = request.Request(url, headers={"User-Agent": "portfolio-validator"})
        with request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


def _validate_network_links() -> list[str]:
    """Optionally verify live links over the network (slow; used in QC)."""
    errors: list[str] = []
    profile = load_profile()
    for key in ["github", "linkedin"]:
        url = profile.get(key)
        if url and "PLACEHOLDER" not in url:
            if not check_url(url):
                errors.append(f"[profile:{key}] Network check failed: {url}")
    for p in load_projects():
        pid = p.get("id")
        for field in ["github_url", "live_demo_url"]:
            url = p.get(field)
            if url and not check_url(url):
                errors.append(f"[projects:{pid}:{field}] Network check failed: {url}")
    return errors


def count_metrics(projects) -> int:
    """Count how many projects have verified metrics."""
    return sum(1 for p in (projects or load_projects()) if p.get("metrics"))
