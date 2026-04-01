import streamlit as st
import sys, os
sys.path.append(os.path.abspath("utils"))

from extract_text import extract_text
from preprocess import preprocess
from keyword_matcher import match_keywords
from ats_scoring import calculate_score
from summary_generator import generate_summary
from ai_chatbot import ask_ai

# ✅ PDF imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

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

# ---------- PDF FUNCTION ----------
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

# ---------- SESSION STORAGE ----------
if "processed" not in st.session_state:
    st.session_state.processed = ""
    st.session_state.jd = ""
    st.session_state.score = 0
    st.session_state.matches = {}
    st.session_state.suggestions = []

# ---------- INPUT ----------
col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("📌 Job Description")

with col2:
    resume = st.file_uploader("📄 Upload Resume", type=["pdf","docx"])

# ---------- ANALYZE ----------
if st.button("🔍 Analyze Resume"):

    if not resume or not jd:
        st.error("⚠️ Please upload resume and paste job description")
    else:
        text = extract_text(resume)
        processed = preprocess(text)

        matches = match_keywords(processed, jd)
        score = calculate_score(matches)
        suggestions = generate_summary(processed, jd)

        # Store in session
        st.session_state.processed = processed
        st.session_state.jd = jd
        st.session_state.score = score
        st.session_state.matches = matches
        st.session_state.suggestions = suggestions

        st.success("✅ Analysis Completed!")

# ---------- DISPLAY RESULTS ----------
if st.session_state.processed:

    matched = st.session_state.matches.get("matched", [])
    missing = st.session_state.matches.get("missing", [])
    score = st.session_state.score

    # Dashboard
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 ATS Score", f"{score}%")

    with col2:
        st.metric("✅ Matched Skills", len(matched))

    with col3:
        st.metric("❌ Missing Skills", len(missing))

    st.progress(score/100)

    # Skills
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        st.write(matched[:10])

    with col2:
        st.subheader("❌ Missing Skills")
        st.write(missing[:10])

    # Suggestions
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

    # ---------- PDF DOWNLOAD ----------
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