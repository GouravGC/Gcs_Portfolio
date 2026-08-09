"""Strict hierarchical domain classification & navigation helpers.

Architecture change: each project has EXACTLY ONE ``primary_domain``, an optional
``subcategory`` within that domain, and optional ``secondary_tags``. A project is
counted in its primary domain ONLY. ``secondary_tags`` are informational and never
inflate the primary-domain statistics.

Use ``primary_domain`` for grouping/counting and ``subcategory`` for the nested
visual hierarchy on the Projects page.
"""
from __future__ import annotations

import streamlit as st

# Ordered top-level primary domains and their display metadata.
PRIMARY_DOMAINS = [
    "Data Analytics",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Agentic AI",
    "Recommendation Systems",
]

DOMAIN_META = {
    "Data Analytics": ("📊", "SQL · Pandas · BI dashboards · Power BI"),
    "Machine Learning": ("🤖", "Classical & end-to-end ML pipelines"),
    "Deep Learning": ("🧠", "PyTorch neural networks, CNN, RNN, MLP"),
    "Generative AI": ("✨", "LLM-based apps & generative applications"),
    "Agentic AI": ("🤝", "Autonomous agent applications"),
    "Recommendation Systems": ("🎯", "Recommendation engines & personalization"),
}

# Subcategory display labels (used to build the nested visual hierarchy).
SUBCATEGORY_LABELS = {
    "Supervised Learning": "🎯 Supervised Learning",
    "Unsupervised Learning": "🧩 Unsupervised Learning",
    "Computer Vision": "👁️ Computer Vision",
    "NLP": "💬 NLP",
    "Sequential / Time-Series Deep Learning": "📈 Sequential / Time-Series Deep Learning",
    "Business Intelligence": "📊 Business Intelligence",
    "Analytics Projects": "📈 Analytics Projects",
    "LLM Applications": "✨ LLM Applications",
    "Deep Learning": "🧠 Deep Learning",
    "Recommendation Systems": "🎯 Recommendation Systems",
}

# Subcategory display order within each primary domain.
SUBCATEGORY_ORDER = {
    "Data Analytics": ["Business Intelligence", "Analytics Projects"],
    "Machine Learning": ["Supervised Learning", "Unsupervised Learning"],
    "Deep Learning": ["Computer Vision", "NLP", "Sequential / Time-Series Deep Learning", "Deep Learning"],
    "Generative AI": ["LLM Applications"],
    "Agentic AI": [],
    "Recommendation Systems": ["Recommendation Systems"],
}

# Top-level navigable chips shown on the Projects page.
NAV_DOMAINS = [
    "All",
    "Data Analytics",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "Agentic AI",
]


def primary_domain_count(projects: list[dict], domain: str) -> int:
    """Count projects whose PRIMARY domain is ``domain`` (never from secondary tags)."""
    return sum(1 for p in projects if p.get("primary_domain") == domain)


def count_by_primary_domain(projects: list[dict]) -> dict[str, int]:
    """Return {primary_domain: count} using primary_domain only. Sum == total projects."""
    counts: dict[str, int] = {}
    for p in projects:
        pd = p.get("primary_domain")
        if not pd:
            continue
        counts[pd] = counts.get(pd, 0) + 1
    return counts


def projects_in_primary(projects: list[dict], domain: str) -> list[dict]:
    """Return projects whose primary_domain == domain."""
    return [p for p in projects if p.get("primary_domain") == domain]


def subcategories_for(projects: list[dict], primary: str) -> list[str]:
    """Return the ordered subcategory labels present in a primary domain, honoring
    the canonical SUBCATEGORY_ORDER and falling back to data order."""
    present = {p.get("subcategory") for p in projects_in_primary(projects, primary)}
    # Canonical order first
    ordered = [s for s in SUBCATEGORY_ORDER.get(primary, []) if s in present]
    # Any leftover subcategories not in canonical list
    leftover = [s for s in present if s not in ordered]
    return ordered + leftover


def projects_in_subcategory(projects: list[dict], primary: str, subcategory: str) -> list[dict]:
    return [
        p
        for p in projects
        if p.get("primary_domain") == primary and p.get("subcategory") == subcategory
    ]


def domain_icon(name: str) -> str:
    return DOMAIN_META.get(name, ("🎖", ""))[0]


def subcategory_label(sub: str) -> str:
    return SUBCATEGORY_LABELS.get(sub, sub or "Projects")


def render_subcategory_header(sub: str) -> None:
    """Render a subcategory heading inside a primary domain section."""
    st.markdown(
        f'<div class="gc-subcategory-header gc-anim-down">{subcategory_label(sub)}</div>',
        unsafe_allow_html=True,
    )


def render_domain_header(domain: str) -> None:
    """Render a primary-domain section header with icon and animated title."""
    icon, meta = DOMAIN_META.get(domain, ("🎖", ""))
    st.markdown(
        f'<div class="gc-domain-header gc-anim-down">'
        f'<span class="gc-domain-icon">{icon}</span>'
        f'<div><div class="gc-domain-title">{domain}</div>'
        f'<div class="gc-domain-sub">{meta}</div></div></div>',
        unsafe_allow_html=True,
    )

