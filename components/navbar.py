"""Navigation helper for the Streamlit multipage app.

Streamlit provides built-in sidebar navigation via the `pages/` directory. This
component renders a consistent, professional header + contextual sidebar hint.
"""
from __future__ import annotations

import streamlit as st

from .ui import inject_css


def render_navbar() -> None:
    """Call at the top of every page to inject styles and a consistent header."""
    inject_css()
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:.5rem; padding:.25rem 0;">
            <span style="font-weight:700; font-size:1.05rem;">Gourav Chhatwani</span>
            <span style="color:#64748b;">· Data Scientist | AI/ML Engineer</span>
        </div>
        <hr style="border:none; border-top:1px solid #e2e8f0; margin:.25rem 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )


def render_page_selector() -> None:
    """Render a small labelled hint for the sidebar navigation."""
    st.sidebar.markdown("### **Navigation**")
    st.sidebar.markdown(
        "Use the sidebar to explore the portfolio:\n"
        "- **Home** · Hero & overview\n"
        "- **About** · Journey & background\n"
        "- **Projects** · Explorer & filters\n"
        "- **Project Detail** · Deep dive\n"
        "- **Skills** · Evidence-tagged skills\n"
        "- **Deployment** · Showcase & architecture\n"
        "- **Resume** · Download master resume\n"
    )
