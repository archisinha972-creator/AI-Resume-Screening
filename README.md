# HireLens AI

## AI-Powered Resume Screening & Candidate Assistant

HireLens AI is an AI-assisted resume screening system that parses PDF/DOCX resumes, detects technical skills, generates an ML screening signal, and uses Google Gemini to create a recruiter-oriented candidate assessment.

> ⚠️ **Portfolio Prototype:** The ML model is trained on a small synthetic dataset. Its score is a model output and should not be interpreted as a hiring probability or hiring decision.

---

## Demo

- **Live App:** [https://hirelens-ai-orpin.vercel.app](https://hirelens-ai-orpin.vercel.app)
- **GitHub:** [https://github.com/archisinha972-creator/AI-Resume-Screening](https://github.com/archisinha972-creator/AI-Resume-Screening)

---

## Features

- PDF & DOCX resume upload
- Resume text extraction
- Technical skill detection
- ML-based screening signal
- Gemini AI recruiter assessment
- UiPath candidate-screening automation
- Deployed web application

---

## How It Works

```text
Resume Upload
      ↓
FastAPI Backend
      ↓
Resume Parser
      ↓
ML Model + Gemini AI
      ↓
Candidate Assessment
```

---

## Tech Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn, Logistic Regression, Pandas, NumPy |
| Generative AI | Google Gemini API |
| Automation | UiPath, Excel |
| Deployment | Vercel, Render |

---

## Project Structure

```text
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
```

---

## Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/archisinha972-creator/AI-Resume-Screening.git
cd AI-Resume-Screening
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set the Gemini API Key

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

### 6. Start the Backend

```bash
uvicorn backend.main:app --reload
```

API:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Limitations

- The ML model uses a small synthetic dataset.
- Screening scores are prototype model outputs.
- Gemini API usage depends on API availability and usage limits.
- The system should not be used as an automated hiring decision system.

---

## Future Improvements

- Larger and more diverse datasets
- Job description analysis
- Resume-job matching
- Database integration
- Recruiter dashboard
- Authentication

---

## Author

**Archi Sinha**

CSE (AI & ML) — KIIT University

---

If you found this project interesting, consider giving it a star!