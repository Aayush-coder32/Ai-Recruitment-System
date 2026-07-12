from utils.gemini import ask_gemini
from models.temporary import TemporaryTalentProfile


def explain_candidate(
    rank: int,
    candidate: TemporaryTalentProfile,
    scores: dict,
    multiplier: float,
    job_requirements: dict
) -> str:

    skill_names = [s.name for s in candidate.skills]
    project_names = [p.name for p in candidate.projects]
    experience_roles = [f"{e.role} at {e.company}" for e in candidate.experience]
    education_summary = [f"{e.degree} in {e.fieldOfStudy} from {e.institution}" for e in candidate.education]
    has_github = bool(candidate.socialLinks and candidate.socialLinks.github)
    has_portfolio = bool(candidate.socialLinks and candidate.socialLinks.portfolio)
    projects_with_links = len([p for p in candidate.projects if p.link])
    cert_names = [c.name for c in (candidate.certifications or [])]

    prompt = f"""
You are an AI recruiting assistant. Write a clear, professional explanation for why this candidate received their ranking.

CANDIDATE INFORMATION:
- Name: {candidate.firstName} {candidate.lastName}
- Headline: {candidate.headline}
- Skills: {", ".join(skill_names)}
- Projects: {", ".join(project_names)}
- Experience: {", ".join(experience_roles)}
- Education: {", ".join(education_summary)}
- Certifications: {", ".join(cert_names) if cert_names else "None"}
- Has GitHub: {has_github}
- Has Portfolio: {has_portfolio}
- Projects with links: {projects_with_links} out of {len(candidate.projects)}

SCORE BREAKDOWN:
- Skills Score: {scores["skills"]} / 45
- Projects Score: {scores["projects"]} / 25
- Experience Score: {scores["experience"]} / 15
- Education Score: {scores["education"]} / 10
- Bonus Score: {scores["bonus"]} / 5
- Evidence Multiplier: {multiplier} (1.0 = full trust, 0.85 = partial, 0.70 = low evidence)
- Final Total: {scores["total"]} / 100

JOB REQUIREMENTS:
- Required Skills: {", ".join(job_requirements.get("required_skills", []))}
- Minimum Experience: {job_requirements.get("minimum_experience_years", 0)} years
- Seniority Level: {job_requirements.get("seniority_level", "Any")}

Write a 3-4 sentence explanation that:
1. States their rank and overall score
2. Highlights their strongest matching qualities
3. Mentions any gaps or weaknesses
4. Comments on their evidence/trust level if the multiplier is below 1.0

Be direct, professional, and specific. Do not use bullet points. Write in paragraph form only.
"""

    try:
        explanation = ask_gemini(prompt)
        return explanation.strip()
    except Exception:
        return (
            f"Ranked #{rank} with a total score of {scores['total']}/100. "
            f"Skills score: {scores['skills']}/45, Projects: {scores['projects']}/25, "
            f"Experience: {scores['experience']}/15, Education: {scores['education']}/10, "
            f"Bonus: {scores['bonus']}/5. Evidence multiplier: {multiplier}."
        )


def explain_all_candidates(ranked_candidates: list, job_requirements: dict) -> list:
    results = []

    for item in ranked_candidates:
        explanation = explain_candidate(
            rank=item["rank"],
            candidate=item["candidate"],
            scores=item["scores"],
            multiplier=item["evidenceMultiplier"],
            job_requirements=job_requirements
        )

        results.append({
            "rank": item["rank"],
            "candidate": item["candidate"],
            "scores": item["scores"],
            "evidenceMultiplier": item["evidenceMultiplier"],
            "explanation": explanation
        })

    return results
