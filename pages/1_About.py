"""About page — candidate background and technical journey."""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.navbar import render_navbar
from components.timeline import render_journey_timeline
from components.ui import render_hero, section_header
from utils.helpers import load_profile

st.set_page_config(page_title="About | Gourav Chhatwani", page_icon="👤", layout="wide")
render_navbar()

profile = load_profile()
render_hero(
    name=profile["name"],
    title=profile["professional_title"],
    summary=profile["summary"],
    tags=["🎓 Self-driven Journey", "📈 End-to-End Projects", "☁️ Cloud & MLOps"],
)

section_header("About Me")
st.markdown(
    "I am a **fresher** building a strong, hands-on foundation in Data Science and AI "
    "through real, end-to-end projects. My work spans the full pipeline — from SQL and "
    "analytical dashboards, to classical machine learning, deep learning, computer vision, "
    "time-series forecasting, recommendation systems, and finally modern AI engineering "
    "and cloud deployment."
)

st.markdown("---")
section_header(
    "Technical Journey",
    "A self-driven learning and project-development path (not professional employment).",
)
render_journey_timeline(profile["journey"], profile["journey_description"])

st.markdown("---")
section_header("What This Portfolio Demonstrates")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "### Foundations\n"
        "- Python, SQL & data tooling\n"
        "- Mathematics & statistics\n"
        "- Data preprocessing, EDA & feature engineering\n"
        "- Databases (SQLite, MongoDB, DuckDB)"
    )
with c2:
    st.markdown(
        "### Applied AI / Engineering\n"
        "- Supervised & unsupervised machine learning\n"
        "- Deep learning (PyTorch: CNN, RNN, MLP)\n"
        "- Time-series forecasting & recommendation systems\n"
        "- MLOps (MLflow), deployment (Streamlit, Flask, Render)"
    )

st.markdown("---")
section_header("Fresher Positioning")
st.markdown(
    "This portfolio is evidence-driven. Every project, metric, and deployment link is "
    "drawn from public GitHub repositories. Where personal information could not be "
    "verified, it is clearly marked as a placeholder rather than fabricated."
)

render_footer()
