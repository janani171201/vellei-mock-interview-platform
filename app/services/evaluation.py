from app.services.llm import call_llm
import json

def fallback_evaluate(question, competency, answer):
    words = answer.strip().split()
    lower = answer.lower()
    evidence_signals = ["because", "example", "project", "implemented", "measured", "result", "trade-off"]
    evidence_count = sum(1 for x in evidence_signals if x in lower)

    relevance = min(100, 45 + min(len(words), 50))
    correctness = 65 if len(words) >= 25 else 45
    depth = min(100, 40 + len(words) + evidence_count * 8)
    evidence = min(100, 35 + evidence_count * 15)
    problem_solving = min(100, 45 + len(words) * 0.8)
    communication = min(100, 50 + (20 if len(words) >= 20 else 0))

    score = (
        relevance * .15 + correctness * .25 + depth * .20 +
        evidence * .15 + problem_solving * .15 + communication * .10
    )
    needs = score < 62 or evidence < 55 or len(words) < 15

    return {
        "relevance": round(relevance, 1),
        "correctness": round(correctness, 1),
        "depth": round(depth, 1),
        "evidence": round(evidence, 1),
        "problem_solving": round(problem_solving, 1),
        "communication": round(communication, 1),
        "overall_score": round(score, 1),
        "evidence_text": [answer[:300]],
        "strengths": [f"Addresses {competency}"] if score >= 65 else [],
        "gaps": [f"Provide stronger concrete evidence for {competency}."] if needs else [],
        "confidence": 0.55,
        "needs_followup": needs,
        "followup_reason": "The answer needs more concrete explanation or evidence." if needs else ""
    }

def evaluate_answer(question, competency, answer, candidate=None, job=None):
    system = (
        "You are an interview evaluator. Return ONLY JSON with numeric scores 0-100 for "
        "relevance, correctness, depth, evidence, problem_solving, communication, overall_score; "
        "arrays evidence_text, strengths, gaps; confidence 0-1; boolean needs_followup; "
        "and followup_reason. Evidence must come from the answer. Do not invent candidate facts."
    )
    result = call_llm(system, json.dumps({
        "question": question,
        "competency": competency,
        "answer": answer,
        "candidate": candidate or {},
        "job": job or {}
    }))
    return result if result else fallback_evaluate(question, competency, answer)
