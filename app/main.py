from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database.db import init_db
from app.routers.mock_interviews import router

app = FastAPI(
    title="Vellei AI Mock Interview Platform",
    version="1.0.0",
    description="Text MVP for adaptive AI mock interviews."
)

static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Vellei AI Mock Interview Platform is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}
