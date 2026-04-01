def ask_ai(resume, jd, question):

    question = question.lower()

    if "improve" in question:
        return "Add measurable achievements, strong action verbs, and more projects."

    elif "skills" in question:
        return "Focus on adding SQL, Python, Excel, Power BI, and communication skills."

    elif "score" in question:
        return "Improve your ATS score by adding missing keywords from the job description."

    elif "project" in question:
        return "Include 2-3 strong projects with clear outcomes and technologies used."

    else:
        return "Try asking about improving resume, skills, or ATS score."