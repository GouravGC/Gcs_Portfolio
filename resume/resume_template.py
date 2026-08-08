"""Resume content assembly.

Builds the resume content (profile, skills, selected projects, education,
certifications, links) from the shared structured data layers. This is the single
source of truth for the resume so project descriptions are not duplicated.
"""
from __future__ import annotations

from utils.helpers import (
    is_placeholder,
    load_certifications,
    load_profile,
    load_projects,
    load_skills,
)

# Ordered list of category -> example project selection for the resume.
# We only include the strongest projects that collectively demonstrate breadth.
RESUME_PROJECT_IDS = [
    "student-academic-outcome-prediction",  # Deep Learning / MLOps / Explainable AI
    "animal-10-classification",             # Computer Vision / Deep Learning
    "human-activity-recognition",           # Deep Learning / Time Series
    "electricity-forecasting-rnn",          # Time Series / MLOps
    "fraud-detection",                      # Machine Learning / Imbalanced
    "customer-segmentation",                # Unsupervised Learning
    "market-basket-analysis",               # Recommendation Systems
    "loan-default-predictor",               # ML / Explainable AI / Deployment
    "insurance-cross-sell",                 # ML / NoSQL / Deployment
    "retail-data-warehouse-analytics",      # Data Analytics / SQL / ML
    "customer-churn-prediction",            # ML / SQL / Deployment
    "concrete-strength-predictor",          # Regression / Flask / Deployment
    "student-performance-predictor",        # Regression / Flask / Deployment
    "hospital-readmissions",                # ML / Healthcare
]


def _clean(value: str) -> str:
    """Replace placeholder markers with a cleaner placeholder label."""
    value = str(value)
    if is_placeholder(value):
        return "[Add your details]"
    return value


def get_selected_projects() -> list[dict]:
    """Return the projects selected for the resume, in priority order."""
    all_projects = {p["id"]: p for p in load_projects()}
    selected = []
    for pid in RESUME_PROJECT_IDS:
        if pid in all_projects:
            selected.append(all_projects[pid])
    return selected


def build_resume_content() -> dict:
    """Assemble all resume sections from the data layer."""
    profile = load_profile()
    projects = get_selected_projects()
    skills_data = load_skills()
    certs_data = load_certifications()

    # Technical skills: flatten categories into a readable list.
    skill_lines: list[str] = []
    for category in skills_data.get("categories", []):
        names = [s["name"] for s in category.get("skills", [])]
        if names:
            skill_lines.append(f"{category['name']}: {', '.join(names)}")

    # Project bullets: ACTION + TECHNIQUE + PROBLEM + RESULT (metrics if verified).
    project_entries = []
    for p in projects:
        bullets = _project_bullets(p)
        project_entries.append({"name": p.get("name", ""), "bullets": bullets})

    return {
        "name": profile.get("name", "Gourav Chhatwani"),
        "title": profile.get("professional_title", "Data Scientist | AI/ML Engineer"),
        "summary": profile.get("summary", ""),
        "email": _clean(profile.get("email", "[ADD_EMAIL_PLACEHOLDER]")),
        "phone": _clean(profile.get("phone", "[ADD_PHONE_PLACEHOLDER]")),
        "location": _clean(profile.get("location", "[ADD_LOCATION_PLACEHOLDER]")),
        "github": profile.get("github", "https://github.com/GouravGC"),
        "linkedin": profile.get("linkedin", "https://www.linkedin.com/in/gourav-chhatwani-9a301134a/"),
        "education": profile.get("education", []),
        "certifications": certs_data.get("certifications", []),
        "skill_lines": skill_lines,
        "project_entries": project_entries,
    }


def _project_bullets(project: dict) -> list[str]:
    """Generate resume bullets for a single project."""
    bullets: list[str] = []
    desc = project.get("short_description", "")
    if desc:
        bullets.append(desc)

    # Technique line
    tech_parts = []
    if project.get("frameworks"):
        tech_parts.append(", ".join(project["frameworks"][:3]))
    models = project.get("models") or project.get("ml_algorithms") or []
    if models:
        tech_parts.append(", ".join(models[:3]))
    libs = project.get("libraries", [])
    if libs:
        tech_parts.append(", ".join(libs[:4]))
    if tech_parts:
        bullets.append("Techniques & tools: " + " | ".join(tech_parts))

    # Metric line if verified
    metrics = project.get("metrics", {})
    if metrics:
        metric_str = ", ".join(f"{k}: {v}" for k, v in list(metrics.items())[:3])
        bullets.append("Key results: " + metric_str)

    # Deployment line
    if project.get("deployment_platform"):
        bullets.append(f"Deployed via {project['deployment_platform']}.")

    return bullets
