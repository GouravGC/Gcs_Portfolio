"""Deployment showcase — how projects were deployed + architecture patterns."""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.navbar import render_navbar
from components.ui import btn_link, info_note, section_header
from utils.helpers import has_verified_demo, load_projects

st.set_page_config(page_title="Deployment | Gourav Chhatwani", page_icon="🚀", layout="wide")
render_navbar()

projects = load_projects()
deployed = [p for p in projects if p.get("deployment_platform")]

section_header(
    "Deployment Showcase",
    "Production engineering across Streamlit, Flask, and cloud platforms.",
)

# Platform breakdown
platform_counts: dict[str, int] = {}
for p in projects:
    dp = p.get("deployment_platform")
    if dp:
        platform_counts[dp] = platform_counts.get(dp, 0) + 1

cols = st.columns(max(1, len(platform_counts)))
for i, (plat, count) in enumerate(sorted(platform_counts.items())):
    with cols[i % len(platform_counts)]:
        st.metric(label=plat, value=str(count))

st.markdown("---")
section_header(
    "Deployed Projects",
    "Only projects with a verified live demo URL are shown as deployed.",
)

if deployed:
    cols = st.columns(2)
    for i, p in enumerate(deployed):
        with cols[i % 2]:
            st.markdown(f'<div class="gc-card">', unsafe_allow_html=True)
            st.markdown(f"### {p.get('name')}")
            st.markdown(f"**Platform:** {p.get('deployment_platform')}")
            if has_verified_demo(p):
                btn_link("Live Demo", p.get("live_demo_url"), variant="accent")
            btn_link("GitHub", p.get("github_url"), variant="outline")
            st.markdown("</div>", unsafe_allow_html=True)
else:
    info_note("No deployed projects found.", tone="amber")

st.markdown("---")
section_header(
    "Typical Deployment Architecture",
    "A representative end-to-end deployment pattern used across projects.",
)
st.markdown(
    """
    ```
    Raw Data
        ↓
    Data Preprocessing / Feature Engineering
        ↓
    Model Training (scikit-learn / PyTorch / XGBoost / CatBoost)
        ↓
    Artifacts (model.pkl / .pth / scaler / encoders)
        ↓
    Prediction Pipeline
        ↓
    Streamlit / Flask Application
        ↓
    Cloud Deployment (Streamlit Community Cloud / Render)
        ↓
    End User
    ```
    """
)

st.markdown("---")
section_header("MLOps Practices Applied")
st.markdown(
    "- **Experiment tracking** with MLflow (Electricity Forecasting RNN)\n"
    "- **Reproducibility** & validation scripts (Animal-10 Classification)\n"
    "- **Modular src/ architectures** with config, logging & exception handling\n"
    "- **Artifact-based inference** (inference-only apps, no retraining)\n"
    "- **Cached loading** for performant Streamlit apps"
)

render_footer()
