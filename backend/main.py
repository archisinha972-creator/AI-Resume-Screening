from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import time
import uuid

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

    safe_filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1].lower()}"

    file_path = os.path.join(
        "data/resumes",
        safe_filename
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

Machine Learning screening signal:

Prediction: {result}
ML model score: {probability * 100:.2f}%

Generate a concise recruiter-oriented assessment containing:

1. Candidate strengths
2. Areas for further assessment
3. Explanation of the ML screening signal
4. Suggested interview focus

Important:

- Refer to the numerical value only as an "ML model score"
  or "screening score".
- Do NOT describe it as a hiring probability.
- Do NOT claim that the score represents the probability
  that the candidate will be hired or succeed in a job.
- Explain the screening result only using the model's actual
  input features: Python, Pandas, NumPy, Machine Learning,
  experience, and projects.
- The model is a prototype trained on a very small synthetic
  dataset.
- Do not claim that the model represents real-world hiring
  decisions or industry hiring practices.
- Do not make a hiring decision.
- Do not use protected characteristics such as age, gender,
  religion, caste, or ethnicity.
- Base the assessment only on the provided candidate
  information and ML screening signal.
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
    safe_filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1].lower()}"

    file_path = os.path.join(
        "data/resumes",
        safe_filename
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

Projects detected:
{candidate_info["projects"]}

Machine Learning screening signal:

Prediction: {result}
ML model score: {probability * 100:.2f}%

Resume text:
{resume_text}

Generate a concise recruiter-oriented assessment with:

1. Candidate strengths
2. Technical skills identified
3. Areas for further assessment
4. Suggested interview focus
5. Explanation of the ML screening signal

Important:

- Refer to {probability * 100:.2f}% only as an
  "ML model score" or "screening score".
- Never call it a hiring probability.
- Do not interpret the score as the probability that
  the candidate will be hired or succeed in a job.
- Explain the ML screening result only using the six
  features used by the model:
  Python, Pandas, NumPy, Machine Learning,
  experience, and projects.
- The ML model is a prototype trained on a very small
  synthetic dataset.
- Do not claim that this model represents real-world
  hiring practices or industry hiring models.
- If experience or projects are missing, state that they
  were not detected in the provided resume. Do not assume
  that the candidate has no ability or potential.
- Do not make a hiring decision.
- Do not use protected characteristics such as age,
  gender, religion, caste, or ethnicity.
- Base the report only on the provided resume information
  and the ML screening signal.
"""

    # Generate Gemini report
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