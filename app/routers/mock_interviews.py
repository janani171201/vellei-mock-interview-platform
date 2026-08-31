import uuid
from fastapi import APIRouter, HTTPException
from app.database.db import SessionLocal
from app.models.models import CandidateContext, JobContext, InterviewSession, Question, Answer, AnswerEvaluation, InterviewReport
from app.schemas.interview import CreateInterviewRequest, AnswerRequest, EvaluateRequest
from app.services.question_engine import choose_competencies, generate_question
from app.services.evaluation import evaluate_answer
from app.services.followup import decide_followup, followup_text
from app.services.report import build_report
from app.config import settings

router = APIRouter(prefix="/mock-interviews", tags=["Mock Interviews"])

def get_session(db, interview_id):
    session = db.get(InterviewSession, interview_id)
    if not session:
        raise HTTPException(404, "Interview session not found")
    return session

def get_candidate_job(db, session):
    return db.get(CandidateContext, session.candidate_id), db.get(JobContext, session.job_id)

@router.post("")
def create_interview(req: CreateInterviewRequest):
    db = SessionLocal()
    try:
        db.merge(CandidateContext(
            candidate_id=req.candidate.candidate_id,
            skills=req.candidate.skills,
            experience=req.candidate.experience,
            projects=req.candidate.projects,
            target_role=req.candidate.target_role
        ))
        db.merge(JobContext(
            job_id=req.job.job_id,
            title=req.job.title,
            description=req.job.description,
            required_skills=req.job.required_skills,
            competencies=req.job.competencies
        ))
        interview_id = "INT-" + uuid.uuid4().hex[:10]
        session = InterviewSession(
            interview_id=interview_id,
            candidate_id=req.candidate.candidate_id,
            job_id=req.job.job_id,
            mode=req.mode,
            interview_type=req.interview_type,
            question_count=req.question_count,
            difficulty=req.difficulty,
            model_name="openai:" + settings.openai_model if settings.openai_api_key else "fallback"
        )
        db.add(session)
        db.commit()
        return {"interview_id": interview_id, "status": "CREATED"}
    finally:
        db.close()

@router.get("/{interview_id}")
def get_interview(interview_id: str):
    db = SessionLocal()
    try:
        s = get_session(db, interview_id)
        return {
            "interview_id": s.interview_id, "status": s.status,
            "sequence": s.current_sequence, "question_count": s.question_count,
            "covered_competencies": s.covered_competencies or [],
            "weak_areas": s.weak_areas or [], "followup_count": s.followup_count
        }
    finally:
        db.close()

@router.post("/{interview_id}/start")
def start_interview(interview_id: str):
    db = SessionLocal()
    try:
        s = get_session(db, interview_id)
        candidate, job = get_candidate_job(db, s)
        if s.status not in ["CREATED", "CONTEXT_READY"]:
            raise HTTPException(400, "Interview has already started or completed")
        s.status = "QUESTIONING"
        s.current_sequence = 1
        competency = choose_competencies(job)[0]
        q = generate_question(candidate, job, {"previous_questions": []}, competency, 2, 1)
        obj = Question(
            question_id=q["question_id"], interview_id=interview_id,
            competency=q["competency"], type=q["question_type"],
            difficulty=q["difficulty"], text=q["text"], sequence=1
        )
        db.add(obj)
        s.asked_question_ids = [obj.question_id]
        db.commit()
        return {
            "message": "Interview started",
            "interviewer_message": "Welcome. I will ask role-relevant questions and adapt based on your answers.",
            "question": {"question_id": q["question_id"], "text": q["text"],
                         "competency": q["competency"], "question_type": q["question_type"],
                         "difficulty": q["difficulty"]}
        }
    finally:
        db.close()

@router.post("/{interview_id}/answers")
def submit_answer(interview_id: str, req: AnswerRequest):
    db = SessionLocal()
    try:
        s = get_session(db, interview_id)
        if s.status != "QUESTIONING":
            raise HTTPException(400, "Interview is not accepting answers")
        q = db.get(Question, req.question_id)
        if not q or q.interview_id != interview_id:
            raise HTTPException(404, "Question not found")

        a = Answer(answer_id="A-" + uuid.uuid4().hex[:10], interview_id=interview_id,
                   question_id=req.question_id, text=req.answer[:settings.max_answer_length])
        db.add(a)
        db.flush()

        candidate, job = get_candidate_job(db, s)
        result = evaluate_answer(
            q.text, q.competency, a.text,
            candidate={"skills": candidate.skills, "projects": candidate.projects},
            job={"title": job.title, "required_skills": job.required_skills}
        )

        ev = AnswerEvaluation(
            evaluation_id="E-" + uuid.uuid4().hex[:10], answer_id=a.answer_id,
            relevance=result["relevance"], correctness=result["correctness"],
            depth=result["depth"], evidence=result["evidence"],
            problem_solving=result["problem_solving"], communication=result["communication"],
            overall_score=result["overall_score"], evidence_text=result["evidence_text"],
            strengths=result["strengths"], gaps=result["gaps"],
            confidence=result["confidence"], needs_followup=1 if result["needs_followup"] else 0,
            followup_reason=result["followup_reason"]
        )
        db.add(ev)

        covered = list(s.covered_competencies or [])
        if q.competency not in covered and not result["needs_followup"]:
            covered.append(q.competency)
        s.covered_competencies = covered

        gaps = list(s.weak_areas or [])
        for gap in result["gaps"]:
            if gap and gap not in gaps:
                gaps.append(gap)
        s.weak_areas = gaps

        do_followup, reason = decide_followup(result, s)
        if do_followup:
            s.followup_count += 1
            s.current_sequence += 1
            qid = "Q-" + uuid.uuid4().hex[:8]
            text = followup_text(q.competency, reason)
            nxt = Question(question_id=qid, interview_id=interview_id,
                           competency=q.competency, type="follow_up",
                           difficulty=min(q.difficulty + 1, 5), text=text,
                           sequence=s.current_sequence)
            db.add(nxt)
            ids = list(s.asked_question_ids or [])
            ids.append(qid)
            s.asked_question_ids = ids
            db.commit()
            return {
                "action": "follow_up",
                "evaluation": {"overall_score": result["overall_score"],
                               "strengths": result["strengths"], "gaps": result["gaps"]},
                "next_question": {"question_id": qid, "text": text,
                                  "competency": q.competency, "question_type": "follow_up",
                                  "difficulty": nxt.difficulty}
            }

        if s.current_sequence >= s.question_count:
            s.status = "COMPLETED"
            db.commit()
            return {"action": "complete", "message": "Question count reached. Complete the interview.",
                    "evaluation": {"overall_score": result["overall_score"]}}

        comps = choose_competencies(job)
        next_comp = next((c for c in comps if c not in covered), comps[s.current_sequence % len(comps)])
        s.current_sequence += 1
        difficulty = min(5, max(2, int(round(result["overall_score"] / 25))))
        previous = [x.text for x in db.query(Question).filter(Question.interview_id == interview_id).all()]
        nq = generate_question(candidate, job, {"previous_questions": previous}, next_comp, difficulty, s.current_sequence)
        nqobj = Question(question_id=nq["question_id"], interview_id=interview_id,
                         competency=nq["competency"], type=nq["question_type"],
                         difficulty=nq["difficulty"], text=nq["text"], sequence=s.current_sequence)
        db.add(nqobj)
        ids = list(s.asked_question_ids or [])
        ids.append(nqobj.question_id)
        s.asked_question_ids = ids
        db.commit()
        return {
            "action": "ask_question",
            "evaluation": {"overall_score": result["overall_score"]},
            "next_question": {"question_id": nq["question_id"], "text": nq["text"],
                              "competency": nq["competency"], "question_type": nq["question_type"],
                              "difficulty": nq["difficulty"]}
        }
    finally:
        db.close()

@router.post("/{interview_id}/complete")
def complete_interview(interview_id: str):
    db = SessionLocal()
    try:
        s = get_session(db, interview_id)
        s.status = "ANALYZING"
        evaluations = db.query(AnswerEvaluation).join(
            Answer, Answer.answer_id == AnswerEvaluation.answer_id
        ).filter(Answer.interview_id == interview_id).all()
        report_data = build_report(evaluations)
        db.add(InterviewReport(
            report_id=report_data["report_id"], interview_id=interview_id,
            version=report_data["version"], overall_score=report_data["overall_score"],
            scores=report_data["scores"], strengths=report_data["strengths"],
            gaps=report_data["gaps"], recommendations=report_data["recommendations"],
            limitations=report_data["limitations"]
        ))
        s.status = "REPORT_READY"
        db.commit()
        return report_data
    finally:
        db.close()

@router.get("/{interview_id}/transcript")
def transcript(interview_id: str):
    db = SessionLocal()
    try:
        get_session(db, interview_id)
        rows = db.query(Question, Answer, AnswerEvaluation).outerjoin(
            Answer, Answer.question_id == Question.question_id
        ).outerjoin(
            AnswerEvaluation, AnswerEvaluation.answer_id == Answer.answer_id
        ).filter(Question.interview_id == interview_id).order_by(Question.sequence).all()
        return {"interview_id": interview_id, "transcript": [
            {
                "question_id": q.question_id, "question": q.text,
                "competency": q.competency, "difficulty": q.difficulty,
                "answer": a.text if a else None,
                "evaluation": {
                    "overall_score": e.overall_score,
                    "strengths": e.strengths, "gaps": e.gaps,
                    "evidence": e.evidence_text
                } if e else None
            } for q, a, e in rows
        ]}
    finally:
        db.close()

@router.get("/{interview_id}/report")
def get_report(interview_id: str):
    db = SessionLocal()
    try:
        get_session(db, interview_id)
        report = db.query(InterviewReport).filter(
            InterviewReport.interview_id == interview_id
        ).order_by(InterviewReport.generated_at.desc()).first()
        if not report:
            raise HTTPException(404, "Report is not ready")
        return {
            "report_id": report.report_id, "interview_id": interview_id,
            "version": report.version, "overall_score": report.overall_score,
            "scores": report.scores, "strengths": report.strengths,
            "gaps": report.gaps, "recommendations": report.recommendations,
            "limitations": report.limitations, "generated_at": report.generated_at
        }
    finally:
        db.close()

@router.get("/{interview_id}/recommendations")
def recommendations(interview_id: str):
    return {"interview_id": interview_id, "recommendations": get_report(interview_id)["recommendations"]}

@router.post("/evaluate")
def developer_evaluate(req: EvaluateRequest):
    return evaluate_answer(
        req.question, req.competency, req.answer,
        candidate=req.candidate_context.model_dump() if req.candidate_context else None,
        job=req.job_context.model_dump() if req.job_context else None
    )
