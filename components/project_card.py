"""Project card component for the project explorer."""
from __future__ import annotations

import streamlit as st

from utils.helpers import has_verified_demo


def _badges(items: list[str], tone: str = "blue") -> str:
    return "".join(
        f'<span class="gc-badge {tone}">{item}</span>'
        for item in items[:4]
    )


def project_card(project: dict, detail_page: str = "Project_Detail") -> None:
    """Render a single project card with title, description, badges, and buttons."""
    name = project.get("name", "Untitled Project")
    desc = project.get("short_description", "")
    categories = project.get("category", [])
    langs = project.get("languages", [])
    github = project.get("github_url", "")
    demo = project.get("live_demo_url", "")
    pid = project.get("id", "")
    featured = project.get("featured", False)

    star = " ⭐" if featured else ""
    cat_html = _badges(categories, "blue")
    lang_html = _badges(langs, "green")

    st.markdown(f'<div class="gc-card">', unsafe_allow_html=True)
    st.markdown(
        f'<h3>{name}{star}</h3><div class="gc-desc">{desc}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div>{cat_html}</div>', unsafe_allow_html=True)
    if lang_html:
        st.markdown(f'<div>{lang_html}</div>', unsafe_allow_html=True)

    # Buttons
    a, b, c = st.columns([1, 1, 1])
    with a:
        if github:
            st.markdown(
                f'<a class="gc-btn gc-btn-primary" href="{github}" target="_blank" rel="noopener">GitHub</a>',
                unsafe_allow_html=True,
            )
    with b:
        if has_verified_demo(project) and demo:
            st.markdown(
                f'<a class="gc-btn gc-btn-accent" href="{demo}" target="_blank" rel="noopener">Live Demo</a>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="gc-badge amber">No verified demo</span>',
                unsafe_allow_html=True,
            )
    with c:
        if pid:
            # Use a Streamlit button wiring to the detail page via query params.
            if st.button("View Details", key=f"detail_{pid}"):
                st.switch_page(f"pages/{detail_page}.py")

    st.markdown("</div>", unsafe_allow_html=True)
