"""Project card component for the project explorer.

Renders each project with a clear name, description, category badges,
technology badges, a deployment status badge, and three visually distinct
actions: GitHub, Live Demo (only when a demo URL exists), and View Details.

View Details uses the **native, non-callback** Streamlit navigation pattern:

    if st.button("View Details", key=...):
        st.session_state["selected_project_id"] = pid
        st.switch_page("pages/3_Project_Detail.py")

This carries the selected project's **unique stable id** in session_state and
switches to the detail page. It avoids ``on_click`` callbacks, ``st.rerun()``,
and query-param mutation, all of which are problematic in Streamlit 1.37.1
(calling navigation inside a callback is a no-op).
"""
from __future__ import annotations

import html as _html

import streamlit as st

from components.ui import guess_deployment_status
from utils.helpers import get_tier, has_verified_demo

# The actual multipage filename for the project detail page. Streamlit registers
# pages with their exact filename (including the numeric navigation prefix), so
# st.switch_page(...) must use this exact path or it raises StreamlitAPIException.
PROJECT_DETAIL_PAGE = "3_Project_Detail"


def _badges(items: list[str], tone: str = "blue", limit: int = 6) -> str:
    return "".join(
        f'<span class="gc-badge {tone}">{_html.escape(str(item))}</span>'
        for item in items[:limit]
    )


def _view_details(pid: str, btn_key: str) -> None:
    """Render the View Details button using native, non-callback navigation.

    When clicked, the running script naturally re-runs (button clicks are page
    events). This branch runs in normal script flow -- NOT inside an on_click
    callback -- so ``st.switch_page`` works reliably and carries the exact
    project id via session_state.
    """
    if not pid:
        return
    if st.button("View Details", key=btn_key, use_container_width=True):
        st.session_state["selected_project_id"] = pid
        st.switch_page(f"pages/{PROJECT_DETAIL_PAGE}.py")


def _render_buttons(project: dict, pid: str, key_suffix: str = "") -> None:
    """Render GitHub / Live Demo / View Details as distinct, always-readable buttons."""
    github = project.get("github_url", "")
    demo = project.get("live_demo_url", "")
    # Unique key per rendered instance so the same project appearing in multiple
    # domain sections (e.g. the "All" view) does not cause DuplicateWidgetID.
    btn_key = f"detail_{pid}{key_suffix}"

    if github:
        col_g, col_d, col_v = st.columns(3)
        with col_g:
            st.markdown(
                f'<a class="gc-btn gc-btn-primary" href="{github}" '
                f'target="_blank" rel="noopener">GitHub</a>',
                unsafe_allow_html=True,
            )
        with col_d:
            if has_verified_demo(project) and demo:
                st.markdown(
                    f'<a class="gc-btn gc-btn-accent" href="{demo}" '
                    f'target="_blank" rel="noopener">Live Demo</a>',
                    unsafe_allow_html=True,
                )
        with col_v:
            _view_details(pid, btn_key)
    else:
        col_g, col_d, col_v = st.columns([1, 1, 1])
        with col_g:
            st.markdown('<span></span>', unsafe_allow_html=True)
        with col_d:
            st.markdown('<span></span>', unsafe_allow_html=True)
        with col_v:
            _view_details(pid, btn_key)


def project_card(project: dict, detail_page: str = PROJECT_DETAIL_PAGE, key_suffix: str = "") -> None:
    """Render a single project card.

    Visual hierarchy: title → description → tier → deployment badge →
    categories → technology badges → action buttons (GitHub / Live Demo / View Details).
    """
    name = project.get("name", "Untitled Project")
    desc = project.get("short_description", "")
    categories = project.get("category", [])
    tech = (
        project.get("languages", [])
        + project.get("frameworks", [])
        + project.get("libraries", [])
    )
    pid = project.get("id", "")
    tier = get_tier(project)

    tier_meta = {
        "featured": "⭐ Featured",
        "supporting": "▪ Supporting",
        "experimental": "◈ Experimental",
    }.get(tier, "")

    cat_html = _badges(categories, "blue", limit=5)
    tech_html = _badges(tech, "green", limit=6)
    dep_info = guess_deployment_status(project)

    st.markdown('<div class="gc-card gc-anim-2">', unsafe_allow_html=True)
    tier_html = f'<div class="gc-meta">{tier_meta}</div>' if tier_meta else ""
    st.markdown(
        f'<h3>{_html.escape(name)}</h3>'
        f'{tier_html}'
        f'<div class="gc-desc">{desc}</div>'
        f'<span class="gc-dep-badge {dep_info["cls"]}">{dep_info["label"]}</span>',
        unsafe_allow_html=True,
    )
    if cat_html:
        st.markdown(f'<div>{cat_html}</div>', unsafe_allow_html=True)
    if tech_html:
        st.markdown(f'<div style="margin-top:.2rem;">{tech_html}</div>', unsafe_allow_html=True)

    _render_buttons(project, pid, key_suffix)

    st.markdown("</div>", unsafe_allow_html=True)

