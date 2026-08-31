from app.services.evaluation import evaluate_answer

def test_weak_answer_triggers_followup():
    result = evaluate_answer("Explain Python lists.", "Python", "They store data.")
    assert "overall_score" in result
    assert result["needs_followup"] is True

def test_stronger_answer_has_evidence():
    result = evaluate_answer(
        "Describe a Python project.", "Python",
        "In my project I implemented a FastAPI service because the team needed a REST API. "
        "I measured response time and improved it by caching repeated lookups."
    )
    assert result["evidence"] >= 50
