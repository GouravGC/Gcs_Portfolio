"""Rendering helpers for the project detail page sections.

Only sections with verified information are rendered. Empty/null fields are
omitted gracefully. Uses expanders and cards for a clean, professional layout.
"""
from __future__ import annotations

import html as _html

import streamlit as st

from components.ui import deployment_badge
from utils.helpers import has_verified_demo


def _list_block(title: str, items) -> None:
    if not items:
        return
    st.markdown(f"**{title}**")
    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, dict):
        for k, v in items.items():
            st.markdown(f"- **{k}:** {v}")


def _badge_row(items, tone: str = "blue") -> None:
    if not items:
        return
    html = "".join(f'<span class="gc-badge {tone}">{_html.escape(str(i))}</span>' for i in items)
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
    with st.expander("🚀 Deployment", expanded=True):
        platforms = project.get("deployment", [])
        _badge_row(platforms, "green")
        dp = project.get("deployment_platform")
        if dp:
            st.markdown(f"- **Platform:** {dp}")
        deployment_badge(project)
        if has_verified_demo(project):
            st.markdown(
                f'<a class="gc-btn gc-btn-accent" href="{project.get("live_demo_url")}" target="_blank" rel="noopener">Open Live Demo</a>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown("*No live demo URL is available for this project.*")


def render_github(project: dict) -> None:
    with st.expander("💻 Source Code", expanded=True):
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
    with st.expander("🏗 Architecture"):
        st.code(architecture, language="text")


def render_key_features(features: list) -> None:
    if not features:
        return
    with st.expander("✨ Key Features"):
        _list_block("", features)


def render_technical_highlights(highlights: list) -> None:
    if not highlights:
        return
    with st.expander("⚙️ Technical Highlights"):
        _list_block("", highlights)


def render_problem_statement(statement: str | None) -> None:
    if not statement:
        return
    with st.expander("🎯 Problem Statement", expanded=True):
        st.markdown(statement)


def render_dataset(project: dict) -> None:
    dataset = project.get("dataset")
    size = project.get("data_size")
    if not dataset and not size:
        return
    with st.expander("🗂 Dataset"):
        if dataset:
            st.markdown(f"- **Source:** {dataset}")
        if size:
            st.markdown(f"- **Size:** {size}")


def render_section(title: str, content) -> None:
    """Generic section renderer. content may be a str, list, or dict."""
    if not content:
        return
    with st.expander(title, expanded=False):
        if isinstance(content, str):
            st.markdown(content)
        elif isinstance(content, list):
            for item in content:
                st.markdown(f"- {item}")
        elif isinstance(content, dict):
            for k, v in content.items():
                st.markdown(f"- **{k}:** {v}")
