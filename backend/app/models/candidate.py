from pydantic import BaseModel
from typing import List, Optional


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


class CandidateProfile(BaseModel):
    resume_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[Education] = []
    years_of_experience: Optional[float] = None
    raw_text_length: int
