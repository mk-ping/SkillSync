from pydantic import BaseModel
from typing import List, Optional


class JobRequirements(BaseModel):
    job_id: str
    title: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    min_years_experience: Optional[float] = None
    education_requirement: Optional[str] = None
    raw_text_length: int
