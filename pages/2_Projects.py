"""Project Explorer — strict hierarchical, domain-organized project browsing.

Each project has exactly ONE primary domain (and an optional subcategory). The
Projects page renders the hierarchy visually:

    DATA ANALYTICS            (primary domain heading)
        Business Intelligence (subcategory heading)
            [Sales BI] [HR Analytics] ...
        Analytics Projects
            [...]

    MACHINE LEARNING
        Supervised Learning
            [Fraud Detection] [Loan Default] ...
        Unsupervised Learning
            [Customer Segmentation] ...

    DEEP LEARNING
        Computer Vision
            [...]
        Sequential / Time-Series Deep Learning
            [Electricity Forecasting] ...

Domain nav uses a styled ``st.radio`` (safe on all supported Streamlit versions).
View Details carries each project's unique id via session_state + query params.
"""
from __future__ import annotations

import streamlit as st

from components.domain import (
    NAV_DOMAINS,
    PRIMARY_DOMAINS,
    render_domain_header,
    render_subcategory_header,
    projects_in_primary,
    subcategories_for,
    projects_in_subcategory,
)
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
    "Organsied by a strict domain hierarchy — each project belongs to one primary domain.",
)

# ---- Domain navigation (horizontal, styled radio) ----
sel_domain = st.radio(
    "Domain",
    NAV_DOMAINS,
    index=0,
    horizontal=True,
    label_visibility="collapsed",
    key="domain_nav",
)

st.markdown("---")

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


def _matches_filters(p: dict) -> bool:
    if sel_tier != "All tiers" and get_tier(p) != sel_tier.lower():
        return False
    if sel_cat != "All categories" and sel_cat not in p.get("category", []):
        return False
    if deployed_only and not p.get("live_demo_url"):
        return False
    if sel_platform != "All deployments":
        if p.get("deployment_platform") != sel_platform:
            return False
    if sel_techs:
        p_techs = set(p.get("languages", []) + p.get("frameworks", []) + p.get("libraries", []))
        if not any(t in p_techs for t in sel_techs):
            return False
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
            return False
    return True


def _tier_sort_key(p: dict):
    rank = {"featured": 0, "supporting": 1, "experimental": 2}
    return (rank.get(get_tier(p), 1), p.get("name", ""))


def _render_cards(cards: list[dict], section_id: str = "") -> None:
    if not cards:
        return
    cards.sort(key=_tier_sort_key)
    st.markdown('<div class="gc-anim-stagger">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, proj in enumerate(cards):
        with cols[i % 2]:
            # Unique suffix per section so the same project never gets a duplicate
            # button key (each project appears in exactly one primary domain).
            project_card(proj, key_suffix=f"__{section_id}__{i}")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_primary_section(primary: str, base: list[dict]) -> None:
    """Render a primary domain with its subcategory headings and project cards."""
    render_domain_header(primary)
    subs = subcategories_for(base, primary)
    if not subs:
        # Primary domain has projects but no subcategory label -> show directly.
        _render_cards(base, section_id=primary.replace(" ", "_"))
        return
    for sub in subs:
        cards = projects_in_subcategory(base, primary, sub)
        if not cards:
            continue
        render_subcategory_header(sub)
        _render_cards(cards, section_id=f"{primary.replace(' ', '_')}__{sub.replace(' ', '_')}")
    st.markdown("---")


# ---- Filter all projects once ----
filtered_all = [p for p in projects if _matches_filters(p)]

if sel_domain == "All":
    shown_any = False
    for primary in PRIMARY_DOMAINS:
        base = [p for p in filtered_all if _matches_filters(p)]
        base = projects_in_primary(base, primary)
        if not base:
            # Only show a simple placeholder for Agentic AI (no fabrication).
            if primary == "Agentic AI":
                st.markdown(
                    '<div class="gc-domain-header gc-anim-down">'
                    '<span class="gc-domain-icon">🤝</span>'
                    '<div><div class="gc-domain-title">Agentic AI</div>'
                    '<div class="gc-domain-sub">Coming soon — autonomous agent projects will appear '
                    'here when published.</div></div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown("---")
            continue
        shown_any = True
        _render_primary_section(primary, base)
    if not shown_any:
        info_note("No projects match the current filters.", tone="amber")
else:
    base = [p for p in filtered_all if _matches_filters(p)]
    base = projects_in_primary(base, sel_domain)
    if not base:
        if sel_domain == "Agentic AI":
            info_note(
                "No Agentic AI projects are published yet. This section is data-driven and will "
                "populate automatically when an Agentic AI project is added.",
                tone="amber",
            )
        else:
            info_note("No projects in this domain match the current filters.", tone="amber")
    else:
        _render_primary_section(sel_domain, base)

st.markdown("---")
st.caption(
    "Each project belongs to exactly one primary domain. Subcategory headings organise "
    "projects within a domain. Live Demo buttons appear only when a deployment URL exists."
)

render_footer()
