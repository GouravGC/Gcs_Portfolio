"""Project Detail page — deep dive into a selected project.

Project selection is resolved from the Streamlit query parameter ``?id=<project_id>``
set by the View Details link on the listing pages (the single source of truth).
This guarantees the exact project opens and never falls back to another project.

If no valid project id is provided, a clear "PROJECT NOT FOUND" message is shown
and a manual selector is offered (never a silent fallback to a default project,
e.g. the first project or "Student Academic Outcome").
"""
from __future__ import annotations

import streamlit as st

from components.detail_sections import (
    render_architecture,
    render_dataset,
    render_deployment,
    render_github,
    render_key_features,
    render_metrics,
    render_problem_statement,
    render_section,
    render_technical_highlights,
)
from components.footer import render_footer
from components.navbar import render_navbar
from components.ui import section_header
from utils.helpers import get_project_by_id, get_tier, load_projects

st.set_page_config(page_title="Project Detail | Gourav Chhatwani", page_icon="🔍", layout="wide")
render_navbar()

projects = load_projects()
project_ids = [p.get("id") for p in projects]


def _get_qid() -> str | None:
    """Resolve the project id from session_state (set by the View Details card).

    In Streamlit 1.37.x, ``st.switch_page`` clears all query params during the
    switch, so a ``?id=`` query param cannot survive a page change. The reliable
    mechanism is ``st.session_state["selected_project_id"]`` set in normal script
    flow right before the switch. The ``?id=`` query param is kept only as a
    secondary source for deep links, never a fallback to a wrong/default project.
    """
    sid = st.session_state.get("selected_project_id")
    if sid:
        return sid
    raw = st.query_params.get("id", None)
    qid = raw[0] if isinstance(raw, list) else raw
    return qid


selected_id = _get_qid()

# Validate the id against the actual project database. If it is missing or does
# not match any project, show a clear "PROJECT NOT FOUND" message and offer a
# manual selector. Never silently fall back to projects[0] or to a default
# project (e.g. Student Academic Outcome).
valid_ids = set(project_ids)
if selected_id not in valid_ids:
    selected_id = None

if not selected_id:
    options = {p.get("name"): p.get("id") for p in projects}
    # Default a manual pick to the only valid id we already know, so nothing ever
    # falls back to a wrong or placeholder project.
    chosen = st.selectbox(
        "Select a project to view",
        list(options.keys()),
        index=None,
        placeholder="Choose a project…",
    )
    if chosen:
        selected_id = options[chosen]
        # Persist the pick so it survives the natural rerun after this widget event.
        st.session_state["selected_project_id"] = selected_id
        st.query_params["id"] = selected_id

if not selected_id:
    st.error("PROJECT NOT FOUND")
    st.markdown(
        "No matching project was selected. Please choose a project below to view its details."
    )

project = get_project_by_id(selected_id) if selected_id else None

if not project:
    st.warning("PROJECT NOT FOUND — no valid project could be resolved.")
    render_footer()
    st.stop()

# ---- Hero ----
tier = get_tier(project)
tier_label = (
    "⭐ Featured"
    if tier == "featured"
    else "▪ Supporting"
    if tier == "supporting"
    else "◈ Experimental"
)
cat_html = "".join(
    f'<span class="gc-hero-badge">{c}</span>' for c in project.get("category", [])
)
st.markdown(
    f"""
    <div class="gc-hero gc-anim">
        <h1>{project.get("name", "Project")}</h1>
        <div class="gc-title">{tier_label} · <span class="gc-dep-badge badge-blue">{project.get("status", "Not specified")}</span></div>
        <p>{project.get("short_description", "")}</p>
        {f'<div style="margin-top:.9rem;">{cat_html}</div>' if cat_html else ''}
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Hero Actions: GitHub / Live Demo / Back ----
gh = project.get("github_url", "")
demo = project.get("live_demo_url", "")
a1, a2, a3, a4 = st.columns([1, 1, 1, 1])
with a1:
    if gh:
        st.markdown(
            f'<a class="gc-btn gc-btn-primary" href="{gh}" target="_blank" rel="noopener">GitHub</a>',
            unsafe_allow_html=True,
        )
with a2:
    if demo:
        st.markdown(
            f'<a class="gc-btn gc-btn-accent" href="{demo}" target="_blank" rel="noopener">Live Demo</a>',
            unsafe_allow_html=True,
        )
with a3:
    st.markdown("", unsafe_allow_html=True)
with a4:
    back = st.button("← Back to Projects", use_container_width=True)
    if back:
        st.query_params.clear()
        st.switch_page("pages/2_Projects.py")
st.markdown("---")

# ---- Overview ----
section_header("Overview")
st.markdown(project.get("short_description", ""))

render_problem_statement(project.get("problem_statement"))
render_dataset(project)
render_section("Data Processing", project.get("preprocessing"))
render_section("Feature Engineering", project.get("feature_engineering"))
render_section("Models / Algorithms", project.get("models") or project.get("ml_algorithms"))
render_section("Evaluation", project.get("evaluation"))

st.markdown("### Metrics")
render_metrics(project.get("metrics", {}))

render_section("Explainability", project.get("explainability"))
render_architecture(project.get("architecture"))
render_deployment(project)
render_github(project)
render_key_features(project.get("key_features", []))
render_technical_highlights(project.get("technical_highlights", []))

# ---- Technologies ----
st.markdown("### Technologies")
tech = project.get("languages", []) + project.get("frameworks", []) + project.get("libraries", [])
if tech:
    html = "".join(
        f'<span class="gc-badge green">{t}</span>' for t in dict.fromkeys(tech)
    )
    st.markdown(f'<div>{html}</div>', unsafe_allow_html=True)

# ---- MLOps ----
st.markdown("#### MLOps")
mlops = project.get("mlops", [])
if mlops:
    for m in mlops:
        st.markdown(f"- {m}")
else:
    st.markdown("*No verified MLOps details for this project.*")

# ---- Status ----
st.markdown("#### Status")
st.markdown(project.get("status", "Not specified"))

render_footer()

