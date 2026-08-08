"""Project Detail page — deep dive into a selected project.

Uses the Streamlit query parameter ?id=<project_id> to select the project.
Renders only sections that have verified information.
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
from utils.helpers import get_project_by_id, load_projects

st.set_page_config(page_title="Project Detail | Gourav Chhatwani", page_icon="🔍", layout="wide")
render_navbar()

projects = load_projects()

# Project selection via query param, fallback to sidebar select
params = st.query_params
selected_id = params.get("id", None)

options = {p.get("name"): p.get("id") for p in projects}
names = list(options.keys())

if selected_id and selected_id in options.values():
    project = get_project_by_id(selected_id)
else:
    default_name = names[0] if names else None
    chosen = st.sidebar.selectbox("Select a project", names, index=0)
    project = get_project_by_id(options[chosen])

if not project:
    st.error("Project not found. Please select a valid project.")
    st.stop()

back = st.button("← Back to Explorer")
if back:
    st.switch_page("pages/2_Projects.py")

section_header(project.get("name", "Project"))
st.caption(" · ".join(project.get("category", [])))
st.markdown(project.get("short_description", ""))

featured = project.get("featured", False)
if featured:
    st.markdown('<span class="gc-badge amber">⭐ Featured</span>', unsafe_allow_html=True)

st.markdown("---")

# Overview
st.markdown("## Overview")
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

st.markdown("### Technologies")
tech = project.get("languages", []) + project.get("frameworks", []) + project.get("libraries", [])
if tech:
    html = "".join(f'<span class="gc-badge green">{t}</span>' for t in dict.fromkeys(tech))
    st.markdown(f'<div>{html}</div>', unsafe_allow_html=True)

st.markdown("#### MLOps")
mlops = project.get("mlops", [])
if mlops:
    for m in mlops:
        st.markdown(f"- {m}")
else:
    st.markdown("*No verified MLOps details for this project.*")

st.markdown("#### Status")
st.markdown(project.get("status", "N/A"))

render_footer()
