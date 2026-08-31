from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

if settings.database_url.startswith("sqlite:///./"):
    Path("database").mkdir(exist_ok=True)

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db():
    from app.models.models import CandidateContext, JobContext, InterviewSession, Question, Answer, AnswerEvaluation, InterviewReport
    Base.metadata.create_all(bind=engine)
