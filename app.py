import streamlit as st
from utils.extract_text import extract_pdf, extract_docx
from utils.preprocess import clean_text
from utils.keyword_matcher import compute_similarity
from utils.ats_scoring import ats_score
from utils.summary_generator import rewrite_summary

st.title("AI Resume Analyzer + ATS Predictor")

jd_text = st.text_area("Paste Job Description Here")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Analyze Resume"):
    if resume_file and jd_text:
        # Extract text
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_pdf(resume_file)
        else:
            resume_text = extract_docx(resume_file)

        # Preprocess
        jd_clean = clean_text(jd_text)
        resume_clean = clean_text(resume_text)

        # Similarity Score
        similarity = compute_similarity(jd_clean, resume_clean)
        match_percent = round(similarity * 100, 2)

        # ATS Score
        ats = ats_score(match_percent, 100)

        # Dummy Skills
        skills = ["Python", "Machine Learning", "NLP"]

        # Summary
        summary = rewrite_summary(skills)

        st.subheader("📊 Results")
        st.write("**Resume Match %:**", match_percent)
        st.write("**ATS Score:**", ats)
        st.write("**Rewritten Professional Summary:**")
        st.success(summary)
