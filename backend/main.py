from fastapi import FastAPI, UploadFile, File, Form
from utils import extract_text
from model import analyze_resume

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Resume Analyzer Backend Running"}


@app.post("/analyze")
def analyze(file: UploadFile = File(...), jd: str = Form(...)):

    # 1. Extract text
    resume_text = extract_text(file)

    # 2. Analyze resume
    result = analyze_resume(resume_text, jd)

    # 3. Return JSON to frontend
    return result