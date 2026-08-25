"""Technical journey timeline component."""
from __future__ import annotations

import html
import streamlit as st


def render_journey_timeline(steps: list[str], description: str) -> None:
    """Render a vertical timeline illustrating the candidate's learning journey.

    This is a learning and project-development journey, NOT professional
    employment experience.
    """
    st.markdown(
        f'<div class="gc-note">{html.escape(description)}</div>',
        unsafe_allow_html=True,
    )

    last = len(steps) - 1

    for i, step in enumerate(steps):
        is_last = i == last

        line_html = ""
        if not is_last:
            line_html = (
                '<div class="gc-timeline-line" '
                'style="flex:1; min-height:2.2rem;"></div>'
            )

        timeline_html = f"""
        <div class="gc-timeline-step gc-anim-2">
            <div style="display:flex; flex-direction:column; align-items:center;">
                <div class="gc-timeline-dot">{i + 1}</div>
                {line_html}
            </div>
            <div class="gc-timeline-label">{html.escape(str(step))}</div>
        </div>
        """

        st.html(timeline_html)