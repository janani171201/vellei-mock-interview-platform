def decide_followup(evaluation, session):
    if evaluation["needs_followup"] and session.followup_count < 2:
        return True, evaluation.get("followup_reason") or "Please provide more detail or a concrete example."
    return False, ""

def followup_text(competency, reason):
    return f"Thanks. To clarify your answer on {competency}: {reason}"
