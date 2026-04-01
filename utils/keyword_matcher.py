import re

STOPWORDS = {
    "the","is","and","or","to","of","in","for","on","with","a","an",
    "our","other","we","are","you","your","will","be","as","by",
    "at","from","this","that","it","using","have","has"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # remove punctuation
    words = text.split()
    return [w for w in words if w not in STOPWORDS]

def match_keywords(resume, jd):
    jd_words = set(clean_text(jd))
    resume_words = set(clean_text(resume))

    matched = list(jd_words & resume_words)
    missing = list(jd_words - resume_words)

    return {
        "matched": matched,
        "missing": missing
    }