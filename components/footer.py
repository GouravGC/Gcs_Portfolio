"""Footer component."""
from __future__ import annotations

import streamlit as st

from utils.helpers import load_profile


def render_footer() -> None:
    """Render a consistent footer using verified profile links."""
    profile = load_profile()
    name = profile.get("name", "Gourav Chhatwani")
    github = profile.get("github", "#")
    linkedin = profile.get("linkedin", "#")
    st.markdown(
        f"""
        <div class="gc-footer">
            © {name} ·
            <a href="{github}" target="_blank" rel="noopener">GitHub</a> ·
            <a href="{linkedin}" target="_blank" rel="noopener">LinkedIn</a> ·
            Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
