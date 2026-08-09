"""Skill card component."""
from __future__ import annotations

import html as _html

import streamlit as st

EVIDENCE_LABEL = {
    "project_demonstrated": "Project Demonstrated",
    "technical_knowledge": "Technical Knowledge",
}


def skill_card(skill: dict) -> None:
    """Render a single skill as an elegant badge with its evidence label."""
    name = skill.get("name", "Untitled")
    evidence = skill.get("evidence", "technical_knowledge")
    label = EVIDENCE_LABEL.get(evidence, "Technical Knowledge")
    cls = "gc-evidence project" if evidence == "project_demonstrated" else "gc-evidence knowledge"

    st.markdown(
        f"""
        <div class="gc-card">
            <strong>{_html.escape(name)}</strong>
            <div style="margin-top:.35rem;">
                <span class="{cls}">{label}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def skill_badge(name: str, evidence: str = "technical_knowledge") -> None:
    """Render a compact inline skill badge."""
    cls = "gc-badge green" if evidence == "project_demonstrated" else "gc-badge blue"
    st.markdown(f'<span class="{cls}">{_html.escape(name)}</span>', unsafe_allow_html=True)
