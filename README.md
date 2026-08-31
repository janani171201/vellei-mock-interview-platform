# Vellei AI Mock Interview Platform

An AI-powered adaptive mock interview platform built with **FastAPI**. The system simulates a realistic interview by using candidate and job context to generate relevant questions, process candidate answers, generate adaptive follow-up questions, evaluate competencies, and produce a structured diagnostic report with recommendations.

## Project Overview

The Vellei AI Mock Interview Platform is designed to provide candidates with a realistic interview practice experience.

The platform takes:

* Candidate profile and skills
* Candidate experience and summary
* Target job title
* Job description
* Required job skills

and uses this information to conduct an adaptive mock interview.

### Core Workflow

```text
Candidate Context
        +
Job Context
        ↓
Create Interview
        ↓
Generate Interview Questions
        ↓
Candidate Answers
        ↓
Adaptive Follow-up Questions
        ↓
Competency Evaluation
        ↓
Interview Completion
        ↓
Transcript
        ↓
Diagnostic Report
        ↓
Recommendations
```

## Features

### 1. Candidate & Job Context

The platform accepts structured candidate information and target job information.

Candidate context includes:

* Candidate ID
* Name
* Experience
* Skills
* Candidate summary

Job context includes:

* Job ID
* Job title
* Job description
* Required skills

### 2. Adaptive Interview

The interview dynamically processes candidate answers and generates subsequent questions.

The system supports:

* Role-specific questions
* Candidate-context-based questions
* Follow-up questions
* Interview state management
* Answer tracking

### 3. Competency Evaluation

Candidate responses are evaluated against relevant competencies.

The evaluation can identify:

* Strengths
* Skill gaps
* Areas requiring improvement
* Overall interview performance

### 4. Diagnostic Report

After the interview is completed, the platform provides a structured report containing interview performance information and improvement guidance.

### 5. Recommendations

The platform generates recommendations based on the candidate's interview performance and identified gaps.

### 6. Interview Transcript

The complete interview conversation can be retrieved through the transcript API.

## Technology Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* **SQLite**
* **OpenAI / LLM integration**
* **Pytest**
* **HTML/CSS/JavaScript** for the basic frontend

## Project Structure

```text
vellei_mock_interview_platform/
│
├── app/
│   ├── database/
│   │   ├── db.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── mock_interviews.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── interview.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── evaluation.py
│   │   ├── followup.py
│   │   ├── llm.py
│   │   ├── question_engine.py
│   │   ├── report.py
│   │   └── __init__.py
│   │
│   ├── static/
│   │   └── index.html
│   │
│   ├── config.py
│   ├── main.py
│   └── __init__.py
│
├── tests/
│   ├── test_evaluation.py
│   ├── test_health.py
│   ├── test_interview_flow.py
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## API Endpoints

### Health

```http
GET /health
```

Checks whether the API is running.

### Create Interview

```http
POST /api/v1/mock-interviews
```

Creates a new mock interview using candidate and job context.

### Get Interview

```http
GET /api/v1/mock-interviews/{interview_id}
```

Retrieves interview information.

### Start Interview

```http
POST /api/v1/mock-interviews/{interview_id}/start
```

Starts the interview and generates the initial question.

### Submit Answer

```http
POST /api/v1/mock-interviews/{interview_id}/answers
```

Submits a candidate answer and continues the adaptive interview flow.

### Complete Interview

```http
POST /api/v1/mock-interviews/{interview_id}/complete
```

Completes the interview.

### Transcript

```http
GET /api/v1/mock-interviews/{interview_id}/transcript
```

Retrieves the interview transcript.

### Diagnostic Report

```http
GET /api/v1/mock-interviews/{interview_id}/report
```

Retrieves the candidate's interview evaluation report.

### Recommendations

```http
GET /api/v1/mock-interviews/{interview_id}/recommendations
```

Retrieves improvement recommendations.

### Developer Evaluation

```http
POST /api/v1/mock-interviews/evaluate
```

Provides an evaluation endpoint for testing and development.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/janani171201/vellei-mock-interview-platform.git
cd vellei-mock-interview-platform
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

**Never commit the actual API key to GitHub.**

## Run the Application

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative OpenAPI documentation:

```text
http://127.0.0.1:8000/redoc
```

## Testing

The project includes automated tests using Pytest.

Run:

```powershell
pytest
```

For more detailed output:

```powershell
pytest -v
```

## Example Candidate

```json
{
  "candidate_id": "CAND-001",
  "name": "Sample Candidate",
  "experience_years": 1,
  "skills": [
    "Python",
    "SQL",
    "Statistics",
    "Power BI"
  ],
  "summary": "Candidate with experience in data analysis and statistical programming."
}
```

## Example Job

```json
{
  "job_id": "JOB-001",
  "title": "Data Analyst",
  "description": "We are looking for a Data Analyst who can analyze datasets, write SQL queries, build dashboards and communicate insights.",
  "required_skills": [
    "Python",
    "SQL",
    "Statistics",
    "Power BI",
    "Data Analysis"
  ]
}
```

## Security

Sensitive configuration should be stored in environment variables.

The following files and directories are excluded from Git:

```text
.env
venv/
__pycache__/
*.pyc
.pytest_cache/
```

Do not expose API keys, passwords, or other secrets in source code or GitHub.

## Future Enhancements

Possible future improvements include:

* Voice-based interviews
* Speech-to-text integration
* Text-to-speech interviewer
* Real-time conversational interviews
* Advanced competency scoring
* Interview difficulty adaptation
* Resume and job-description upload
* Candidate readiness scoring
* Analytics dashboard
* Authentication and user management
* Interview history and progress tracking

## Project Status

**Current status: MVP / Working Prototype**

The project provides a FastAPI-based adaptive mock interview backend with interview creation, question generation, answer submission, follow-up handling, evaluation, reporting, transcript retrieval, and recommendations.

## Author

**Janani Mohan**

GitHub:

https://github.com/janani171201

## Repository

https://github.com/janani171201/vellei-mock-interview-platform
