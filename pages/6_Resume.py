"""Resume page — view and download the master resume.

The resume is generated from the same structured data (profile.json + projects.json)
via resume/generate_resume.py. This page lets the user view and download the PDF/DOCX.
"""
from __future__ import annotations

import streamlit as st

from components.footer import render_footer
from components.navbar import render_navbar
from components.ui import info_note, section_header
from utils.helpers import OUTPUT_DIR, load_profile

st.set_page_config(page_title="Resume | Gourav Chhatwani", page_icon="📄", layout="wide")
render_navbar()

profile = load_profile()
st.info(
    "This portfolio contains a dedicated digital resume app: run `streamlit run resume.py` in the project root to open the premium resume at a separate port (e.g. `--server.port 8502`).",
)
section_header(
    "Master Resume",
    "A professional, ATS-friendly resume generated from the same structured candidate data as this portfolio.",
)

st.markdown("### Download")
resume_names = [
    "Gourav_Chhatwani_Master_Resume.docx",
    "Gourav_Chhatwani_Master_Resume.pdf",
]

for fname in resume_names:
    fpath = OUTPUT_DIR / fname
    if fpath.exists():
        st.markdown(f"**{fname}**")
        with open(fpath, "rb") as f:
            data = f.read()
        mime = (
            "application/pdf"
            if fname.endswith(".pdf")
            else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.download_button(
            label=f"Download {fname}",
            data=data,
            file_name=fname,
            mime=mime,
        )

# In-app PDF preview (View Resume) if present
pdf_path = OUTPUT_DIR / "Gourav_Chhatwani_Master_Resume.pdf"
if pdf_path.exists():
    st.markdown("### Preview")
    st.markdown("📄 **View Resume** — full preview below.")
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="Open PDF",
        data=pdf_bytes,
        file_name=pdf_path.name,
        mime="application/pdf",
    )
    try:
        import base64

        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" '
            f'style="height:80vh; border:1px solid rgba(255,255,255,.1); border-radius:12px;"></iframe>',
            unsafe_allow_html=True,
        )
    except Exception:
        st.info("Inline PDF preview is unavailable in this environment. Use the Download buttons above.")

st.markdown("---")

st.markdown("### Generate / Regenerate the Resume")
st.code("python resume/generate_resume.py", language="bash")
info_note(
    "The DOCX is generated with python-docx from data/profile.json and data/projects.json. "
    "PDF generation occurs automatically when a reliable ODF/LibreOffice conversion is available. "
    "Personal details marked as placeholders should be filled in before finalizing.",
    tone="amber",
)

st.markdown("---")
st.markdown("### Resume Positioning")
st.markdown(
    "The resume is positioned for a **fresher** targeting Data Scientist, Data Analyst, "
    "ML Engineer, AI Engineer, and Generative AI Engineer roles. Wording emphasizes "
    "**Built / Developed / Implemented / Deployed**, and includes only the strongest projects "
    "that collectively demonstrate Data Analytics, Machine Learning, Deep Learning, Computer "
    "Vision, Time Series, Recommendation Systems, Generative AI, MLOps, and deployment."
)

render_footer()
