import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.resume_parser import extract_resume_text
from app.services.candidate_extractor import extract_candidate_profile
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.db_models import Candidate
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = Path("../data/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}{ext}"
    saved_path = UPLOAD_DIR / saved_filename

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_resume_text(str(saved_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    profile = extract_candidate_profile(file_id, extracted_text)
    education_list = [e.dict() for e in profile.education]

    candidate_row = Candidate(
        id=file_id,
        user_id=current_user.id,
        original_filename=file.filename,
        name=profile.name,
        email=profile.email,
        phone=profile.phone,
        skills=profile.skills,
        education=education_list,
        years_of_experience=profile.years_of_experience,
        raw_text=extracted_text,
    )
    db.add(candidate_row)
    db.commit()
    db.refresh(candidate_row)

    return {
        "resume_id": file_id,
        "original_filename": file.filename,
        "saved_as": saved_filename,
        "profile": profile,
    }
