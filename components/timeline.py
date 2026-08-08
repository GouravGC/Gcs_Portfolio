"""Technical journey timeline component."""
from __future__ import annotations

import streamlit as st


def render_journey_timeline(steps: list[str], description: str) -> None:
    """Render a vertical timeline illustrating the candidate's learning journey.

    This is a learning and project-development journey, NOT professional
    employment experience.
    """
    st.markdown(f'<div class="gc-note">{description}</div>', unsafe_allow_html=True)

    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        connector = "" if is_last else "│"
        st.markdown(
            f"""
            <div style="display:flex; gap:.9rem; align-items:stretch;">
                <div style="display:flex; flex-direction:column; align-items:center;">
                    <span style="width:14px; height:14px; border-radius:50%;
                        background:#2563eb; margin-top:.2rem;"></span>
                    {("<span style='color:#cbd5e1; font-size:1rem; line-height:1.4;'>" + connector + "</span>") if not is_last else ""}
                </div>
                <div style="padding-bottom:1.1rem;">
                    <strong style="color:#0f172a;">{step}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
