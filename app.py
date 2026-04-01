import streamlit as st
import sys, os
import requests
import io
import sqlite3

sys.path.append(os.path.abspath("utils"))

from extract_text import extract_text
from preprocess import preprocess
from keyword_matcher import match_keywords
from ats_scoring import calculate_score
from summary_generator import generate_summary
from ai_chatbot import ask_ai

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ---------- DB INIT ----------
def init_db():
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            matched TEXT,
            missing TEXT,
            suggestions TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_result(score, matched, missing, suggestions):
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumes (score, matched, missing, suggestions)
        VALUES (?, ?, ?, ?)
    """, (
        int(score),
        str(matched),
        str(missing),
        str(suggestions)
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("resume_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


# ---------- INIT ----------
init_db()

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
h1 {text-align:center;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Resume Analyzer Pro")

# ---------- MODE ----------
mode = st.radio("Choose Mode", ["Local (Python)", "Backend (FastAPI)"])


# ---------- PDF ----------
def generate_pdf(score, matched, missing, suggestions):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("AI Resume Analysis Report", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"ATS Score: {score}%", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Matched Skills:", styles['Heading2']))
    content.append(Paragraph(", ".join(matched), styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Missing Skills:", styles['Heading2']))
    content.append(Paragraph(", ".join(missing), styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Suggestions:", styles['Heading2']))
    for s in suggestions:
        content.append(Paragraph(f"- {s}", styles['Normal']))

    doc.build(content)
    buffer.seek(0)
    return buffer


# ---------- SESSION ----------
if "processed" not in st.session_state:
    st.session_state.processed = ""
    st.session_state.jd = ""
    st.session_state.score = 0
    st.session_state.matches = {"matched": [], "missing": []}
    st.session_state.suggestions = []


# ---------- INPUT ----------
col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("📌 Job Description")

with col2:
    resume = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])


# ---------- ANALYZE ----------
if st.button("🔍 Analyze Resume"):

    if not resume or not jd:
        st.error("⚠️ Please upload resume and paste job description")

    else:
        try:

            # =========================
            # 🔵 LOCAL MODE
            # =========================
            if mode == "Local (Python)":

                text = extract_text(resume)
                processed = preprocess(text)

                matches = match_keywords(processed, jd)
                score = calculate_score(matches)
                suggestions = generate_summary(processed, jd)

                processed_text = processed


            # =========================
            # 🟢 BACKEND MODE
            # =========================
            else:

                files = {"file": resume}
                data = {"jd": jd}

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    files=files,
                    data=data
                )

                if response.status_code != 200:
                    st.error("❌ Backend Error")
                    st.write(response.text)
                    st.stop()

                result = response.json()

                score = result["score"]

                matches = {
                    "matched": result["matched"],
                    "missing": result["missing"]
                }

                suggestions = result["suggestions"]

                processed_text = extract_text(resume)


            # ---------- STORE SESSION ----------
            st.session_state.processed = processed_text
            st.session_state.jd = jd
            st.session_state.score = score
            st.session_state.matches = matches
            st.session_state.suggestions = suggestions

            # ---------- SAVE TO DATABASE ----------
            save_result(score, matches["matched"], matches["missing"], suggestions)

            st.success("✅ Analysis Completed & Saved!")

        except Exception as e:
            st.error(f"Error: {str(e)}")


# ---------- DISPLAY ----------
if st.session_state.processed:

    matched = st.session_state.matches.get("matched", [])
    missing = st.session_state.matches.get("missing", [])
    score = st.session_state.score

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 ATS Score", f"{score}%")

    with col2:
        st.metric("✅ Matched Skills", len(matched))

    with col3:
        st.metric("❌ Missing Skills", len(missing))

    st.progress(score / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        st.write(matched[:10])

    with col2:
        st.subheader("❌ Missing Skills")
        st.write(missing[:10])

    st.subheader("🧠 AI Suggestions")
    for s in st.session_state.suggestions:
        st.info(s)

    # ---------- CHATBOT ----------
    st.subheader("🤖 AI Resume Assistant")

    user_q = st.text_input("Ask about your resume")

    if user_q:
        response = ask_ai(
            st.session_state.processed,
            st.session_state.jd,
            user_q
        )
        st.success(response)

    # ---------- PDF ----------
    pdf = generate_pdf(
        score,
        matched,
        missing,
        st.session_state.suggestions
    )

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf,
        file_name="resume_report.pdf",
        mime="application/pdf"
    )


# ---------- HISTORY ----------
st.markdown("---")
st.subheader("📂 Resume History")

if st.button("Show Past Analyses"):
    data = get_history()

    for row in data:
        st.write("🆔 ID:", row[0])
        st.write("📊 Score:", row[1])
        st.write("✅ Matched:", row[2])
        st.write("❌ Missing:", row[3])
        st.write("🧠 Suggestions:", row[4])
        st.markdown("---")