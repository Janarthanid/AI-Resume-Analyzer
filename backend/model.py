def analyze_resume(resume_text, jd):

    resume_words = set(resume_text.lower().split())
    jd_words = set(jd.lower().split())

    matched = list(resume_words.intersection(jd_words))
    missing = list(jd_words - resume_words)

    score = int((len(matched) / len(jd_words)) * 100) if jd_words else 0

    suggestions = []

    if "docker" in missing:
        suggestions.append("Add Docker experience")

    if "fastapi" in missing:
        suggestions.append("Learn FastAPI for backend roles")

    if score < 50:
        suggestions.append("Improve technical keywords in resume")

    return {
        "score": score,
        "matched": matched[:10],
        "missing": missing[:10],
        "suggestions": suggestions
    }