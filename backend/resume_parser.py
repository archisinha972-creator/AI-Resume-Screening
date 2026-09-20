from pypdf import PdfReader
from docx import Document
import re

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    text =""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def extract_text_from_docx(file_path):
    document = Document(file_path)

    text =""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_resume_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Only Pdf and Docx files are supported.")

def extract_candidate_info(text):

    text_lower = text.lower()

    skills = {
        "python": "python" in text_lower,
        "pandas": "pandas" in text_lower,
        "numpy": "numpy" in text_lower,
        "machine_learning": (
            "machine learning" in text_lower
            or "machine-learning" in text_lower
        ),
        "scikit_learn": (
            "scikit-learn" in text_lower
            or "sklearn" in text_lower
        ),
        "java": "java" in text_lower,
        "html": "html" in text_lower,
        
        "uipath": ("uipath" in text_lower or "ui path" in text_lower),
        "agentic_ai": "agentic ai" in text_lower
    }

    # Basic experience detection
    experience = 0

    if "internship" in text_lower:
        experience = 1

    if "work experience" in text_lower:
        experience = 1

    # Basic project detection
    projects = 0

    project_heading_pattern = r"(?m)^\s*(projects|academic projects|personal projects|project experience|projects experience)\s*$"

    if re.search(project_heading_pattern, text_lower):
        projects = 1

    return {
        "skills": skills,
        "experience":experience,
        "projects":projects,
        "text_length": len(text)
    }