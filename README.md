# HireLens AI

## AI-Powered Resume Screening & Candidate Assistant

HireLens AI is an AI-assisted resume screening system that parses PDF/DOCX resumes, detects technical skills, generates an ML screening signal, and uses Google Gemini to create a recruiter-oriented candidate assessment.

> ⚠️ Portfolio prototype. The ML model is trained on a small synthetic dataset and its score is not a hiring probability or hiring decision.

---

## 🚀 Live Demo

🌐 Live App: https://hirelens-ai-orpin.vercel.app

🐙 GitHub: https://github.com/archisinha972-creator/AI-Resume-Screening

---

## ✨ Features

- 📄 PDF & DOCX resume upload
- 🔍 Resume text extraction
- 🧠 Technical skill detection
- 📊 ML-based screening signal
- 🤖 Gemini AI recruiter assessment
- ⚙️ UiPath candidate-screening automation
- 🌐 Deployed web application

---

## 🏗️ How It Works

Resume Upload
↓
FastAPI Backend
↓
Resume Parser
↓
ML Screening Model + Gemini AI
↓
Candidate Assessment

---

## 🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python, FastAPI

ML: Scikit-learn, Logistic Regression, Pandas, NumPy

AI: Google Gemini API

Automation: UiPath, Excel

Deployment: Vercel, Render

---

## 📂 Project Structure

AI-Resume-Screening/
├── agent/
├── backend/
├── data/
├── frontend/
├── ml/
├── notebooks/
├── uipath/
├── requirements.txt
├── render.yaml
└── README.md

---

## 💻 Run Locally

git clone https://github.com/archisinha972-creator/AI-Resume-Screening.git

cd AI-Resume-Screening

python -m venv venv

### Windows PowerShell

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

uvicorn backend.main:app --reload

Open: http://127.0.0.1:8000

---

## ⚠️ Limitations

- ML model uses a small synthetic dataset.
- Resume parsing depends on document structure and wording.
- The screening score is a prototype model output.
- Results should not be used as a standalone hiring decision.

---

## 🔮 Future Improvements

- Job description matching
- Semantic skill matching
- Improved resume parsing
- Larger datasets
- Recruiter dashboard
- Database integration

---

## 👩‍💻 Author

Archi Sinha

B.Tech — Computer Science Technology

KIIT University