"""UI helpers: custom CSS, injected styles, and small rendering utilities.

Kept dependency-light and re-usable across pages. Uses st.markdown with
unsafe_allow_html only where needed for controlled, professional styling.
"""
from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    """Inject the global custom stylesheet once."""
    css = """
    <style>
    /* Typography & base */
    .gc-root { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    /* Hero section */
    .gc-hero {
        padding: 2.5rem 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #f6f8fc 0%, #eef2f8 100%);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .gc-hero h1 { font-size: 2.6rem; font-weight: 700; margin: 0; color: #0f172a; }
    .gc-hero .gc-title { font-size: 1.25rem; color: #2563eb; font-weight: 600; margin-top: .25rem; }
    .gc-hero p { color: #334155; max-width: 760px; }

    /* Buttons */
    .gc-btn {
        display: inline-block; padding: .55rem 1.1rem; border-radius: 9px;
        font-weight: 600; font-size: .9rem; text-decoration: none;
        margin-right: .5rem; margin-bottom: .4rem; transition: all .15s ease;
        border: 1px solid transparent;
    }
    .gc-btn-primary { background: #0f172a; color: #fff; }
    .gc-btn-primary:hover { background: #1e293b; }
    .gc-btn-outline { background: transparent; color: #0f172a; border-color: #cbd5e1; }
    .gc-btn-outline:hover { border-color: #0f172a; }
    .gc-btn-accent { background: #2563eb; color: #fff; }
    .gc-btn-accent:hover { background: #1d4ed8; }

    /* Cards */
    .gc-card {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: box-shadow .15s ease, transform .15s ease;
    }
    .gc-card:hover { box-shadow: 0 6px 18px rgba(0,0,0,0.08); transform: translateY(-2px); }
    .gc-card h3 { margin: 0 0 .25rem; font-size: 1.1rem; color: #0f172a; }
    .gc-card .gc-desc { color: #475569; font-size: .9rem; min-height: 2.6rem; }

    /* Badges */
    .gc-badge {
        display: inline-block; padding: .18rem .55rem; border-radius: 999px;
        font-size: .72rem; font-weight: 600; margin-right: .3rem; margin-bottom: .3rem;
        background: #eef2ff; color: #3730a3;
    }
    .gc-badge.blue { background: #dbeafe; color: #1e40af; }
    .gc-badge.green { background: #dcfce7; color: #166534; }
    .gc-badge.amber { background: #fef3c7; color: #92400e; }

    /* Section headings */
    .gc-section-title { font-size: 1.6rem; font-weight: 700; color: #0f172a; margin: 1.5rem 0 .25rem; }
    .gc-section-sub { color: #64748b; margin-bottom: 1rem; }

    /* Placement note */
    .gc-note {
        background: #f8fafc; border-left: 4px solid #2563eb; padding: .75rem 1rem;
        border-radius: 0 8px 8px 0; font-size: .85rem; color: #334155; margin: 1rem 0;
    }
    .gc-note.amber { border-color: #f59e0b; }

    /* Evidence tags */
    .gc-evidence.project { color: #166534; font-weight: 600; }
    .gc-evidence.knowledge { color: #92400e; font-weight: 600; }

    /* Footer */
    .gc-footer { text-align: center; color: #94a3b8; font-size: .8rem; padding: 1.5rem 0; border-top: 1px solid #e2e8f0; margin-top: 2rem; }

    /* Dark mode overrides */
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-hero {
        background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
        border-color: rgba(255,255,255,.06);
    }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-hero h1 { color: #f8fafc; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-hero p { color: #cbd5e1; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-card { background: #1e293b; border-color: #334155; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-card h3 { color: #f1f5f9; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-card .gc-desc { color: #cbd5e1; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-section-title { color: #f1f5f9; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-footer { color: #64748b; border-color: #334155; }
    [data-testid="stAppViewContainer"][data-theme="dark"] .gc-note { background: #1e293b; color: #cbd5e1; }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(name: str, title: str, summary: str) -> None:
    """Render the hero banner."""
    st.markdown(
        f"""
        <div class="gc-hero">
            <h1>{name}</h1>
            <div class="gc-title">{title}</div>
            <p>{summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    """Render a section header."""
    sub_html = f'<div class="gc-section-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="gc-section-title">{title}</div>{sub_html}',
        unsafe_allow_html=True,
    )


def info_note(text: str, tone: str = "default") -> None:
    """Render an informational note box."""
    cls = "gc-note amber" if tone == "amber" else "gc-note"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def btn_link(label: str, url: str, variant: str = "outline") -> None:
    """Render a styled button that opens a URL in a new tab."""
    cls = {
        "primary": "gc-btn-primary",
        "outline": "gc-btn-outline",
        "accent": "gc-btn-accent",
    }.get(variant, "gc-btn-outline")
    st.markdown(
        f'<a class="gc-btn {cls}" href="{url}" target="_blank" rel="noopener">{label}</a>',
        unsafe_allow_html=True,
    )


def render_footer(name: str, github: str, linkedin: str) -> None:
    """Render the footer."""
    st.markdown(
        f"""
        <div class="gc-footer">
            © {name} · <a href="{github}" target="_blank" rel="noopener">GitHub</a>
            · <a href="{linkedin}" target="_blank" rel="noopener">LinkedIn</a>
            · Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
