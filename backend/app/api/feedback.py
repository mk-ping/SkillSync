from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.db_models import Job, Candidate
from app.models.candidate import CandidateProfile, Education
from app.models.job import JobRequirements
from app.models.feedback import MatchFeedback
from app.models.user import User
from app.services.feature_engineering import extract_features

router = APIRouter(prefix="/feedback", tags=["Feedback"])


class FeedbackInput(BaseModel):
    job_id: str
    candidate_id: str
    label: int


@router.post("/")
async def submit_feedback(
    payload: FeedbackInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.label not in (0, 1):
        raise HTTPException(status_code=400, detail="label must be 0 or 1")

    job_row = db.query(Job).filter(Job.id == payload.job_id, Job.user_id == current_user.id).first()
    candidate_row = db.query(Candidate).filter(
        Candidate.id == payload.candidate_id, Candidate.user_id == current_user.id
    ).first()

    if not job_row or not candidate_row:
        raise HTTPException(status_code=404, detail="Job or candidate not found")

    job = JobRequirements(
        job_id=job_row.id,
        title=job_row.title,
        required_skills=job_row.required_skills or [],
        preferred_skills=job_row.preferred_skills or [],
        min_years_experience=job_row.min_years_experience,
        education_requirement=job_row.education_requirement,
        raw_text_length=len(job_row.raw_text),
    )
    candidate = CandidateProfile(
        resume_id=candidate_row.id,
        name=candidate_row.name,
        email=candidate_row.email,
        phone=candidate_row.phone,
        skills=candidate_row.skills or [],
        education=[Education(**e) for e in (candidate_row.education or [])],
        years_of_experience=candidate_row.years_of_experience,
        raw_text_length=len(candidate_row.raw_text),
    )

    features = extract_features(job, job_row.raw_text, candidate, candidate_row.raw_text)

    feedback_row = MatchFeedback(
        user_id=current_user.id,
        job_id=payload.job_id,
        candidate_id=payload.candidate_id,
        semantic_similarity=features["semantic_similarity"],
        skill_overlap=features["skill_overlap"],
        experience_alignment=features["experience_alignment"],
        label=payload.label,
    )
    db.add(feedback_row)
    db.commit()

    total_labels = db.query(MatchFeedback).count()

    return {
        "status": "recorded",
        "features": features,
        "total_labels_collected": total_labels,
    }
