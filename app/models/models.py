from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, JSON
from app.database.db import Base

def utcnow():
    return datetime.now(timezone.utc)

class CandidateContext(Base):
    __tablename__ = "candidate_contexts"
    candidate_id = Column(String, primary_key=True)
    skills = Column(JSON, default=list)
    experience = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    target_role = Column(String, nullable=True)

class JobContext(Base):
    __tablename__ = "job_contexts"
    job_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    required_skills = Column(JSON, default=list)
    competencies = Column(JSON, default=list)

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    interview_id = Column(String, primary_key=True)
    candidate_id = Column(String, nullable=False)
    job_id = Column(String, nullable=False)
    status = Column(String, default="CREATED")
    mode = Column(String, default="text")
    interview_type = Column(String, default="technical")
    question_count = Column(Integer, default=10)
    difficulty = Column(String, default="adaptive")
    current_sequence = Column(Integer, default=0)
    followup_count = Column(Integer, default=0)
    covered_competencies = Column(JSON, default=list)
    weak_areas = Column(JSON, default=list)
    asked_question_ids = Column(JSON, default=list)
    model_name = Column(String, default="fallback")
    config_version = Column(String, default="v1")
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow)

class Question(Base):
    __tablename__ = "questions"
    question_id = Column(String, primary_key=True)
    interview_id = Column(String, ForeignKey("interview_sessions.interview_id"))
    competency = Column(String)
    type = Column(String)
    difficulty = Column(Integer)
    text = Column(Text)
    sequence = Column(Integer)

class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column(String, primary_key=True)
    interview_id = Column(String, ForeignKey("interview_sessions.interview_id"))
    question_id = Column(String, ForeignKey("questions.question_id"))
    text = Column(Text)
    modality = Column(String, default="text")
    timestamp = Column(DateTime, default=utcnow)

class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"
    evaluation_id = Column(String, primary_key=True)
    answer_id = Column(String, ForeignKey("answers.answer_id"))
    relevance = Column(Float)
    correctness = Column(Float)
    depth = Column(Float)
    evidence = Column(Float)
    problem_solving = Column(Float)
    communication = Column(Float)
    overall_score = Column(Float)
    evidence_text = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    gaps = Column(JSON, default=list)
    confidence = Column(Float, default=0.5)
    needs_followup = Column(Integer, default=0)
    followup_reason = Column(Text, default="")

class InterviewReport(Base):
    __tablename__ = "interview_reports"
    report_id = Column(String, primary_key=True)
    interview_id = Column(String, ForeignKey("interview_sessions.interview_id"))
    version = Column(String, default="v1")
    overall_score = Column(Float)
    scores = Column(JSON, default=dict)
    strengths = Column(JSON, default=list)
    gaps = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    limitations = Column(JSON, default=list)
    generated_at = Column(DateTime, default=utcnow)
