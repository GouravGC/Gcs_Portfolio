"""Metric cards component for displaying key statistics."""
from __future__ import annotations

import streamlit as st

from utils.helpers import has_verified_demo, load_projects


def render_metric_row(label: str, value: str, delta: str | None = None) -> None:
    """Render a single metric card via st.metric."""
    st.metric(label=label, value=value, delta=delta)


def render_portfolio_metrics() -> None:
    """Render a row of headline portfolio metrics derived from the data layer."""
    projects = load_projects()
    total = len(projects)
    featured = sum(1 for p in projects if p.get("featured"))
    deployed = sum(1 for p in projects if has_verified_demo(p))
    categories = set()
    for p in projects:
        categories.update(p.get("category", []))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_row("Total Projects", str(total))
    with c2:
        render_metric_row("Featured", str(featured))
    with c3:
        render_metric_row("Deployed", str(deployed))
    with c4:
        render_metric_row("Categories", str(len(categories)))
