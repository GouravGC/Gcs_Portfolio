"""Shared helper utilities for the portfolio application.

This module is intentionally dependency-light so it can be used both by the
Streamlit app and by standalone scripts (resume generation, validation, etc.)
without importing heavy ML/DL frameworks.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# Root directory of the project (parent of this utils/ folder).
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"
RESUME_DIR = ROOT_DIR / "resume"
OUTPUT_DIR = RESUME_DIR / "output"


def get_path(*parts: str) -> Path:
    """Return a Path rooted at the project directory."""
    return ROOT_DIR.joinpath(*parts)


def load_json(relative_path: str) -> dict:
    """Load a JSON file relative to the project root and return its content."""
    path = get_path(relative_path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, relative_path: str) -> None:
    """Write a JSON file relative to the project root."""
    path = get_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_projects() -> list[dict]:
    """Load the projects database."""
    data = load_json("data/projects.json")
    return data.get("projects", [])


def load_profile() -> dict:
    """Load the candidate profile."""
    return load_json("data/profile.json")


def load_skills() -> dict:
    """Load the skills database."""
    return load_json("data/skills.json")


def load_certifications() -> dict:
    """Load the certifications database."""
    return load_json("data/certifications.json")


def get_project_by_id(project_id: str) -> dict | None:
    """Return a project dict by its id, or None."""
    for p in load_projects():
        if p.get("id") == project_id:
            return p
    return None


def list_categories(projects: list[dict] | None = None) -> list[str]:
    """Return a sorted, de-duplicated list of all project categories."""
    projects = projects or load_projects()
    cats: set[str] = set()
    for p in projects:
        cats.update(p.get("category", []))
    return sorted(cats)


def list_technologies(projects: list[dict] | None = None) -> list[str]:
    """Return a sorted, de-duplicated list of key technologies across projects.

    Combines languages, frameworks, and libraries into a single searchable list.
    """
    projects = projects or load_projects()
    techs: set[str] = set()
    for p in projects:
        techs.update(p.get("languages", []))
        techs.update(p.get("frameworks", []))
        techs.update(p.get("libraries", []))
    return sorted(techs)


def list_deployment_platforms(projects: list[dict] | None = None) -> list[str]:
    """Return a sorted, de-duplicated list of deployment platforms."""
    projects = projects or load_projects()
    platforms: set[str] = set()
    for p in projects:
        dp = p.get("deployment_platform")
        if dp:
            platforms.add(dp)
    return sorted(platforms)


def is_placeholder(value) -> bool:
    """Return True if a value is a placeholder (contains square-bracket tags)."""
    if not value:
        return True
    return "[ADD_" in str(value).upper() and "PLACEHOLDER" in str(value).upper()


def has_verified_demo(project: dict) -> bool:
    """Return True if a project has a verified live demo URL."""
    url = project.get("live_demo_url")
    return bool(url) and project.get("demo_verified") is True


def ensure_output_dir() -> Path:
    """Ensure the resume output directory exists and return it."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def get_env(key: str, default: str = "") -> str:
    """Read an environment variable (lightweight, no python-dotenv required)."""
    return os.environ.get(key, default)
