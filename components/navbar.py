"""Navigation helper for the Streamlit multipage app.

Provides a consistent, professional branded header injected at the top of every
page, plus a contextual sidebar hint. The actual page navigation is handled by
Streamlit's built-in multipage sidebar.
"""
from __future__ import annotations

import streamlit as st

from .ui import inject_css


def render_navbar() -> None:
    """Call at the top of every page to inject styles and a consistent header."""
    inject_css()
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:.6rem; padding:.35rem 0;">
            <span style="width:34px; height:34px; border-radius:10px;
                background:linear-gradient(135deg,#4F8CFF,#7C5CFF);
                display:inline-flex; align-items:center; justify-content:center;
                color:#fff; font-weight:800; font-size:.95rem;">GC</span>
            <span style="font-weight:700; font-size:1.05rem; color:#F0F4FF;">Gourav Chhatwani</span>
            <span style="color:#7E8CA8;">· Data Scientist | AI/ML Engineer</span>
        </div>
        <hr style="border:none; border-top:1px solid rgba(255,255,255,.08); margin:.35rem 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )


def render_page_selector() -> None:
    """Render sidebar navigation hint."""
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
