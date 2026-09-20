from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.jd_parser import parse_job_description
from app.core.database import get_db
from app.models.db_models import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


class JobDescriptionInput(BaseModel):
    text: str


@router.post("/parse")
async def parse_jd(payload: JobDescriptionInput, db: Session = Depends(get_db)):
    requirements = parse_job_description(payload.text)

    job_row = Job(
        id=requirements.job_id,
        title=requirements.title,
        raw_text=payload.text,
        required_skills=requirements.required_skills,
        preferred_skills=requirements.preferred_skills,
        min_years_experience=requirements.min_years_experience,
        education_requirement=requirements.education_requirement,
    )
    db.add(job_row)
    db.commit()
    db.refresh(job_row)

    return {"job_requirements": requirements}
