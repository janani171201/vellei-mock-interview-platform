from typing import List, Optional
from pydantic import BaseModel, Field

class CandidateContextIn(BaseModel):
    candidate_id: str
    skills: List[str] = []
    experience: List[dict] = []
    projects: List[dict] = []
    target_role: Optional[str] = None

class JobContextIn(BaseModel):
    job_id: str
    title: str
    description: str = ""
    required_skills: List[str] = []
    competencies: List[str] = []

class CreateInterviewRequest(BaseModel):
    candidate: CandidateContextIn
    job: JobContextIn
    mode: str = "text"
    interview_type: str = "technical"
    question_count: int = Field(default=10, ge=1, le=30)
    difficulty: str = "adaptive"

class AnswerRequest(BaseModel):
    question_id: str
    answer: str = Field(min_length=1, max_length=6000)
    client_timestamp: Optional[str] = None

class EvaluateRequest(BaseModel):
    question: str
    competency: str
    answer: str
    candidate_context: Optional[CandidateContextIn] = None
    job_context: Optional[JobContextIn] = None
