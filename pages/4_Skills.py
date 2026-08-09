"""Skills page — interactive, evidence-tagged skill explorer.

Groups skills into professional categories with a category filter, evidence
badges, and a count of demonstrated skills. Layout is dynamic and animated.
"""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.metrics import count_programming_skills
from components.navbar import render_navbar
from components.skill_card import skill_card
from components.ui import info_note, section_header
from utils.helpers import load_skills

st.set_page_config(page_title="Skills | Gourav Chhatwani", page_icon="🛠️", layout="wide")
render_navbar()

skills_data = load_skills()
categories = skills_data.get("categories", [])

section_header(
    "Skills Explorer",
    "Skills are grouped by professional domain and tagged by evidence level.",
)

# Evidence legend
st.markdown(
    '<span class="gc-evidence project">Project Demonstrated</span> — used in a verified public project &nbsp;|&nbsp; '
    '<span class="gc-evidence knowledge">Technical Knowledge</span> — stated knowledge, not yet demonstrated in a project.',
    unsafe_allow_html=True,
)
st.markdown("---")

# Animated count of demonstrated skills (real data, no fabrication).
st.markdown(
    f'<div class="gc-counter gc-anim-down"><span class="gc-metric-value" '
    f'style="font-size:1.6rem;">{count_programming_skills()}</span> '
    f'<span class="gc-metric-label" style="font-size:.85rem;">skills demonstrated in projects</span></div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Filter by category (interactive pills via radio — streamlit-safe).
cat_names = [c["name"] for c in categories]
sel = st.radio(
    "Filter by category",
    ["All"] + cat_names,
    horizontal=True,
    label_visibility="collapsed",
    key="skill_cat_filter",
)

filtered_cats = categories if sel == "All" else [c for c in categories if c["name"] == sel]

cols = st.columns(2)
col_idx = 0
for category in filtered_cats:
    with cols[col_idx % 2]:
        st.markdown(
            f'<div class="gc-domain-header gc-anim-down">'
            f'<span class="gc-domain-icon">{category.get("icon", "🛠️")}</span>'
            f'<div><div class="gc-domain-title">{category["name"]}</div>'
            f'<div class="gc-domain-sub">{len(category.get("skills", []))} skills</div></div></div>',
            unsafe_allow_html=True,
        )
        for skill in category.get("skills", []):
            skill_card(skill)
    col_idx += 1

st.markdown("---")
info_note(
    "Technical Knowledge items are capabilities the candidate has stated knowing. "
    "They are not claimed as production project experience unless tagged Project Demonstrated.",
    tone="amber",
)

render_footer()
