"""Metric cards component for displaying key statistics."""
from __future__ import annotations

import streamlit as st

from components.ui import metric_card
from utils.helpers import has_verified_demo, load_projects


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
        metric_card(str(total), "Total Projects")
    with c2:
        metric_card(str(featured), "Featured")
    with c3:
        metric_card(str(deployed), "Deployed")
    with c4:
        metric_card(str(len(categories)), "Categories")
