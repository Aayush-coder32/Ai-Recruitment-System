from fastapi import FastAPI, HTTPException
from models.schemas import ScreeningRequest, ScreeningResponse, RankedCandidate, ScoreBreakdown
from core.parser import parse_job_description
from core.ranker import rank_candidates
from core.explainer import explain_all_candidates

app = FastAPI(
    title="AI Recruiting System",
    description="AI-powered candidate screening and ranking API",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {"status": "running", "message": "AI Recruiting System is live"}


@app.post("/screen", response_model=ScreeningResponse)
def screen_candidates(request: ScreeningRequest):
    try:
        job_requirements = parse_job_description(request.job)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse job description: {str(e)}")

    try:
        ranked = rank_candidates(request.candidates, job_requirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rank candidates: {str(e)}")

    try:
        explained = explain_all_candidates(ranked, job_requirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate explanations: {str(e)}")

    results = []
    for item in explained:
        candidate = item["candidate"]
        scores = item["scores"]

        results.append(RankedCandidate(
            rank=item["rank"],
            candidateId=candidate.id,
            name=f"{candidate.firstName} {candidate.lastName}",
            email=str(candidate.email),
            headline=candidate.headline,
            location=candidate.location,
            score=ScoreBreakdown(
                skills=scores["skills"],
                projects=scores["projects"],
                experience=scores["experience"],
                education=scores["education"],
                bonus=scores["bonus"],
                total=scores["total"]
            ),
            evidenceMultiplier=item["evidenceMultiplier"],
            explanation=item["explanation"]
        ))

    return ScreeningResponse(
        jobTitle=request.job.title,
        totalCandidates=len(request.candidates),
        shortlisted=len(results),
        results=results
    )