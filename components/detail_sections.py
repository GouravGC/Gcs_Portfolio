"""Rendering helpers for the project detail page sections.

Only sections with verified information are rendered. Empty/null fields are
omitted gracefully.
"""
from __future__ import annotations

import streamlit as st

from utils.helpers import has_verified_demo


def _list_block(title: str, items: list) -> None:
    if not items:
        return
    st.markdown(f"**{title}**")
    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, dict):
        for k, v in items.items():
            st.markdown(f"- **{k}:** {v}")


def _badge_row(items: list) -> None:
    if not items:
        return
    html = "".join(f'<span class="gc-badge blue">{i}</span>' for i in items)
    st.markdown(f'<div>{html}</div>', unsafe_allow_html=True)


def render_metrics(metrics: dict) -> None:
    if not metrics:
        st.markdown("*No verified numeric metrics were available for this project.*")
        return
    cols = st.columns(min(3, max(1, len(metrics))))
    for i, (k, v) in enumerate(metrics.items()):
        with cols[i % len(cols)]:
            st.metric(label=k, value=v)


def render_deployment(project: dict) -> None:
    st.markdown("### Deployment")
    platforms = project.get("deployment", [])
    _badge_row(platforms)
    dp = project.get("deployment_platform")
    if dp:
        st.markdown(f"- **Platform:** {dp}")
    if has_verified_demo(project):
        st.markdown(
            f'<a class="gc-btn gc-btn-accent" href="{project.get("live_demo_url")}" target="_blank" rel="noopener">Open Live Demo</a>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("*No verified live demo URL is available for this project.*")


def render_github(project: dict) -> None:
    st.markdown("### GitHub")
    gh = project.get("github_url", "")
    if gh:
        st.markdown(
            f'<a class="gc-btn gc-btn-primary" href="{gh}" target="_blank" rel="noopener">Open Repository</a>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("*GitHub URL not available.*")


def render_architecture(architecture: str | None) -> None:
    if not architecture:
        return
    st.markdown("### Architecture")
    st.code(architecture, language="text")


def render_key_features(features: list) -> None:
    _list_block("Key Features", features)


def render_technical_highlights(highlights: list) -> None:
    _list_block("Technical Highlights", highlights)


def render_problem_statement(statement: str | None) -> None:
    if not statement:
        return
    st.markdown("### Problem Statement")
    st.markdown(statement)


def render_dataset(project: dict) -> None:
    dataset = project.get("dataset")
    size = project.get("data_size")
    if not dataset and not size:
        return
    st.markdown("### Dataset")
    if dataset:
        st.markdown(f"- **Source:** {dataset}")
    if size:
        st.markdown(f"- **Size:** {size}")


def render_section(title: str, content) -> None:
    """Generic section renderer. content may be a str, list, or dict."""
    if not content:
        return
    st.markdown(f"### {title}")
    if isinstance(content, str):
        st.markdown(content)
    elif isinstance(content, list):
        for item in content:
            st.markdown(f"- {item}")
    elif isinstance(content, dict):
        for k, v in content.items():
            st.markdown(f"- **{k}:** {v}")
