import re

STOPWORDS = {
    "the","is","and","or","to","of","in","for","on","with","a","an",
    "our","other","we","are","you","your","will","be","as","by",
    "at","from","this","that","it","using","have","has"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def generate_summary(resume, jd):
    summary = []

    resume_words = set(clean_text(resume))
    jd_words = set(clean_text(jd))

    matched = jd_words & resume_words
    missing = jd_words - resume_words

    # Match %
    match_percent = int((len(matched) / (len(jd_words) + 1)) * 100)
    summary.append(f"Your resume matches approximately {match_percent}% of the job description.")

    # Strengths
    if matched:
        summary.append("Strong skills: " + ", ".join(list(matched)[:8]))

    # Missing Skills (CLEAN now ✅)
    if missing:
        summary.append("Missing important skills: " + ", ".join(list(missing)[:8]))

    # Quality Suggestions
    if len(resume) < 300:
        summary.append("Add more detailed experience and projects.")

    if "project" not in resume.lower():
        summary.append("Include project experience.")

    if "experience" not in resume.lower():
        summary.append("Add work experience or internships.")

    if "skill" not in resume.lower():
        summary.append("Add a skills section.")

    return summary