import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=True)
    raw_text = Column(String)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    min_years_experience = Column(Float, nullable=True)
    education_requirement = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=True)
    original_filename = Column(String, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    skills = Column(JSON, default=list)
    education = Column(JSON, default=list)
    years_of_experience = Column(Float, nullable=True)
    raw_text = Column(String)
    final_score = Column(Float, nullable=True)
    score_breakdown = Column(JSON, nullable=True)
    matched_required_skills = Column(JSON, default=list)
    matched_preferred_skills = Column(JSON, default=list)
    missing_required_skills = Column(JSON, default=list)
    missing_preferred_skills = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="candidates")
