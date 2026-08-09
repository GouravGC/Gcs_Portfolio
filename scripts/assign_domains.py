"""Assign a stable ``domains`` field to every project in projects.json.

This is a one-time data-adjuster that derives the multi-domain classification
from information ALREADY present in each project record (category, ml_algorithms,
deep_learning, genai, analytics, etc.). It never fabricates detail.

The ``domains`` field is the single source of truth used by the Projects page to
group projects into recruiter-friendly domain sections:

    Data Analytics
    Machine Learning  (Supervised Learning / Unsupervised Learning)
    Deep Learning     (Computer Vision / Time Series & Sequential)
    Generative AI
    Agentic AI
    Recommendation Systems

Run:
    python scripts/assign_domains.py
It is idempotent (safe to run repeatedly).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "projects.json"

# Ordered domain section list for the UI (order here = display order).
DOMAIN_ORDER = [
    "Data Analytics",
    "Machine Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Deep Learning",
    "Computer Vision",
    "Time Series",
    "Recommendation Systems",
    "Generative AI",
    "Agentic AI",
]


def _has_any(project: dict, *fields: str) -> bool:
    for f in fields:
        v = project.get(f)
        if isinstance(v, list) and v:
            return True
        if isinstance(v, str) and v:
            return True
    return False


def _cat(project: dict) -> list[str]:
    return [str(c).strip() for c in project.get("category", [])]


def derive_domains(project: dict) -> list[str]:
    """Return the list of domains a project belongs to (deduplicated, ordered)."""
    domains: set[str] = set()
    cats_l = [c.lower() for c in _cat(project)]
    dl = [str(x).lower() for x in project.get("deep_learning", [])]
    ml_algos = [str(x).lower() for x in project.get("ml_algorithms", [])]
    analytics = [str(x).lower() for x in project.get("analytics", [])]
    models = [str(x).lower() for x in (project.get("models") or [])]
    genai = [str(x).lower() for x in project.get("genai", [])]

    def in_cat(*needles: str) -> bool:
        return any(any(n in c for c in cats_l) for n in needles)

    # ---- Generative AI (precise: genai field non-empty OR literal "generative") ----
    if genai or "generative" in " ".join(cats_l) or in_cat("generative ai"):
        domains.add("Generative AI")

    # ---- Agentic AI (only ever true when real data says so) ----
    if any("agentic" in x for x in genai) or in_cat("agentic"):
        domains.add("Agentic AI")

    # ---- Recommendation Systems ----
    if in_cat("recommend") or any("recommend" in x for x in ml_algos):
        domains.add("Recommendation Systems")

    # ---- Time Series ----
    if in_cat("time series") or any("forecast" in x for x in analytics) or in_cat("forecast"):
        domains.add("Time Series")

    # ---- Deep Learning (and sub-domains) ----
    dl_keywords = ("neural network", "mlp", "cnn", "alexnet", "rnn", "vanilla rnn",
                   "residual mlp", "deep learning mlp", "lstm", "gru", "deep learning")
    if project.get("deep_learning") or any(m in dl_keywords for m in models):
        domains.add("Deep Learning")
        # Computer Vision
        if any(k in dl for k in ("cnn", "alexnet", "lenet", "minicnn")) or in_cat(
            "computer vision", "image classification"
        ):
            domains.add("Computer Vision")

    # ---- Machine Learning (only when real algorithms/models are present) ----
    if ml_algos or any(m and m not in ("llm-based chatbot", "deep learning mlp") for m in models):
        domains.add("Machine Learning")
        algo_names = " ".join(ml_algos + models)
        unsupervised_hint = any(
            k in algo_names
            for k in ("k-means", "kmeans", "dbscan", "gmm", "gaussian",
                      "agglomerative", "apriori", "fp-growth", "association",
                      "unsupervised")
        )
        unsupervised_cat = "unsupervised" in " ".join(cats_l)
        if unsupervised_hint or unsupervised_cat:
            domains.add("Unsupervised Learning")
        else:
            domains.add("Supervised Learning")

    # ---- Data Analytics ----
    if (
        project.get("analytics")
        or in_cat("data analytics", "business intelligence", "visualization", "sql")
    ):
        domains.add("Data Analytics")

    # Preserve a stable, UI-friendly ordering.
    ordered = [d for d in DOMAIN_ORDER if d in domains]
    # Anything else not in the known list is appended after.
    for d in domains:
        if d not in ordered:
            ordered.append(d)
    return ordered


def main() -> None:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = 0
    for p in data.get("projects", []):
        domains = derive_domains(p)
        if p.get("domains") != domains:
            p["domains"] = domains
            pid = p.get("id", "?")
            print(f"  {'set' if 'domains' in p else 'upd'} {pid}: {', '.join(domains)}")
            changed += 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nFinished. {changed} project(s) updated with a 'domains' field.")


if __name__ == "__main__":
    main()

