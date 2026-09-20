import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class MatchFeedback(Base):
    __tablename__ = "match_feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(String, ForeignKey("candidates.id"), nullable=False)

    semantic_similarity = Column(Float, nullable=False)
    skill_overlap = Column(Float, nullable=False)
    experience_alignment = Column(Float, nullable=False)

    label = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
