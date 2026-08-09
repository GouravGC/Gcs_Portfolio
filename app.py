"""Gourav Chhatwani — Data Scientist | AI/ML Engineer Portfolio.

Entry point for the Streamlit application. This is the Home/Hero page.
All pages live under pages/ and share a modular, data-driven architecture.
"""
from __future__ import annotations

import streamlit as st

from components.metrics import render_portfolio_metrics
from components.navbar import render_navbar, render_page_selector
from components.project_card import project_card
from components.ui import btn_link, render_hero, section_header
from utils.helpers import get_tier, load_profile, load_projects

st.set_page_config(
    page_title="Gourav Chhatwani | Data Scientist & AI/ML Engineer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_navbar()
render_page_selector()

profile = load_profile()
projects = load_projects()

HERO_TAGS = [
    "📊 Data Analytics",
    "🤖 Machine Learning",
    "🧠 Deep Learning",
    "✨ Generative AI",
    "🚀 Deployment",
    "⚙️ MLOps",
]

render_hero(
    name=profile["name"],
    title=profile["professional_title"],
    summary=profile["summary"],
    tags=HERO_TAGS,
)

# Action buttons — every button must work.
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.page_link("pages/6_Resume.py", label="📄 Download Resume")
with c2:
    btn_link("GitHub", profile["github"], variant="primary")
with c3:
    btn_link("LinkedIn", profile["linkedin"], variant="outline")
with c4:
    st.page_link("pages/2_Projects.py", label="🛠 View Projects")

st.markdown("---")

section_header(
    "Portfolio at a Glance",
    "A broad, hands-on, end-to-end project portfolio built as a fresher.",
)
render_portfolio_metrics()

st.markdown("---")
section_header(
    "Featured Projects",
    "Production-oriented projects spanning analytics, ML, deep learning, time series, recommendations, and deployment.",
)

featured = [p for p in projects if get_tier(p) == "featured"]
if featured:
    cols = st.columns(2)
    for i, proj in enumerate(featured[:8]):
        with cols[i % 2]:
            project_card(proj)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    section_header("About Me")
    st.markdown(
        "An aspiring Data Scientist and AI/ML Engineer who has built a wide range of "
        "real, end-to-end projects — from SQL and analytics dashboards to deep learning, "
        "time-series forecasting, recommendation systems, and cloud-deployed applications. "
        "View the **About** page for the full learning journey."
    )
with c2:
    section_header("Get Started")
    st.markdown(
        "- **Projects** · Explore the full project archive with filters and search.\n"
        "- **Skills** · Browse evidence-tagged skills.\n"
        "- **Deployment** · See how projects are shipped.\n"
        "- **Resume** · Download the master resume.\n"
    )

st.markdown("---")
st.caption(
    "Built from the candidate's public GitHub. Live Demo buttons appear for projects "
    "that provide a deployment URL. All external links are manually verified by the candidate."
)
