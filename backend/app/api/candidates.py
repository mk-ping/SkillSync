from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.db_models import Job, Candidate
from app.models.candidate import CandidateProfile, Education
from app.models.job import JobRequirements
from app.models.user import User
from app.services.matching_engine import compute_hybrid_score
from app.services.explainability import generate_explanation, build_skill_gap_chart

router = APIRouter(prefix="/candidates", tags=["Candidates"])


def _to_candidate_profile(candidate_row: Candidate) -> CandidateProfile:
    return CandidateProfile(
        resume_id=candidate_row.id,
        name=candidate_row.name,
        email=candidate_row.email,
        phone=candidate_row.phone,
        skills=candidate_row.skills or [],
        education=[Education(**e) for e in (candidate_row.education or [])],
        years_of_experience=candidate_row.years_of_experience,
        raw_text_length=len(candidate_row.raw_text),
    )


def _to_job_requirements(job_row: Job) -> JobRequirements:
    return JobRequirements(
        job_id=job_row.id,
        title=job_row.title,
        required_skills=job_row.required_skills or [],
        preferred_skills=job_row.preferred_skills or [],
        min_years_experience=job_row.min_years_experience,
        education_requirement=job_row.education_requirement,
        raw_text_length=len(job_row.raw_text),
    )


@router.get("/{candidate_id}/explain/{job_id}")
async def explain_candidate(
    candidate_id: str,
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate_row = db.query(Candidate).filter(
        Candidate.id == candidate_id, Candidate.user_id == current_user.id
    ).first()
    job_row = db.query(Job).filter(
        Job.id == job_id, Job.user_id == current_user.id
    ).first()

    if not candidate_row:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if not job_row:
        raise HTTPException(status_code=404, detail="Job not found")

    candidate = _to_candidate_profile(candidate_row)
    job = _to_job_requirements(job_row)

    score_result = compute_hybrid_score(job, job_row.raw_text, candidate, candidate_row.raw_text)
    explanation = generate_explanation(job, candidate, score_result)
    skill_gap_chart = build_skill_gap_chart(job, candidate)

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "score_result": score_result,
        "explanation": explanation,
        "skill_gap_chart": skill_gap_chart,
    }


@router.get("/{candidate_id}/best-roles")
async def best_roles_for_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate_row = db.query(Candidate).filter(
        Candidate.id == candidate_id, Candidate.user_id == current_user.id
    ).first()
    if not candidate_row:
        raise HTTPException(status_code=404, detail="Candidate not found")

    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    if not jobs:
        raise HTTPException(status_code=400, detail="No jobs available to compare against")

    candidate = _to_candidate_profile(candidate_row)

    results = []
    for job_row in jobs:
        job = _to_job_requirements(job_row)
        score_result = compute_hybrid_score(job, job_row.raw_text, candidate, candidate_row.raw_text)

        results.append({
            "job_id": job_row.id,
            "job_title": job.title or "Untitled role",
            "final_score": score_result["final_score"],
            "breakdown": score_result["breakdown"],
            "matched_required_skills": score_result["matched_required_skills"],
            "missing_required_skills": score_result["missing_required_skills"],
        })

    results.sort(key=lambda r: r["final_score"], reverse=True)

    return {
        "candidate_id": candidate_id,
        "candidate_name": candidate.name,
        "total_roles_compared": len(results),
        "best_roles": results,
    }
