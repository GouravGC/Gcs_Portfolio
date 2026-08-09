"""Assign a strict hierarchical taxonomy to each project.

Every project receives EXACTLY ONE ``primary_domain``, a ``subcategory`` within
that domain, and optional ``secondary_tags`` (technology/methodology only, NOT
additional primary categories).

Rules enforced:
  * primary_domain is one of the PRIMARY_DOMAINS set.
  * A project is counted in exactly one primary domain.
  * subcategory is a valid child of the primary_domain.
  * secondary_tags are informational only and never contribute to domain counts.

Usage:
    python scripts/assign_taxonomy.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "projects.json"

# Primary domain -> ordered list of valid subcategories.
TAXONOMY = {
    "Data Analytics": [
        "Business Intelligence",
        "Analytics Projects",
    ],
    "Machine Learning": [
        "Supervised Learning",
        "Unsupervised Learning",
    ],
    "Deep Learning": [
        "Computer Vision",
        "NLP",
        "Sequential / Time-Series Deep Learning",
        "Deep Learning",
    ],
    "Generative AI": [
        "LLM Applications",
    ],
    "Agentic AI": [],
    "Recommendation Systems": [],
}

# project id -> (primary_domain, subcategory, secondary_tags)
ASSIGNMENTS = {
    "student-academic-outcome-prediction": (
        "Deep Learning",
        "Deep Learning",
        ["Neural Network", "MLP", "Classification", "SHAP", "MLOps"],
    ),
    "animal-10-classification": (
        "Deep Learning",
        "Computer Vision",
        ["CNN", "AlexNet", "Image Classification", "ONNX"],
    ),
    "human-activity-recognition": (
        "Deep Learning",
        "Deep Learning",
        ["Residual MLP", "Classification", "Sensor Data", "Time Series"],
    ),
    "fraud-detection": (
        "Machine Learning",
        "Supervised Learning",
        ["Classification", "XGBoost", "Imbalanced Data"],
    ),
    "customer-segmentation": (
        "Machine Learning",
        "Unsupervised Learning",
        ["Clustering", "K-Means", "RFM", "GMM", "DBSCAN"],
    ),
    "electricity-forecasting-rnn": (
        "Deep Learning",
        "Sequential / Time-Series Deep Learning",
        ["RNN", "Time Series", "Forecasting", "MLflow"],
    ),
    "market-basket-analysis": (
        "Machine Learning",
        "Unsupervised Learning",
        ["Association Rule Mining", "Apriori", "FP-Growth", "Recommendation System"],
    ),
    "loan-default-predictor": (
        "Machine Learning",
        "Supervised Learning",
        ["CatBoost", "Optuna", "Classification", "SHAP"],
    ),
    "insurance-cross-sell": (
        "Machine Learning",
        "Supervised Learning",
        ["XGBoost", "Classification", "NoSQL", "MongoDB"],
    ),
    "retail-data-warehouse-analytics": (
        "Data Analytics",
        "Analytics Projects",
        ["SQL", "Data Warehousing", "RFM", "Machine Learning", "SHAP"],
    ),
    "customer-churn-prediction": (
        "Machine Learning",
        "Supervised Learning",
        ["Classification", "XGBoost", "SQL"],
    ),
    "concrete-strength-predictor": (
        "Machine Learning",
        "Supervised Learning",
        ["Regression", "Flask", "Render"],
    ),
    "student-performance-predictor": (
        "Machine Learning",
        "Supervised Learning",
        ["Regression", "Flask", "Render"],
    ),
    "hospital-readmissions": (
        "Machine Learning",
        "Supervised Learning",
        ["XGBoost", "Classification", "Healthcare", "SHAP"],
    ),
    "hr-analytics-dashboard": (
        "Data Analytics",
        "Business Intelligence",
        ["Power BI", "SQL", "Dashboards", "Plotly"],
    ),
    "sales-bi-dashboard": (
        "Data Analytics",
        "Business Intelligence",
        ["Power BI", "SQL", "DuckDB", "Dashboards"],
    ),
    "retail-demand-forecasting": (
        "Deep Learning",
        "Deep Learning",
        ["MLP", "Regression", "Forecasting", "Time Series"],
    ),
    "basic-chatbot": (
        "Generative AI",
        "LLM Applications",
        ["LLM", "Chatbot", "Prompt Engineering"],
    ),
    "mini-chatgpt": (
        "Generative AI",
        "LLM Applications",
        ["LLM", "Chatbot", "Prompt Engineering"],
    ),
    "word-cloud-app": (
        "Data Analytics",
        "Analytics Projects",
        ["Text Visualization", "NLP", "Word Cloud"],
    ),
    "basic-stock-market-app": (
        "Data Analytics",
        "Analytics Projects",
        ["Financial Analytics", "Time Series", "yfinance"],
    ),
}


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    projects = data["projects"]

    seen_ids = set()
    for p in projects:
        pid = p["id"]
        if pid in seen_ids:
            raise SystemExit(f"Duplicate project id: {pid}")
        seen_ids.add(pid)

        if pid not in ASSIGNMENTS:
            raise SystemExit(f"No taxonomy assignment for project id: {pid}")
        primary, subcategory, tags = ASSIGNMENTS[pid]

        if primary not in TAXONOMY:
            raise SystemExit(f"Invalid primary_domain '{primary}' for {pid}")
        if subcategory not in TAXONOMY[primary]:
            raise SystemExit(f"Invalid subcategory '{subcategory}' for {pid} under {primary}")

        p["primary_domain"] = primary
        p["subcategory"] = subcategory
        p["secondary_tags"] = tags

    data["projects"] = projects
    DATA_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Assigned taxonomy to {len(projects)} projects.")

    # Sanity: sum of primary-domain counts must equal total unique projects.
    from collections import Counter

    counts = Counter(p["primary_domain"] for p in projects)
    print("Primary domain counts:", dict(counts))
    print("Total:", sum(counts.values()))


if __name__ == "__main__":
    main()
