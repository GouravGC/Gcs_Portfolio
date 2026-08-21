# Gourav Chhatwani — Data Science & AI Portfolio

A production-quality, **data-driven Streamlit portfolio and master resume system**
for **Gourav Chhatwani**, a fresher targeting **Data Scientist, Data Analyst,
Machine Learning Engineer, AI Engineer, and Generative AI Engineer** roles.

The entire portfolio is driven by structured JSON data, so adding or updating a
project automatically propagates to the project explorer, category filters,
project detail pages, skill associations, and resume selection logic — without
rewriting any UI code.

> **Source of truth:** All project information, links, and metrics come from the
> candidate's public [GitHub profile](https://github.com/GouravGC). Nothing is
> fabricated. Unknown personal details are kept as clearly marked placeholders.

---

# 🚀 Live Demo

The application is deployed using Streamlit Cloud:

🔗 **Customer Churn Prediction App:**  
https://gcsportfolio.streamlit.app/ (Live Demo Note: The Streamlit Community Cloud app may be asleep due to inactivity. If prompted, click “Yes, get this app back up!” and wait a few seconds for the app to load.)

---

## ✨ Features

- **Hero / Home** — professional intro, positioning, and quick links.
- **About** — the candidate's learning & project-development journey as an elegant timeline.
- **Project Explorer** — searchable, filterable project cards (category, technology, deployment).
- **Project Detail pages** — deep-dive per project (problem, dataset, models, metrics, deployment, etc.).
- **Skills** — interactive, evidence-tagged skills browser.
- **Deployment Showcase** — verified deployment architectures and platforms.
- **Resume** — download the generated master resume (DOCX + optional PDF).
- **Master Resume Generator** — builds an ATS-friendly resume from the same data layer.
- **GitHub metadata updater** — refresh project metadata offline (no per-page API calls).
- **Validation script** — QC checks for JSON, links, imports, and resume assembly.

---

## 🧱 Architecture

```
.
├── app.py                      # Main entry / Hero page
├── pages/
│   ├── 1_About.py
│   ├── 2_Projects.py           # Project explorer (search + filters)
│   ├── 3_Project_Detail.py
│   ├── 4_Skills.py
│   ├── 5_Deployment.py
│   └── 6_Resume.py
├── components/                 # Reusable UI components
│   ├── ui.py                   # Theme / CSS
│   ├── navbar.py
│   ├── footer.py
│   ├── project_card.py
│   ├── skill_card.py
│   ├── metrics.py
│   ├── timeline.py
│   └── detail_sections.py
├── data/                       # Structured data layer (source of truth)
│   ├── profile.json
│   ├── projects.json
│   ├── skills.json
│   └── certifications.json
├── utils/                      # Helpers, validation, GitHub updater
│   ├── helpers.py
│   ├── validation.py
│   └── github.py
├── resume/
│   ├── resume_template.py      # Resume content assembly (from data layer)
│   ├── generate_resume.py      # DOCX (+ optional PDF) generator
│   └── output/                 # Generated resumes
├── scripts/
│   ├── update_github_data.py   # Refresh GitHub metadata
│   └── validate.py             # QC / validation
├── assets/
├── requirements.txt
├── .env.example
└── README.md
```

**Data flow:** `data/*.json` → `utils/helpers.py` → `components/*` + `pages/*` → render.
The resume generator reads the same JSON files, so project descriptions are never duplicated.

---

## 🛠 Tech Stack

| Area | Technology |
|------|------------|
| Presentation | Streamlit, custom CSS |
| Data layer | JSON (structured) |
| Resume | python-docx (DOCX), LibreOffice (optional PDF) |
| GitHub metadata | GitHub REST API (`requests`) |

> **Deliberately lightweight.** The portfolio does **not** install or import heavy
> ML/DL/GenAI frameworks. It is a navigation/presentation layer; the real projects
> run in their own repositories and are accessed via verified GitHub + Live Demo links.

---

## 🚀 Local Setup

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd <portfolio-folder>
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The portfolio opens at `http://localhost:8501`.

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in values. The app works without any
environment variables; the optional `GITHUB_TOKEN` only raises the GitHub API
rate limit for the metadata refresh script.

```bash
cp .env.example .env
```

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) → **New app**.
3. Select the repository, branch `main`, and set **Main file** to `app.py`.
4. Click **Deploy**.

No secrets are required for the public portfolio.

---

## 🔄 Updating GitHub Project Data

The portfolio does **not** call the GitHub API at every page load. To refresh
repository metadata (languages, stars, updated dates) from GitHub:

```bash
# Optional: set a token to avoid rate limits
export GITHUB_TOKEN=ghp_xxx      # Windows: set GITHUB_TOKEN=ghp_xxx

python scripts/update_github_data.py
```

This merges safe metadata fields back into `data/projects.json`. Curated
descriptions and live demo URLs are left untouched.

---

## 📄 Resume Generation

Generate the master resume (DOCX, and PDF if LibreOffice is installed):

```bash
python resume/generate_resume.py
```

Outputs land in `resume/output/`:

- `Gourav_Chhatwani_Master_Resume.docx`
- `Gourav_Chhatwani_Master_Resume.pdf` (optional)

The resume is assembled from `data/profile.json` and `data/projects.json` (only
the strongest projects are selected). Personal details currently marked as
placeholders should be filled in before finalizing.

---

## ✅ Validation / QC

Run the validation script to check JSON validity, unique project ids, URL
syntax, placeholders, resume assembly, and module imports:

```bash
python scripts/validate.py
```

---

## 📁 Adding a New Project

1. Add a new object to `data/projects.json` (follow the existing schema).
2. The project automatically appears in:
   - Project explorer
   - Category filters
   - Project detail pages
   - Skill associations
   - Resume selection logic (if its id is listed in `RESUME_PROJECT_IDS`)

No UI code changes are required.

---

## 🧭 Project Categories Covered

Data Analytics · Business Intelligence · SQL · Machine Learning · Supervised
Learning · Unsupervised Learning · Deep Learning · Computer Vision · Time Series ·
Recommendation Systems · Generative AI · MLOps · Deployment · End-to-End AI Applications

---

## 👤 Candidate

**Gourav Chhatwani** — Aspiring Data Scientist & AI Engineer

- [GitHub](https://github.com/GouravGC)
- [LinkedIn](https://www.linkedin.com/in/gourav-chhatwani-9a301134a/)

---

## 📄 License

This portfolio project is for educational and portfolio purposes. All project
data is sourced from the candidate's public GitHub repositories.
