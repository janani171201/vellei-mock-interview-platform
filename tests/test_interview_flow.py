from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_start():
    body = {
        "candidate":{"candidate_id":"TEST-CAND","skills":["Python","FastAPI"],"experience":[],"projects":[],"target_role":"Python Developer"},
        "job":{"job_id":"TEST-JOB","title":"Python Developer","description":"Python backend role","required_skills":["Python","FastAPI"],"competencies":["Python","FastAPI"]},
        "question_count":2
    }
    r=client.post("/api/v1/mock-interviews",json=body)
    assert r.status_code==200
    interview_id=r.json()["interview_id"]
    r=client.post(f"/api/v1/mock-interviews/{interview_id}/start")
    assert r.status_code==200
    assert r.json()["question"]["question_id"]
