"""Skills page — interactive, evidence-tagged skill explorer."""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
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
    "Skills are tagged by evidence level: Project Demonstrated vs Technical Knowledge.",
)

# Evidence legend
st.markdown(
    '<span class="gc-evidence project">Project Demonstrated</span> — used in a verified public project &nbsp;|&nbsp; '
    '<span class="gc-evidence knowledge">Technical Knowledge</span> — stated knowledge, not yet demonstrated in a project.',
    unsafe_allow_html=True,
)
st.markdown("---")

# Filter by category
cat_names = [c["name"] for c in categories]
sel = st.multiselect("Filter by category", cat_names, default=cat_names)

cols = st.columns(2)
col_idx = 0
for category in categories:
    if category["name"] not in sel:
        continue
    with cols[col_idx % 2]:
        st.markdown(f"### {category['icon']} {category['name']}")
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
