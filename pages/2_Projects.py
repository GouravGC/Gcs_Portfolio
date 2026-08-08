"""Project Explorer — search, filter, and browse all verified projects."""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.navbar import render_navbar
from components.project_card import project_card
from components.ui import info_note, section_header
from utils.helpers import (
    list_categories,
    list_deployment_platforms,
    list_technologies,
    load_projects,
)

st.set_page_config(page_title="Projects | Gourav Chhatwani", page_icon="📁", layout="wide")
render_navbar()

projects = load_projects()
section_header(
    "Project Explorer",
    "Search, filter, and explore the full portfolio of verified projects.",
)

# Filters sidebar section
st.sidebar.markdown("### Project Filters")

search = st.sidebar.text_input("Search", placeholder="e.g. fraud, pytorch, sales…")

cats = list_categories(projects)
sel_cats = st.sidebar.multiselect("Categories", cats)

techs = list_technologies(projects)
sel_techs = st.sidebar.multiselect("Technologies", techs)

platforms = list_deployment_platforms(projects)
sel_platforms = st.sidebar.multiselect("Deployment", platforms)

show_only_featured = st.sidebar.checkbox("Featured only", value=False)
show_only_deployed = st.sidebar.checkbox("Deployed (verified demo) only", value=False)

# Apply filters
filtered = []
for p in projects:
    if show_only_featured and not p.get("featured"):
        continue
    if show_only_deployed and not p.get("live_demo_url"):
        continue
    if sel_cats and not any(c in sel_cats for c in p.get("category", [])):
        continue
    if sel_techs:
        p_techs = set(p.get("languages", []) + p.get("frameworks", []) + p.get("libraries", []))
        if not any(t in p_techs for t in sel_techs):
            continue
    if sel_platforms:
        dp = p.get("deployment_platform")
        if dp not in sel_platforms:
            continue
    if search:
        haystack = " ".join(
            [
                p.get("name", ""),
                p.get("short_description", ""),
                " ".join(p.get("category", [])),
                " ".join(p.get("languages", [])),
                " ".join(p.get("frameworks", [])),
                " ".join(p.get("libraries", [])),
            ]
        ).lower()
        if search.lower() not in haystack:
            continue
    filtered.append(p)

st.caption(f"Showing {len(filtered)} of {len(projects)} projects.")

if not filtered:
    info_note("No projects match the current filters. Try adjusting your selections.", tone="amber")
else:
    # Order featured first, then by name
    filtered.sort(key=lambda x: (not x.get("featured"), x.get("name", "")))
    cols = st.columns(2)
    for i, proj in enumerate(filtered):
        with cols[i % 2]:
            project_card(proj)

st.markdown("---")
st.caption(
    "Live Demo buttons appear only for projects with a verified deployment URL. "
    "Projects without a verified demo are clearly marked."
)

render_footer()
