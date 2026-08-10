"""Professional digital resume app for Streamlit.

This app reads structured data from the repository, renders a polished digital
resume, and generates a selectable-text PDF with ReportLab.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from typing import Any

import streamlit as st
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from utils.helpers import ROOT_DIR, load_projects, load_profile, load_skills


st.set_page_config(page_title="Gourav Chhatwani | Resume", page_icon="📄", layout="wide")

RESUME_DATA_PATH = ROOT_DIR / "data" / "resume.json"
CERTS_DATA_PATH = ROOT_DIR / "data" / "certifications.json"
PORTFOLIO_URL = "https://gcsportfolio.streamlit.app/"
GITHUB_URL = "https://github.com/GouravGC"
LINKEDIN_URL = "https://www.linkedin.com/in/gourav-chhatwani-9a301134a/"
EMAIL = "Chhatwanigourav@gmail.com"
PHONE = "7412841464"


def load_json_file(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return default or {}


def save_json_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def load_resume_overrides() -> dict[str, Any]:
    return load_json_file(RESUME_DATA_PATH, {})


def find_profile_image() -> Path | None:
    candidates = [
        ROOT_DIR / "assets" / "resume" / "Gourav_Chhatwani_Profile.jpg",
        ROOT_DIR / "assets" / "resume" / "Gourav_Chhatwani_Profile.jpeg",
        ROOT_DIR / "assets" / "resume" / "Gourav_Chhatwani_Profile.png",
        ROOT_DIR / "assets" / "resume" / "Gourav_Chhatwani_Profile.webp",
        ROOT_DIR / "Assets" / "Gourav_Chhatwani_Profile.jpg",
        ROOT_DIR / "Assets" / "Gourav_Chhatwani_Profile.jpeg",
        ROOT_DIR / "Assets" / "Gourav_Chhatwani_Profile.png",
        ROOT_DIR / "Assets" / "Gourav_Chhatwani_Profile.webp",
        ROOT_DIR / "Assets" / "Gemini_Generated_Image_qtttiqtttiqtttiq.png",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    for root_name in ("assets", "Assets"):
        root = ROOT_DIR / root_name
        if not root.exists():
            continue
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
            for candidate in root.rglob(ext):
                if "profile" in candidate.name.lower() or "gourav" in candidate.name.lower() or "gemini" in candidate.name.lower():
                    return candidate
    return None


def safe_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip() or default
    return str(value)


def normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def resolve_certificate_path(relative_path: Any) -> Path | None:
    if not relative_path:
        return None
    candidate = (ROOT_DIR / safe_text(relative_path)).resolve()
    if candidate.exists() and candidate.is_file():
        return candidate
    return None

def extract_skill_names(category: Any) -> list[str]:
    """Safely extract skill names from strings, dicts, lists, or malformed values."""
    if category is None:
        return []

    items: list[Any]
    if isinstance(category, dict):
        items = normalize_list(category.get("skills") or category.get("items") or category.get("values"))
        if not items and category.get("name"):
            items = [category]
    elif isinstance(category, list):
        items = category
    else:
        items = [category]

    names: list[str] = []
    for item in items:
        if isinstance(item, str):
            name = item.strip()
        elif isinstance(item, dict):
            name = safe_text(item.get("name") or item.get("skill") or item.get("title"))
        else:
            name = safe_text(item)
        if name:
            names.append(name)
    return names


def flatten_skill_groups(skills_data: dict[str, Any]) -> list[dict[str, Any]]:
    categories = skills_data.get("categories") or []
    normalized: list[dict[str, Any]] = []
    for category in categories:
        if not isinstance(category, dict):
            continue
        normalized.append(
            {
                "name": safe_text(category.get("name"), "Skills"),
                "icon": safe_text(category.get("icon")),
                "skills": extract_skill_names(category),
            }
        )
    return normalized


def load_resume_data() -> dict[str, Any]:
    profile = load_profile()
    overrides = load_resume_overrides()
    resume_data = {
        "name": overrides.get("name") or profile.get("name") or "Gourav Chhatwani",
        "title": overrides.get("title") or profile.get("professional_title") or "Data Scientist | AI/ML Engineer",
        "summary": overrides.get("summary") or profile.get("summary") or "",
        "email": overrides.get("email") or EMAIL,
        "phone": overrides.get("phone") or PHONE,
        "location": overrides.get("location") or "Jaipur, Rajasthan, India",
        "github": overrides.get("github") or GITHUB_URL,
        "linkedin": overrides.get("linkedin") or LINKEDIN_URL,
        "portfolio": overrides.get("portfolio") or PORTFOLIO_URL,
        "featured_project_ids": overrides.get("featured_project_ids") or [],
        "additional_project_ids": overrides.get("additional_project_ids") or [],
        "education": overrides.get("education") or [],
    }
    return resume_data


def build_project_lookup() -> dict[str, dict[str, Any]]:
    projects = load_projects()
    return {project.get("id", ""): project for project in projects if project.get("id")}


def select_projects(featured_ids: list[str], additional_ids: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lookup = build_project_lookup()
    featured = [lookup[project_id] for project_id in featured_ids if project_id in lookup]
    additional = [lookup[project_id] for project_id in additional_ids if project_id in lookup]
    return featured, additional


def render_css() -> None:
    st.markdown(
        """
        <style>
        :root { --bg: #0c1220; --panel: #121a2c; --panel2: #172139; --text: #e8edf7; --muted: #9aa7bd; --accent: #6ca9ff; }
        .stApp { background: linear-gradient(180deg, #0b1020 0%, #0e1424 100%); color: var(--text); }
        .resume-shell { border: 1px solid rgba(255,255,255,0.08); background: rgba(18,26,44,0.78); border-radius: 22px; padding: 24px; box-shadow: 0 24px 64px rgba(0,0,0,0.28); }
        .hero-grid { display: flex; gap: 22px; align-items: center; flex-wrap: wrap; }
        .photo-wrap { width: 160px; flex: 0 0 160px; }
        .photo-wrap img { width: 160px; height: 160px; object-fit: cover; border-radius: 28px; border: 1px solid rgba(255,255,255,0.14); box-shadow: 0 12px 40px rgba(0,0,0,0.35); }
        .name { margin: 0; font-size: 2.25rem; line-height: 1.05; color: var(--text); }
        .title { margin: 0.35rem 0 0; color: var(--accent); font-size: 1.03rem; font-weight: 600; }
        .subtle { color: var(--muted); }
        .pill-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }
        .pill { display: inline-flex; align-items: center; gap: 8px; padding: 9px 14px; border-radius: 999px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: var(--text); text-decoration: none; transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease; }
        .pill:hover { transform: translateY(-1px); background: rgba(108,169,255,0.12); border-color: rgba(108,169,255,0.35); }
        .section { margin-top: 22px; padding-top: 4px; }
        .section h2 { margin-bottom: 10px; font-size: 1.25rem; }
        .section-divider { height: 1px; background: linear-gradient(90deg, rgba(108,169,255,0.6), rgba(255,255,255,0.06)); margin: 16px 0 0; }
        .skill-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 14px 16px; height: 100%; }
        .skill-chip { display: inline-block; margin: 0 8px 8px 0; padding: 7px 11px; border-radius: 999px; background: rgba(108,169,255,0.12); border: 1px solid rgba(108,169,255,0.18); color: var(--text); font-size: 0.91rem; }
        .project-card, .cert-card, .edu-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 16px 18px; height: 100%; transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease; }
        .project-card:hover, .cert-card:hover, .edu-card:hover { transform: translateY(-2px); border-color: rgba(108,169,255,0.24); box-shadow: 0 18px 40px rgba(0,0,0,0.18); }
        .meta { color: var(--muted); font-size: 0.92rem; }
        .small-link { display: inline-block; margin-right: 10px; margin-top: 10px; color: var(--accent); text-decoration: none; }
        .small-link:hover { text-decoration: underline; }
        .muted-note { color: var(--muted); font-size: 0.92rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_photo(photo_path: Path | None) -> None:
    if not photo_path:
        st.warning("Profile photo not found in the repository. The resume will continue without it.")
        return
    with photo_path.open("rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("utf-8")
    suffix = photo_path.suffix.lower().lstrip(".") or "png"
    st.markdown(
        f"<div class='photo-wrap'><img src='data:image/{suffix};base64,{encoded}' alt='Gourav Chhatwani profile photo'></div>",
        unsafe_allow_html=True,
    )


def render_links(resume_data: dict[str, Any]) -> None:
    pills = [
        ("Email", f"mailto:{resume_data['email']}") if resume_data.get("email") else None,
        ("Phone", f"tel:{resume_data['phone']}") if resume_data.get("phone") else None,
        ("GitHub", resume_data.get("github")),
        ("LinkedIn", resume_data.get("linkedin")),
        ("Portfolio", resume_data.get("portfolio")),
    ]
    html = []
    for item in pills:
        if not item:
            continue
        label, href = item
        if href:
            html.append(f"<a class='pill' href='{href}' target='_blank' rel='noopener noreferrer'>{label}</a>")
    st.markdown("<div class='pill-row'>" + "".join(html) + "</div>", unsafe_allow_html=True)


def render_summary(summary: str) -> None:
    st.markdown(
        f"<div class='section'><h2>Professional Summary</h2><div class='subtle'>{summary}</div></div>",
        unsafe_allow_html=True,
    )


def render_skills(skills_data: dict[str, Any]) -> None:
    groups = flatten_skill_groups(skills_data)
    st.markdown("<div class='section'><h2>Technical Skills</h2></div>", unsafe_allow_html=True)
    if not groups:
        st.info("No skill groups found in the structured data.")
        return
    cols = st.columns(2)
    for idx, group in enumerate(groups):
        with cols[idx % 2]:
            chips = "".join(f"<span class='skill-chip'>{skill}</span>" for skill in group["skills"])
            st.markdown(
                f"<div class='skill-card'><div style='font-weight:700;margin-bottom:8px;'>{group['icon']} {group['name']}</div>{chips}</div>",
                unsafe_allow_html=True,
            )


def project_badges(project: dict[str, Any]) -> str:
    tech_parts: list[str] = []
    for key in ("languages", "frameworks", "libraries", "databases", "ml_algorithms", "deep_learning", "genai", "deployment"):
        values = normalize_list(project.get(key))
        if values:
            tech_parts.extend([safe_text(item) for item in values if safe_text(item)])
    ordered = []
    seen = set()
    for item in tech_parts:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ", ".join(ordered[:10])


def render_project_card(project: dict[str, Any]) -> None:
    metrics = project.get("metrics") or {}
    metric_line = ""
    if isinstance(metrics, dict) and metrics:
        metric_pairs = []
        for key, value in metrics.items():
            if value not in (None, ""):
                metric_pairs.append(f"{key}: {value}")
        metric_line = "; ".join(metric_pairs[:3])
    st.markdown(
        f"""
        <div class='project-card'>
          <div style='font-size:1.02rem;font-weight:700;margin-bottom:4px;'>{project.get('name','')}</div>
          <div class='meta'>{safe_text(project.get('short_description'))}</div>
          <div class='meta' style='margin-top:10px;'><strong>Technologies:</strong> {project_badges(project) or 'N/A'}</div>
          {f"<div class='meta' style='margin-top:6px;'><strong>Result:</strong> {metric_line}</div>" if metric_line else ''}
          <div style='margin-top:10px;'>
            {f"<a class='small-link' href='{project.get('live_demo_url')}' target='_blank' rel='noopener noreferrer'>Live Demo</a>" if project.get('live_demo_url') else ''}
            {f"<a class='small-link' href='{project.get('github_url')}' target='_blank' rel='noopener noreferrer'>GitHub</a>" if project.get('github_url') else ''}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_projects(featured: list[dict[str, Any]]) -> None:
    st.markdown("<div class='section'><h2>Featured Projects</h2></div>", unsafe_allow_html=True)
    if not featured:
        st.info("No featured projects were selected from the structured data.")
        return
    for start in range(0, len(featured), 2):
        cols = st.columns(2)
        for col_idx, project in enumerate(featured[start:start + 2]):
            with cols[col_idx]:
                render_project_card(project)


def render_certifications(certifications: list[dict[str, Any]]) -> None:
    st.markdown("<div class='section'><h2>Certifications</h2></div>", unsafe_allow_html=True)
    if not certifications:
        st.info("No verified certification entries were found in the repository.")
        return
    for idx, cert in enumerate(certifications):
        with st.container():
            st.markdown(
                f"""
                <div class='cert-card'>
                    <div style='font-weight:700;margin-bottom:4px;'>{safe_text(cert.get('name'))}</div>
                    <div class='meta'>{safe_text(cert.get('issuer'))}</div>
                    <div class='meta'>{safe_text(cert.get('date'))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            certificate_paths: list[Path] = []
            seen_paths: set[Path] = set()
            raw_files = cert.get("files") or cert.get("file_paths") or cert.get("file_path") or cert.get("file")
            for file_path in normalize_list(raw_files):
                resolved = resolve_certificate_path(file_path)
                if resolved and resolved not in seen_paths:
                    seen_paths.add(resolved)
                    certificate_paths.append(resolved)

            if not certificate_paths:
                st.warning(f"Certificate file unavailable: {safe_text(raw_files)}")
                continue

            for file_index, certificate_path in enumerate(certificate_paths):
                mime = "application/pdf"
                suffix = certificate_path.suffix.lower()
                if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                    mime = f"image/{suffix.lstrip('.')}"
                with certificate_path.open("rb") as handle:
                    certificate_bytes = handle.read()
                if len(certificate_paths) > 1:
                    st.caption(certificate_path.name)
                st.download_button(
                    label="View / Download Certificate",
                    data=certificate_bytes,
                    file_name=certificate_path.name,
                    mime=mime,
                    key=f"certificate-{idx}-{file_index}",
                    use_container_width=True,
                )


def render_education(education: list[dict[str, Any]]) -> None:
    st.markdown("<div class='section'><h2>Education</h2></div>", unsafe_allow_html=True)
    if not education:
        st.info("No education entries are available in the resume data file.")
        return
    for idx, item in enumerate(education):
        with st.container():
            st.markdown(
                f"""
                <div class='edu-card'>
                  <div style='font-weight:700;margin-bottom:4px;'>{safe_text(item.get('degree'))}</div>
                  <div class='meta'>{safe_text(item.get('institution'))}</div>
                  <div class='meta'>{safe_text(item.get('university') or '')}</div>
                  <div class='meta'>{safe_text(item.get('location'))} | {safe_text(item.get('year_start'))}-{safe_text(item.get('year_end') or item.get('passing_year'))}</div>
                  {f"<div class='meta' style='margin-top:4px;'>{safe_text(item.get('stream') or item.get('board') or '')}</div>" if item.get('stream') or item.get('board') else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_additional_projects(project_ids: list[str]) -> None:
    if not project_ids:
        return
    lookup = build_project_lookup()
    with st.expander("Additional Projects", expanded=False):
        for project_id in project_ids:
            project = lookup.get(project_id)
            if not project:
                continue
            st.markdown(f"**{safe_text(project.get('name'))}**")
            st.caption(safe_text(project.get("short_description")))
            line = project_badges(project)
            if line:
                st.markdown(f"<span class='meta'>{line}</span>", unsafe_allow_html=True)
            links = []
            if project.get("github_url"):
                links.append(f"<a class='small-link' href='{project['github_url']}' target='_blank' rel='noopener noreferrer'>GitHub</a>")
            if project.get("live_demo_url"):
                links.append(f"<a class='small-link' href='{project['live_demo_url']}' target='_blank' rel='noopener noreferrer'>Live Demo</a>")
            if links:
                st.markdown("".join(links), unsafe_allow_html=True)
            st.divider()


def build_pdf(resume_data: dict[str, Any], featured: list[dict[str, Any]], certifications: list[dict[str, Any]], skills_data: dict[str, Any], profile_image: Path | None) -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 0.62 * inch
    x = margin
    y = height - margin

    def page_break() -> None:
        nonlocal y
        pdf.showPage()
        y = height - margin

    def ensure_space(required: float) -> None:
        nonlocal y
        if y - required < margin:
            page_break()

    def draw_text(text: str, font: str = "Helvetica", size: int = 10.5, color: str = "000000", indent: float = 0) -> None:
        nonlocal y
        pdf.setFillColor(HexColor(f"#{color}"))
        pdf.setFont(font, size)
        pdf.drawString(x + indent, y, text)
        y -= size + 2.5

    def draw_wrapped(text: str, font: str = "Helvetica", size: int = 10.2, width_chars: int = 96, indent: float = 0) -> None:
        nonlocal y
        for line in wrap_text(text, width_chars):
            ensure_space(size + 4)
            draw_text(line, font=font, size=size, indent=indent)

    def link_line(label: str, url: str, font_size: int = 9.6) -> None:
        nonlocal y
        pdf.setFillColor(HexColor("#0a58ca"))
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(x, y, label)
        text_width = stringWidth(label, "Helvetica", font_size)
        pdf.linkURL(url, (x, y - 2, x + text_width, y + font_size + 2), relative=0)
        y -= font_size + 4

    def wrap_text(text: str, width_chars: int) -> list[str]:
        words = safe_text(text).split()
        if not words:
            return []
        lines: list[str] = []
        current: list[str] = []
        for word in words:
            candidate = " ".join(current + [word])
            if len(candidate) <= width_chars:
                current.append(word)
            else:
                lines.append(" ".join(current))
                current = [word]
        if current:
            lines.append(" ".join(current))
        return lines

    # header
    pdf.setTitle(f"{resume_data['name']} Resume")
    if profile_image and profile_image.exists():
        try:
            pdf.drawImage(ImageReader(str(profile_image)), x, y - 1.6 * inch, width=1.4 * inch, height=1.4 * inch, mask="auto")
        except Exception:
            pass

    text_x = x + (1.7 * inch if profile_image and profile_image.exists() else 0)
    pdf.setFillColor(HexColor("#111111"))
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(text_x, y - 4, resume_data["name"])
    pdf.setFont("Helvetica", 11.2)
    pdf.drawString(text_x, y - 22, resume_data["title"])
    y -= 52

    pdf.setFont("Helvetica", 9.4)
    pdf.setFillColor(HexColor("#1d1d1d"))
    contact_parts = [resume_data.get("location", ""), resume_data.get("email", ""), resume_data.get("phone", ""), resume_data.get("github", ""), resume_data.get("linkedin", ""), resume_data.get("portfolio", "")]
    pdf.drawString(x, y, " | ".join(part for part in contact_parts if part))
    y -= 15
    pdf.linkURL(f"mailto:{resume_data['email']}", (x, y + 5, x + 180, y + 18), relative=0)
    pdf.linkURL(f"tel:{resume_data['phone']}", (x + 185, y + 5, x + 290, y + 18), relative=0)
    y -= 8

    # summary
    pdf.setFont("Helvetica-Bold", 12.2)
    pdf.drawString(x, y, "Professional Summary")
    y -= 16
    for line in wrap_text(resume_data["summary"], 106):
        ensure_space(14)
        draw_text(line, size=9.6)

    # skills
    ensure_space(20)
    pdf.setFont("Helvetica-Bold", 12.2)
    pdf.drawString(x, y, "Technical Skills")
    y -= 16
    for group in flatten_skill_groups(skills_data):
        ensure_space(18)
        pdf.setFont("Helvetica-Bold", 10.1)
        pdf.drawString(x, y, f"{group['name']}")
        y -= 12
        skill_text = ", ".join(group["skills"])
        draw_wrapped(skill_text, size=9.2, width_chars=112, indent=10)

    # featured projects
    ensure_space(20)
    pdf.setFont("Helvetica-Bold", 12.2)
    pdf.drawString(x, y, "Featured Projects")
    y -= 16
    for project in featured:
        ensure_space(54)
        pdf.setFont("Helvetica-Bold", 10.6)
        pdf.drawString(x, y, safe_text(project.get("name")))
        y -= 12.5
        draw_wrapped(safe_text(project.get("short_description")), size=9.1, width_chars=108, indent=10)
        technologies = project_badges(project)
        if technologies:
            draw_wrapped(f"Technologies: {technologies}", size=8.9, width_chars=108, indent=10)
        metrics = project.get("metrics") or {}
        if isinstance(metrics, dict) and metrics:
            metric_line = "; ".join(f"{k}: {v}" for k, v in list(metrics.items())[:3])
            draw_wrapped(f"Result: {metric_line}", size=8.9, width_chars=108, indent=10)
        if project.get("live_demo_url"):
            link_line("Live Demo: " + safe_text(project.get("live_demo_url")), safe_text(project.get("live_demo_url")))
        if project.get("github_url"):
            link_line("GitHub: " + safe_text(project.get("github_url")), safe_text(project.get("github_url")))
        y -= 2

    # certifications
    ensure_space(20)
    pdf.setFont("Helvetica-Bold", 12.2)
    pdf.drawString(x, y, "Certifications")
    y -= 16
    for cert in certifications:
        ensure_space(24)
        pdf.setFont("Helvetica-Bold", 10.2)
        pdf.drawString(x, y, safe_text(cert.get("name")))
        y -= 11.5
        cert_line = safe_text(cert.get("issuer"))
        if cert.get("date"):
            cert_line = f"{cert_line} | {safe_text(cert.get('date'))}"
        draw_wrapped(cert_line, size=9.1, width_chars=108, indent=10)
        for file_path in normalize_list(cert.get("file_paths") or cert.get("file_path")):
            link_target = ROOT_DIR / safe_text(file_path)
            if link_target.exists():
                link_line(f"Certificate file: {link_target.name}", link_target.as_uri(), font_size=8.8)
        y -= 2

    # education
    ensure_space(20)
    pdf.setFont("Helvetica-Bold", 12.2)
    pdf.drawString(x, y, "Education")
    y -= 16
    for item in resume_data.get("education", []):
        ensure_space(36)
        pdf.setFont("Helvetica-Bold", 10.6)
        pdf.drawString(x, y, safe_text(item.get("degree")))
        y -= 12
        details = [safe_text(item.get("institution")), safe_text(item.get("university")), safe_text(item.get("location"))]
        details = [part for part in details if part]
        year_start = safe_text(item.get("year_start"))
        year_end = safe_text(item.get("year_end") or item.get("passing_year"))
        if year_start and year_end:
            details.append(f"{year_start}–{year_end}")
        elif year_end:
            details.append(year_end)
        draw_wrapped(" | ".join(details), size=9.2, width_chars=108, indent=10)
        extra = []
        if item.get("stream"):
            extra.append(safe_text(item.get("stream")))
        if item.get("board"):
            extra.append(safe_text(item.get("board")))
        if extra:
            draw_wrapped(" | ".join(extra), size=8.9, width_chars=108, indent=10)

    pdf.save()
    buffer.seek(0)
    return buffer.read()


def render_header(resume_data: dict[str, Any], photo_path: Path | None) -> None:
    st.markdown("<div class='resume-shell'>", unsafe_allow_html=True)
    cols = st.columns([1.05, 2.9])
    with cols[0]:
        render_photo(photo_path)
    with cols[1]:
        st.markdown(f"<h1 class='name'>{resume_data['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='title'>{resume_data['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtle' style='margin-top:8px;'>{resume_data['location']}</div>", unsafe_allow_html=True)
        render_links(resume_data)
        st.markdown(
            f"<div class='muted-note' style='margin-top:14px;'>View Portfolio: <a class='small-link' href='{PORTFOLIO_URL}' target='_blank' rel='noopener noreferrer'>{PORTFOLIO_URL}</a></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    render_css()
    resume_data = load_resume_data()
    skills_data = load_skills()
    certifications = load_json_file(CERTS_DATA_PATH, {}).get("certifications", [])
    profile_image = find_profile_image()
    featured_projects, additional_projects = select_projects(
        resume_data.get("featured_project_ids", []),
        resume_data.get("additional_project_ids", []),
    )

    render_header(resume_data, profile_image)
    render_summary(resume_data["summary"])
    render_skills(skills_data)
    render_projects(featured_projects)
    render_certifications(certifications)
    render_education(resume_data.get("education", []))

    if additional_projects:
        st.markdown("<div class='section'><h2>Additional Projects</h2></div>", unsafe_allow_html=True)
        render_additional_projects([project["id"] for project in additional_projects])

    st.markdown("<div class='section'><h2>Download</h2></div>", unsafe_allow_html=True)
    pdf_bytes = build_pdf(resume_data, featured_projects, certifications, skills_data, profile_image)
    st.download_button(
        label="Download Resume PDF",
        data=pdf_bytes,
        file_name="Gourav_Chhatwani_Digital_Resume.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
