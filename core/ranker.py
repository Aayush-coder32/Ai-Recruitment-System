from models.schemas import TalentProfile
from core.scorer import score_candidate


def rank_candidates(candidates: list[TalentProfile], job_requirements: dict) -> list[dict]:
    scored = []

    for candidate in candidates:
        if candidate.availability.status.value == "Not Available":
            continue

        scores, multiplier = score_candidate(candidate, job_requirements)

        scored.append({
            "candidate": candidate,
            "scores": scores,
            "evidenceMultiplier": multiplier
        })

    scored.sort(key=lambda x: x["scores"]["total"], reverse=True)

    ranked = []
    for index, item in enumerate(scored):
        ranked.append({
            "rank": index + 1,
            "candidate": item["candidate"],
            "scores": item["scores"],
            "evidenceMultiplier": item["evidenceMultiplier"]
        })

    return ranked