import pdfplumber
import docx


def extract_text(file):
    filename = file.filename.lower()

    # PDF
    if filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # DOCX
    elif filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])

    return ""