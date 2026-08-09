"""UI helpers: custom CSS, injected styles, and small rendering utilities.

Provides the premium dark-first design system used across the portfolio.
Kept dependency-light and re-usable across pages. Uses st.markdown with
unsafe_allow_html only where needed for controlled, professional styling.
"""
from __future__ import annotations

import streamlit as st

# -------- Accent & palette tokens (kept in sync with config.toml) --------
ACCENT = "#4F8CFF"
ACCENT_DARK = "#3B6FE0"
BG = "#0B1220"
SURFACE = "#111A2E"
SURFACE_2 = "#17223800"

# -------- Deployment status badge metadata --------
# status -> (label, css class)
DEPLOYMENT_BADGES = {
    "live": ("🟢 Live Demo", "badge-green"),
    "streamlit_cloud": ("🔵 Streamlit Community Cloud", "badge-blue"),
    "render": ("🟣 Render", "badge-purple"),
    "flask_api": ("🟠 Flask API", "badge-orange"),
    "github_only": ("⚪ GitHub Only", "badge-gray"),
    "not_deployed": ("⚫ Not Deployed", "badge-dark"),
}


def guess_deployment_status(project: dict) -> dict:
    """Derive a deployment badge from a project's data layer.

    Uses only information already present in the data (no network checks).
    Returns (label, css_class) keyed by the DEPLOYMENT_BADGES mapping.
    """
    demo = project.get("live_demo_url")
    platform = (project.get("deployment_platform") or "").lower()
    status = project.get("deployment_status", "").lower()

    if status:
        for key, (label, cls) in DEPLOYMENT_BADGES.items():
            if status == key:
                return {"label": label, "cls": cls}

    if demo:
        if "render" in platform:
            return {"label": "🟣 Render", "cls": "badge-purple"}
        if "flask" in platform:
            return {"label": "🟠 Flask API", "cls": "badge-orange"}
        if "streamlit" in platform:
            return {"label": "🔵 Streamlit Community Cloud", "cls": "badge-blue"}
        return {"label": "🟢 Live Demo", "cls": "badge-green"}

    if project.get("github_url"):
        return {"label": "⚪ GitHub Only", "cls": "badge-gray"}

    return {"label": "⚫ Not Deployed", "cls": "badge-dark"}


def inject_css() -> None:
    """Inject the global custom stylesheet once."""
    css = """
    <style>
    /* ===== Base & typography ===== */
    .gc-root { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

/* Hide Streamlit branding & default chrome */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background: radial-gradient(1200px 600px at 80% -10%, rgba(79,140,255,.08), transparent 55%), radial-gradient(900px 500px at -10% 110%, rgba(124,92,255,.07), transparent 55%), #0B1220; }
    [data-testid="stHeader"] { background: rgba(11,18,32,0.72); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.06); }
    [data-testid="stSidebar"] { background: #0E1626; border-right: 1px solid rgba(255,255,255,0.06); }
    [data-testid="stSidebar"] a, [data-testid="stSidebar"] .stMarkdown { color:#C6D4EA; }
    [data-testid="stSidebar"] a:hover { color:#9EC0FF; }

    /* ===== Base typography ===== */
    .gc-root, .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    h1, h2, h3 { letter-spacing:-0.3px; }
    p, li { color:#C6D4EA; line-height:1.6; }
    a { color:#8FB4FF; }

    /* ===== Animations ===== */
    @keyframes gcFadeUp { from { opacity: 0; transform: translateY(14px);} to { opacity: 1; transform: translateY(0);} }
    @keyframes gcFadeDown { from { opacity: 0; transform: translateY(-14px);} to { opacity: 1; transform: translateY(0);} }
    @keyframes gcSlideRight { from { opacity: 0; transform: translateX(-18px);} to { opacity: 1; transform: translateX(0);} }
    @keyframes gcFadeIn { from { opacity: 0;} to { opacity: 1;} }
    .gc-anim { animation: gcFadeUp .5s ease both; }
    .gc-anim-2 { animation: gcFadeIn .7s ease both; }
    .gc-anim-down { animation: gcFadeDown .55s ease both; }
    .gc-anim-right { animation: gcSlideRight .6s ease both; }
    .gc-anim-stagger > * { animation: gcFadeUp .6s ease both; }
    .gc-anim-stagger > *:nth-child(1) { animation-delay: .02s; }
    .gc-anim-stagger > *:nth-child(2) { animation-delay: .08s; }
    .gc-anim-stagger > *:nth-child(3) { animation-delay: .14s; }
    .gc-anim-stagger > *:nth-child(4) { animation-delay: .2s; }
    .gc-anim-stagger > *:nth-child(5) { animation-delay: .26s; }
    @media (prefers-reduced-motion: reduce) {
        .gc-anim, .gc-anim-2, .gc-anim-down, .gc-anim-right, .gc-anim-stagger > * { animation: none !important; }
    }

    /* ===== Hero ===== */
    .gc-hero {
        padding: 3rem 2rem;
        border-radius: 22px;
        background:
            radial-gradient(900px 360px at 12% -10%, rgba(79,140,255,0.28), transparent 60%),
            radial-gradient(700px 300px at 100% 0%, rgba(124,92,255,0.18), transparent 55%),
            linear-gradient(135deg, #131C33 0%, #0B1220 60%, #0D1120 100%);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 60px rgba(0,0,0,0.45);
        margin-bottom: 1.75rem;
        position: relative;
        overflow: hidden;
    }
    .gc-hero::after {
        content: "";
        position: absolute; inset: 0;
        background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.04) 50%, transparent 100%);
        pointer-events: none;
    }
    .gc-hero h1 { font-size: 2.9rem; font-weight: 800; margin: 0; color: #F5F8FF; letter-spacing:-0.5px; }
    .gc-hero .gc-title { font-size: 1.35rem; color: #8FB4FF; font-weight: 600; margin-top: .4rem; }
    .gc-hero .gc-hero-badge {
        display:inline-block; padding:.3rem .8rem; border-radius:999px; font-size:.75rem;
        font-weight:600; letter-spacing:.4px; background:rgba(79,140,255,.15);
        color:#9EC0FF; border:1px solid rgba(79,140,255,.3); margin-right:.4rem; margin-bottom:.4rem;
    }
    .gc-hero p { color: #AEBBD4; max-width: 780px; font-size: 1.02rem; line-height: 1.6; }

/* ===== Buttons ===== */
    .gc-btn {
        display: inline-flex; align-items: center; justify-content: center;
        padding: .66rem 1.35rem; border-radius: 10px;
        font-weight: 700; font-size: .9rem; line-height: 1.2; text-decoration: none;
        margin-right: .5rem; margin-bottom: .5rem;
        letter-spacing: .2px; white-space: nowrap;
        transition: transform .18s ease, box-shadow .18s ease, background .18s ease,
                    border-color .18s ease, filter .18s ease;
        border: 1px solid transparent; cursor: pointer; will-change: transform;
    }
    .gc-btn:hover { transform: translateY(-2px) scale(1.01); filter: brightness(1.08); }
    .gc-btn:active { transform: translateY(0) scale(.98); filter: brightness(.95); }
    .gc-btn:focus-visible {
        outline: 3px solid #9EC0FF; outline-offset: 2px;
    }
    .gc-btn-primary {
        background: linear-gradient(135deg, #4F8CFF, #3B6FE0);
        color: #FFFFFF !important; border-color: rgba(255,255,255,.25);
        box-shadow: 0 6px 18px rgba(79,140,255,.38);
    }
    .gc-btn-primary:hover { box-shadow: 0 12px 30px rgba(79,140,255,.55); border-color: #fff; }
    .gc-btn-primary:active { box-shadow: 0 4px 14px rgba(79,140,255,.4); }
    .gc-btn-primary:focus-visible { outline-color: #C9DCFF; }
    .gc-btn-outline {
        background: rgba(255,255,255,.06); color: #F0F4FF !important;
        border: 1px solid rgba(255,255,255,.35);
    }
    .gc-btn-outline:hover { border-color: rgba(255,255,255,.85); background: rgba(255,255,255,.12); color:#FFFFFF !important; }
    .gc-btn-outline:active { background: rgba(255,255,255,.04); }
    .gc-btn-outline:focus-visible { outline-color: #E6EDF7; }
    .gc-btn-accent {
        background: linear-gradient(135deg, #2DD4BF, #4F8CFF);
        color: #06211D !important; border-color: rgba(255,255,255,.22);
        box-shadow: 0 6px 18px rgba(45,212,191,.32);
    }
    .gc-btn-accent:hover { box-shadow: 0 12px 30px rgba(45,212,191,.5); border-color: #fff; color:#06211D !important; }
    .gc-btn-accent:active { box-shadow: 0 4px 14px rgba(45,212,191,.4); }
    .gc-btn-accent:focus-visible { outline-color: #8BEFE4; }

    /* Streamlit-native buttons (View Details, Download, navigation) — force
       readable text in both the dark and inherited light themes. */
    .stButton > button,
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"] {
        font-weight: 700 !important; border-radius: 10px !important;
        color: #FFFFFF !important; background: linear-gradient(135deg, #3B6FE0, #2B55C4) !important;
        border: 1px solid rgba(255,255,255,.3) !important;
        transition: transform .18s ease, box-shadow .18s ease, background .18s ease,
                    border-color .18s ease, filter .18s ease, color .18s ease !important;
    }
    .stButton > button:hover { transform: translateY(-2px) scale(1.01); box-shadow: 0 12px 28px rgba(79,140,255,.5); filter: brightness(1.1); color:#FFFFFF !important; }
    .stButton > button:active { transform: translateY(0) scale(.98); filter: brightness(.9); box-shadow: 0 4px 14px rgba(79,140,255,.4); }
    .stButton > button:focus-visible { outline: 3px solid #9EC0FF; outline-offset: 2px; }
    .stButton > button:focus { color: #FFFFFF !important; border-color: #9EC0FF !important; }

    /* Download buttons */
    .stDownloadButton > button,
    .stDownloadButton > button[kind="primary"] {
        font-weight: 700 !important; color: #FFFFFF !important;
        background: linear-gradient(135deg, #7C5CFF, #5B3FD6) !important;
        border: 1px solid rgba(255,255,255,.3) !important; border-radius: 10px !important;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
    }
    .stDownloadButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(124,92,255,.5); filter: brightness(1.1); color:#FFFFFF !important; }
    .stDownloadButton > button:active { transform: translateY(0) scale(.98); filter: brightness(.9); }
    .stDownloadButton > button:focus-visible { outline: 3px solid #D8C9FF; outline-offset: 2px; }

    /* Link-style page buttons (st.page_link) */
    [data-testid="stPageLink"] a {
        display:inline-flex; align-items:center; justify-content:center;
        padding:.66rem 1.35rem; border-radius:10px; font-weight:700; font-size:.9rem;
        color:#FFFFFF !important; background:linear-gradient(135deg, #2B55C4, #3B6FE0) !important;
        border:1px solid rgba(255,255,255,.3) !important;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
    }
    [data-testid="stPageLink"] a:hover {
        transform: translateY(-2px); box-shadow:0 12px 28px rgba(79,140,255,.5);
        filter: brightness(1.1); color:#FFFFFF !important; border-color:#fff !important;
    }
    [data-testid="stPageLink"] a:active { transform: translateY(0) scale(.98); filter: brightness(.9); }
    [data-testid="stPageLink"] a:focus-visible { outline:3px solid #9EC0FF; outline-offset:2px; }

    /* ===== Cards (glassmorphism) ===== */
    .gc-card {
        background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px; padding: 1.3rem; margin-bottom: 1rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }
    .gc-card:hover { transform: translateY(-4px); box-shadow: 0 16px 44px rgba(0,0,0,0.5); border-color: rgba(79,140,255,.35); }
    .gc-card h3 { margin: 0 0 .25rem; font-size: 1.12rem; color: #F0F4FF; }
    .gc-card .gc-desc { color: #AEBBD4; font-size: .9rem; line-height: 1.5; min-height: 2.8rem; }
    .gc-card .gc-meta { color: #7E8CA8; font-size: .78rem; margin-top:.3rem; }

    /* Deployment status badge */
    .gc-dep-badge {
        display:inline-block; padding:.24rem .7rem; border-radius:999px;
        font-size:.72rem; font-weight:700; letter-spacing:.3px; margin: .2rem 0 .5rem;
    }
    .badge-green  { background: rgba(34,197,94,.16); color:#7EE2A8; border:1px solid rgba(34,197,94,.35); }
    .badge-blue   { background: rgba(79,140,255,.16); color:#9EC0FF; border:1px solid rgba(79,140,255,.35); }
    .badge-purple { background: rgba(168,85,247,.16); color:#D8B4FE; border:1px solid rgba(168,85,247,.35); }
    .badge-orange { background: rgba(249,115,22,.16); color:#FBC08A; border:1px solid rgba(249,115,22,.35); }
    .badge-gray   { background: rgba(148,163,184,.16); color:#C7D2E0; border:1px solid rgba(148,163,184,.3); }
    .badge-dark   { background: rgba(100,116,139,.15); color:#8A97AE; border:1px solid rgba(100,116,139,.3); }

    /* ===== Topic / Technology badges ===== */
    .gc-badge {
        display: inline-block; padding: .2rem .6rem; border-radius: 8px;
        font-size: .72rem; font-weight: 600; margin-right: .3rem; margin-bottom: .3rem;
        background: rgba(79,140,255,.12); color: #AEC6FF; border: 1px solid rgba(79,140,255,.2);
        transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease, background .15s ease;
    }
    .gc-badge:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(79,140,255,.25); border-color: rgba(79,140,255,.5); }
    .gc-badge.blue { background: rgba(79,140,255,.14); color:#AEC6FF; border-color:rgba(79,140,255,.25); }
    .gc-badge.green { background: rgba(34,197,94,.13); color:#8FE7B4; border-color:rgba(34,197,94,.25); }
    .gc-badge.green:hover { border-color: rgba(34,197,94,.5); box-shadow: 0 6px 16px rgba(34,197,94,.25); }
    .gc-badge.amber { background: rgba(245,158,11,.14); color:#FCD08A; border-color:rgba(245,158,11,.3); }

    /* ===== Section headings ===== */
    .gc-section-title { font-size: 1.7rem; font-weight: 800; color: #F0F4FF; margin: 1.6rem 0 .3rem; letter-spacing:-0.3px; }
    .gc-section-sub { color: #8FA0BC; margin-bottom: 1rem; font-size:.95rem; }

    /* ===== Note / info box ===== */
    .gc-note {
        background: rgba(79,140,255,.08); border-left: 4px solid #4F8CFF;
        padding: .8rem 1rem; border-radius: 0 10px 10px 0; font-size: .86rem;
        color: #C6D4EA; margin: 1rem 0;
    }
    .gc-note.amber { border-color: #F59E0B; background: rgba(245,158,11,.08); }

    /* ===== Timeline ===== */
    .gc-timeline-step { display:flex; gap:1rem; align-items:flex-start; margin-bottom:.2rem; }
    .gc-timeline-dot {
        width: 34px; height: 34px; border-radius:50%; flex-shrink:0;
        display:flex; align-items:center; justify-content:center;
        background: linear-gradient(135deg, #4F8CFF, #7C5CFF); color:#fff;
        font-weight:700; font-size:.85rem; box-shadow:0 0 0 4px rgba(79,140,255,.15);
    }
    .gc-timeline-line { width:2px; flex:0 0 2px; margin:0 auto; background:linear-gradient(#4F8CFF, rgba(79,140,255,.1)); }
    .gc-timeline-label { padding-top:.35rem; color:#E6EDF7; font-weight:600; }

    /* ===== Metric cards ===== */
    .gc-metric-card {
        padding: 1.1rem 1.2rem; border-radius: 14px; text-align:center;
        background: linear-gradient(160deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
        border:1px solid rgba(255,255,255,.09); box-shadow:0 8px 26px rgba(0,0,0,.3);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .gc-metric-card:hover { transform: translateY(-3px); box-shadow:0 14px 34px rgba(0,0,0,.45); }
    .gc-metric-value { font-size: 2rem; font-weight: 800; color:#E6F0FF; }
    .gc-metric-label { font-size: .8rem; color:#8FA0BC; margin-top:.2rem; letter-spacing:.3px; text-transform:uppercase; }

    /* ===== Evidence tags ===== */
    .gc-evidence.project { color:#8FE7B4; font-weight:600; }
    .gc-evidence.knowledge { color:#FCD08A; font-weight:600; }

    /* ===== Footer ===== */
    .gc-footer { text-align:center; color:#6B7A94; font-size:.8rem; padding:1.6rem 0; border-top:1px solid rgba(255,255,255,.06); margin-top:2rem; }
    .gc-footer a { color:#8FA0BC; text-decoration:none; }
    .gc-footer a:hover { color:#AEC6FF; }

/* ===== Domain navigation ===== */
    .gc-domain-nav-wrap { margin: .2rem 0 .4rem; }
    .gc-domain-nav-label {
        font-size:.78rem; letter-spacing:.4px; text-transform:uppercase;
        color:#7E8CA8; font-weight:700; margin-bottom:.1rem;
    }
    /* Horizontal domain radio (browse by domain) */
    .stRadio > div[role="radiogroup"] {
        flex-direction: row !important; flex-wrap: wrap !important; gap: .4rem !important;
    }
    .stRadio > div[role="radiogroup"] label {
        background: rgba(255,255,255,.05) !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        border-radius: 999px !important; padding: .35rem .95rem !important;
        color: #C6D4EA !important; font-weight: 600 !important; font-size:.85rem !important;
        transition: transform .18s ease, box-shadow .18s ease, background .18s ease,
                    border-color .18s ease !important;
        margin: 0 !important;
    }
    .stRadio > div[role="radiogroup"] label:hover {
        transform: translateY(-2px); border-color: rgba(79,140,255,.5);
        background: rgba(79,140,255,.12) !important;
    }
    .stRadio > div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg,#4F8CFF,#3B6FE0) !important;
        border-color: rgba(255,255,255,.25) !important; color:#fff !important;
        box-shadow: 0 6px 18px rgba(79,140,255,.4) !important;
    }
    .stRadio > div[role="radiogroup"] label > div:first-child {
        display: none !important;  /* hide the radio circle, keep pill look */
    }

    /* Static chips row (visual + query deep-links) */
    .gc-chips { display:flex; flex-wrap:wrap; gap:.4rem; margin:.4rem 0 .6rem; }
    .gc-chip {
        display:inline-flex; align-items:center; padding:.32rem .85rem; border-radius:999px;
        font-size:.8rem; font-weight:600; color:#C6D4EA; text-decoration:none;
        background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.12);
        transition: transform .18s ease, box-shadow .18s ease, background .18s ease,
                    border-color .18s ease, color .18s ease;
    }
    .gc-chip:hover { transform: translateY(-2px); border-color: rgba(79,140,255,.55); color:#fff; background: rgba(79,140,255,.12); }
    .gc-chip.active {
        background: linear-gradient(135deg,#4F8CFF,#3B6FE0); color:#fff;
        border-color: rgba(255,255,255,.25); box-shadow:0 6px 18px rgba(79,140,255,.4);
    }

    /* ===== Domain section headers ===== */
    .gc-domain-header {
        display:flex; align-items:center; gap:.9rem; margin: 1.6rem 0 .9rem;
        padding:.9rem 1.1rem; border-radius:14px;
        background: linear-gradient(120deg, rgba(79,140,255,.10), rgba(255,255,255,.015));
        border:1px solid rgba(79,140,255,.18);
        box-shadow:0 8px 26px rgba(0,0,0,.25);
    }
    .gc-domain-icon {
        font-size:1.6rem; width:48px; height:48px; flex-shrink:0; border-radius:12px;
        display:flex; align-items:center; justify-content:center;
        background: linear-gradient(135deg,#4F8CFF,#7C5CFF);
        box-shadow:0 6px 18px rgba(79,140,255,.35);
    }
    .gc-domain-title { font-size:1.35rem; font-weight:800; color:#F0F4FF; letter-spacing:-.3px; }
    .gc-domain-sub { font-size:.85rem; color:#8FA0BC; }
    .gc-domain-sub-title {
        font-size:1.05rem; font-weight:700; color:#C9DCFF; margin:1.1rem 0 .4rem;
        display:flex; align-items:center; gap:.5rem;
    }
    .gc-domain-sub-title::after {
        content:""; flex:1; height:1px; background:linear-gradient(90deg, rgba(79,140,255,.35), transparent);
    }

    /* Subcategory heading inside a primary domain (strict hierarchy) */
    .gc-subcategory-header {
        display:flex; align-items:center; gap:.5rem; margin:.9rem 0 .6rem;
        font-size:1.05rem; font-weight:700; color:#AEC6FF;
        letter-spacing:.2px; text-transform:uppercase;
    }
    .gc-subcategory-header::after {
        content:""; flex:1; height:1px;
        background:linear-gradient(90deg, rgba(79,140,255,.30), transparent);
    }
    .gc-subcategory-header small {
        font-weight:600; color:#7E8CA8; text-transform:none; font-size:.78rem;
    }

    /* ===== Animated counters (hero metrics) ===== */
    .gc-counter { display:inline-block; }
    @keyframes gcCount { from { opacity:0; transform:scale(.6);} to { opacity:1; transform:scale(1);} }
    .gc-counter span { animation: gcCount .7s ease both; display:inline-block; }

    /* ===== Responsive ===== */
    @media (max-width: 768px) {
        .gc-hero h1 { font-size: 2rem; }
        .gc-hero { padding: 2rem 1.2rem; }
        .gc-hero-badge { font-size:.68rem; }
        .gc-domain-header { padding:.7rem .8rem; }
        .gc-domain-title { font-size:1.1rem; }
    }

/* ===== Light-mode override ===== */
    [data-testid="stAppViewContainer"][data-theme="light"] {
        background: radial-gradient(1200px 600px at 80% -10%, rgba(79,140,255,.10), transparent 55%), #F4F7FF;
    }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-hero {
        background:
            radial-gradient(900px 360px at 12% -10%, rgba(79,140,255,.18), transparent 60%),
            linear-gradient(135deg, #F4F7FF 0%, #EAF0FF 100%);
        border-color: rgba(0,0,0,.06); box-shadow:0 16px 46px rgba(20,40,90,.12);
    }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-hero h1 { color:#0F1B33; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-hero .gc-title { color:#2B5FD9; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-hero p { color:#3E4C63; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-hero .gc-hero-badge { background:rgba(79,140,255,.12); color:#2B5FD9; border-color:rgba(43,95,217,.3); }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-card { background:#ffffff; border-color:#E3E9F5; box-shadow:0 6px 20px rgba(20,40,90,.08); }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-card:hover { box-shadow:0 14px 34px rgba(20,40,90,.14); border-color:#B9CFFA; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-card h3 { color:#0F1B33; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-card .gc-desc { color:#42526C; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-section-title { color:#0F1B33; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-section-sub { color:#66748C; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-metric-card { background:#ffffff; border-color:#E3E9F5; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-metric-value { color:#0F1B33; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-footer { color:#8A97AE; border-color:#E3E9F5; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-note { background:#EEF4FF; color:#2B3A55; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-btn-outline { color:#0F1B33; border-color:#C9D6EE; background:#fff; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-btn-outline:hover { background:#F0F5FF; border-color:#9EC0FF; }
    [data-testid="stAppViewContainer"][data-theme="light"] .gc-meta { color:#7A88A0; }
    [data-testid="stAppViewContainer"][data-theme="light"] p, [data-testid="stAppViewContainer"][data-theme="light"] li { color:#3E4C63; }
    [data-testid="stAppViewContainer"][data-theme="light"] a { color:#2B5FD9; }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero(
    name: str,
    title: str,
    summary: str,
    tags: list[str] | None = None,
) -> None:
    """Render the hero banner with a modern, premium layout."""
    tags_html = ""
    if tags:
        tags_html = '<div style="margin-top:.9rem;">' + "".join(
            f'<span class="gc-hero-badge">{t}</span>' for t in tags
        ) + "</div>"
    st.markdown(
        f"""
        <div class="gc-hero gc-anim">
            <h1>{name}</h1>
            <div class="gc-title">{title}</div>
            <p>{summary}</p>
            {tags_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    """Render a section header."""
    sub_html = f'<div class="gc-section-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="gc-section-title gc-anim-2">{title}</div>{sub_html}',
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


def deployment_badge(project: dict) -> None:
    """Render a visually obvious deployment status badge."""
    info = guess_deployment_status(project)
    st.markdown(
        f'<span class="gc-dep-badge {info["cls"]}">{info["label"]}</span>',
        unsafe_allow_html=True,
    )


def metric_card(value: str, label: str) -> None:
    """Render a styled metric value/label card."""
    st.markdown(
        f"""
        <div class="gc-metric-card gc-anim-2">
            <div class="gc-metric-value">{value}</div>
            <div class="gc-metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer(name: str, github: str, linkedin: str) -> None:
    """Render the footer. (Kept for backward compatibility.)"""
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
