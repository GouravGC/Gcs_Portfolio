"""Metric cards component for displaying key statistics.

Headline metrics are derived from each project's PRIMARY domain (project.primary_domain)
so a project is counted exactly once. No numbers are fabricated and no project is
counted multiple times across domains.
"""
from __future__ import annotations

import streamlit as st

from components.domain import PRIMARY_DOMAINS, count_by_primary_domain
from components.ui import metric_card
from utils.helpers import has_verified_demo, load_projects, load_skills

_DOMAIN_ICONS = {
    "Data Analytics": "📊",
    "Machine Learning": "🤖",
    "Deep Learning": "🧠",
    "Generative AI": "✨",
    "Agentic AI": "🤝",
    "Recommendation Systems": "🎯",
}


def render_portfolio_metrics() -> None:
    """Render a row of headline portfolio metrics derived from the data layer."""
    projects = load_projects()
    total = len(projects)
    featured = sum(1 for p in projects if p.get("featured"))
    deployed = sum(1 for p in projects if has_verified_demo(p))
    domains = count_by_primary_domain(projects)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(str(total), "Total Projects")
    with c2:
        metric_card(str(len(domains)), "Primary Domains")
    with c3:
        metric_card(str(deployed), "Deployed")
    with c4:
        metric_card(str(featured), "Featured")


def render_domain_breakdown(projects: list[dict]) -> None:
    """Render animated counters per PRIMARY domain.

    Counts are derived from ``primary_domain`` only, so the sum always equals the
    total number of unique projects. Secondary tags never contribute here.
    """
    counts = count_by_primary_domain(projects)
    if not counts:
        return

    ordered = [d for d in PRIMARY_DOMAINS if counts.get(d)]
    if not ordered:
        return

    cols = st.columns(min(4, max(1, len(ordered))))
    for i, domain in enumerate(ordered):
        icon = _DOMAIN_ICONS.get(domain, "🎖")
        with cols[i % len(cols)]:
            st.markdown(
                f"""<div class="gc-metric-card gc-anim-2">
                    <div class="gc-metric-value gc-counter"><span>{counts[domain]}</span></div>
                    <div class="gc-metric-label">{icon} {domain}</div>
                </div>""",
                unsafe_allow_html=True,
            )


def count_programming_skills() -> int:
    """Return the number of project_demonstrated skills (for the Skills page)."""
    data = load_skills()
    return sum(
        1
        for category in data.get("categories", [])
        for skill in category.get("skills", [])
        if skill.get("evidence") == "project_demonstrated"
    )
