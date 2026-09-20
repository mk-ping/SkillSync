from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.db_models import Job, Candidate
from app.models.candidate import CandidateProfile, Education
from app.models.job import JobRequirements
from app.models.user import User
from app.services.matching_engine import compute_hybrid_score

router = APIRouter(prefix="/rank", tags=["Ranking"])


class RankRequest(BaseModel):
    candidate_ids: List[str]


@router.post("/{job_id}")
async def rank_candidates(
    job_id: str,
    payload: RankRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_row = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job_row:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = db.query(Candidate).filter(
        Candidate.id.in_(payload.candidate_ids),
        Candidate.user_id == current_user.id,
    ).all()
    if not candidates:
        raise HTTPException(status_code=400, detail="No matching candidates found for the given IDs")

    job = JobRequirements(
        job_id=job_row.id,
        title=job_row.title,
        required_skills=job_row.required_skills or [],
        preferred_skills=job_row.preferred_skills or [],
        min_years_experience=job_row.min_years_experience,
        education_requirement=job_row.education_requirement,
        raw_text_length=len(job_row.raw_text),
    )
    job_text = job_row.raw_text

    results = []
    for row in candidates:
        candidate = CandidateProfile(
            resume_id=row.id,
            name=row.name,
            email=row.email,
            phone=row.phone,
            skills=row.skills or [],
            education=[Education(**e) for e in (row.education or [])],
            years_of_experience=row.years_of_experience,
            raw_text_length=len(row.raw_text),
        )
        score_result = compute_hybrid_score(job, job_text, candidate, row.raw_text)

        row.job_id = job_id
        row.final_score = score_result["final_score"]
        row.score_breakdown = score_result["breakdown"]
        row.matched_required_skills = score_result["matched_required_skills"]
        row.matched_preferred_skills = score_result["matched_preferred_skills"]
        row.missing_required_skills = score_result["missing_required_skills"]
        row.missing_preferred_skills = score_result["missing_preferred_skills"]

        results.append(score_result)

    db.commit()
    results.sort(key=lambda r: r["final_score"], reverse=True)

    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(results),
        "ranked_candidates": results,
    }
