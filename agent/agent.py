from google import genai
import joblib
import numpy as np
import pandas as pd

client = genai.Client()
model = joblib.load("ml/resume_model.pkl")

def find_candidate(name: str):
    """ Find candidate in the candidate database."""
    df = pd.read_csv("data/candidate.csv")

    candidate = df[df["name"].str.lower()==name.lower()]

    if candidate.empty:
        return {"error":"candidate not found"}

    return candidate.iloc[0].to_dict()

def predict_candidate(
        python_skill:int,
        pandas_skill:int,
        numpy_skill:int,
        ml_skill:int,
        experience:float,
        projects:int
):
    """ Predict candidate suitability using the trained ml model."""

    candidate = np.array([
    [python_skill, pandas_skill, numpy_skill, ml_skill, experience, projects]
    ])

    prediction = model.predict(candidate)[0]
    probability = model.predict_proba(candidate)[0][1]

    result = "Suitable" if prediction == 1 else "Not Suitable"
    return {
        "prediction":result,
        "probability": round(probability*100,2)
    }

# give the function to Gemini
tools = [find_candidate,
         predict_candidate]

chat = client.chats.create(
    model = "gemini-3.6-flash",
    config={
        "tools":tools
    }
)

print("AI Resume Screening Agent")
print("*************************")

response = chat.send_message(
    """
    Find the candidate named Aarav.

    Then use the prediction tool to evaluate the candidate.
    
    Generate a structured recuiter report containing:
    1. Candidate name
    2. Ml prediction
    3. Suitability probability
    4. Technical skills
    5. Experience
    6. Number of projects
    7. Candidate strengths
    8. Areas that may need further assesment
    9. Suggest interview fpocus

    Clearly state that the Ml result is an automated screening
    signal and should not replace human view.

    Do not use protected characteristics such as age, gender, religion, caste or ethnicity in the evaluation.
    """
)

print("--- RECRUITER REPORT ---")
print(response.text)