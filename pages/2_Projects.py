"""Project Explorer — search, filter, and browse all verified projects."""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.navbar import render_navbar
from components.project_card import project_card
from components.ui import info_note, section_header
from utils.helpers import (
    get_tier,
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

# ---- Filters sidebar ----
st.sidebar.markdown("### Project Filters")
search = st.sidebar.text_input("Search", placeholder="e.g. fraud, pytorch, sales…")

tier_options = ["All tiers", "Featured", "Supporting", "Experimental"]
sel_tier = st.sidebar.selectbox("Tier", tier_options)

cats = ["All categories"] + list_categories(projects)
sel_cat = st.sidebar.selectbox("Category", cats)

techs = list_technologies(projects)
sel_techs = st.sidebar.multiselect("Technologies", techs)

platforms = ["All deployments"] + list_deployment_platforms(projects)
sel_platform = st.sidebar.selectbox("Deployment Platform", platforms)

deployed_only = st.sidebar.checkbox("Deployed (has live demo URL) only", value=False)

# ---- Apply filters ----
filtered = []
for p in projects:
    if sel_tier != "All tiers" and get_tier(p) != sel_tier.lower():
        continue
    if sel_cat != "All categories" and sel_cat not in p.get("category", []):
        continue
    if deployed_only and not p.get("live_demo_url"):
        continue
    if sel_platform != "All deployments":
        if p.get("deployment_platform") != sel_platform:
            continue
    if sel_techs:
        p_techs = set(p.get("languages", []) + p.get("frameworks", []) + p.get("libraries", []))
        if not any(t in p_techs for t in sel_techs):
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
    tier_rank = {"featured": 0, "supporting": 1, "experimental": 2}
    filtered.sort(key=lambda x: (tier_rank.get(get_tier(x), 1), x.get("name", "")))
    st.markdown('<div class="gc-anim-stagger">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, proj in enumerate(filtered):
        with cols[i % 2]:
            project_card(proj)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "Live Demo buttons appear for projects that provide a deployment URL. "
    "Projects without a demo URL are clearly marked."
)

render_footer()
