import uuid

def build_report(evaluations):
    overall = round(sum(e.overall_score for e in evaluations) / len(evaluations), 1) if evaluations else 0
    strengths, gaps = [], []
    for e in evaluations:
        for s in e.strengths or []:
            if s not in strengths:
                strengths.append(s)
        for g in e.gaps or []:
            if g and g not in gaps:
                gaps.append(g)

    recommendations = [{
        "gap": gap,
        "resource": "Targeted learning material and a small hands-on exercise for the competency.",
        "action": "Complete one practical exercise and explain the trade-offs aloud.",
        "priority": "high"
    } for gap in gaps[:8]]

    return {
        "report_id": "R-" + uuid.uuid4().hex[:8],
        "version": "v1",
        "overall_score": overall,
        "scores": {"overall": overall, "evaluation_count": len(evaluations)},
        "strengths": strengths[:10],
        "gaps": gaps[:10],
        "recommendations": recommendations,
        "limitations": [
            "This is an AI-generated advisory assessment, not a hiring decision.",
            "Scores depend on the supplied questions, answers and model/configuration."
        ]
    }
