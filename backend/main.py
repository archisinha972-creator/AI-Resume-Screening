from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import time

from backend.resume_parser import (
    extract_resume_text,
    extract_candidate_info
)

app = FastAPI(title="AI Resume Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = joblib.load("ml/resume_model.pkl")

# Gemini client
client = genai.Client()


# --------------------------------------------------
# Gemini helper with retry handling
# --------------------------------------------------

def generate_ai_report(prompt):

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"Gemini API attempt {attempt + 1} failed:")
            print(e)

            if attempt < 2:
                time.sleep(3)

    return """
### AI Recruiter Assessment

Gemini is temporarily unavailable.

The resume was successfully processed by the local
resume parser and machine learning screening model.

Please retry the analysis to generate the AI recruiter
assessment.

The ML screening result is only a prototype screening
signal and should not be treated as a hiring decision.
"""


# --------------------------------------------------
# Candidate input model
# --------------------------------------------------

class Candidate(BaseModel):
    python: int
    pandas: int
    numpy: int
    machine_learning: int
    experience: float
    projects: int


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Resume Screening API is running"
    }


# --------------------------------------------------
# Upload Resume
# --------------------------------------------------

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".pdf", ".docx")):

        return {
            "error": "Only PDF and DOCX files are supported."
        }

    os.makedirs("data/resumes", exist_ok=True)

    file_path = os.path.join(
        "data/resumes",
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    resume_text = extract_resume_text(file_path)

    candidate_info = extract_candidate_info(resume_text)

    return {
        "filename": file.filename,
        "resume_text": resume_text,
        "candidate_info": candidate_info
    }


# --------------------------------------------------
# ML Prediction
# --------------------------------------------------

@app.post("/predict")
def predict(candidate: Candidate):

    data = np.array([
        [
            candidate.python,
            candidate.pandas,
            candidate.numpy,
            candidate.machine_learning,
            candidate.experience,
            candidate.projects
        ]
    ])

    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0][1]

    result = "Suitable" if prediction == 1 else "Not Suitable"

    return {
        "prediction": result,
        "probability": round(float(probability * 100), 2)
    }


# --------------------------------------------------
# AI Screening using Candidate Data
# --------------------------------------------------

@app.post("/screen")
def screen_candidate(candidate: Candidate):

    data = np.array([
        [
            candidate.python,
            candidate.pandas,
            candidate.numpy,
            candidate.machine_learning,
            candidate.experience,
            candidate.projects
        ]
    ])

    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0][1]

    result = "Suitable" if prediction == 1 else "Not Suitable"

    prompt = f"""
You are an AI resume screening assistant.

Candidate information:

Python: {candidate.python}
Pandas: {candidate.pandas}
NumPy: {candidate.numpy}
Machine Learning: {candidate.machine_learning}
Experience: {candidate.experience} years
Projects: {candidate.projects}

Machine Learning Result:

Prediction: {result}
Probability: {probability * 100:.2f}%

Generate a concise recruiter report containing:

1. Candidate strengths
2. Areas for further assessment
3. Explanation of the ML result
4. Suggested interview focus

The ML result is an automated screening signal and should
not replace human review.

Do not use protected characteristics such as age, gender,
religion, caste, or ethnicity.
"""

    ai_report = generate_ai_report(prompt)

    return {
        "prediction": result,
        "probability": round(float(probability * 100), 2),
        "ai_report": ai_report
    }


# --------------------------------------------------
# Full Resume Screening
# --------------------------------------------------

@app.post("/screen-resume")
async def screen_resume(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.lower().endswith((".pdf", ".docx")):

        return {
            "error": "Only PDF and DOCX files are supported."
        }

    # Create resume directory
    os.makedirs("data/resumes", exist_ok=True)

    # Save uploaded resume
    file_path = os.path.join(
        "data/resumes",
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract resume text
    resume_text = extract_resume_text(file_path)

    # Extract candidate information
    candidate_info = extract_candidate_info(resume_text)

    skills = candidate_info["skills"]

    # Prepare ML input
    data = np.array([
        [
            int(skills["python"]),
            int(skills["pandas"]),
            int(skills["numpy"]),
            int(skills["machine_learning"]),
            candidate_info["experience"],
            candidate_info["projects"]
        ]
    ])

    # ML prediction
    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0][1]

    result = "Suitable" if prediction == 1 else "Not Suitable"

    # Gemini prompt
    prompt = f"""
You are an AI recruiter assistant.

Analyze the following candidate resume information.

Candidate skills:
{candidate_info["skills"]}

Experience:
{candidate_info["experience"]} years

Projects:
{candidate_info["projects"]}

Machine Learning screening result:

Prediction: {result}
Probability: {probability * 100:.2f}%

Resume text:
{resume_text}

Generate a concise recruiter report with:

1. Candidate strengths
2. Technical skills identified
3. Areas for further assessment
4. Suggested interview focus
5. Explanation of the ML screening result

Important:

- Treat the ML result only as an automated screening signal.
- Do not make a hiring decision.
- Do not use protected characteristics such as age,
  gender, religion, caste, or ethnicity.
- Base the report only on the provided resume information.
"""

    # Generate Gemini report with retry handling
    ai_report = generate_ai_report(prompt)

    # Return complete result
    return {
        "filename": file.filename,
        "candidate_info": candidate_info,
        "prediction": result,
        "probability": round(float(probability * 100), 2),
        "ai_report": ai_report,
        "resume_text": resume_text
    }