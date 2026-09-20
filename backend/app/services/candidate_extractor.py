import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import spacy

from app.models.candidate import CandidateProfile, Education

nlp = spacy.load("en_core_web_sm")

TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "data" / "skills_taxonomy.json"
with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
    SKILLS_TAXONOMY = json.load(f)

ALL_SKILLS = sorted(
    {skill.lower() for group in SKILLS_TAXONOMY.values() for skill in group},
    key=len,
    reverse=True,
)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")
YEAR_REGEX = re.compile(r"\b(19|20)\d{2}\b")

DEGREE_KEYWORDS = [
    "bachelor", "b.tech", "btech", "b.e", "be ", "b.sc", "bsc",
    "master", "m.tech", "mtech", "m.e", "msc", "m.sc", "mba",
    "phd", "ph.d", "doctorate",
]


def extract_email(text: str) -> Optional[str]:
    match = EMAIL_REGEX.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    match = PHONE_REGEX.search(text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> Optional[str]:
    first_chunk = text.strip().split("\n")[0]
    doc = nlp(first_chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    doc_full = nlp(text[:1000])
    for ent in doc_full.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def extract_education(text: str) -> List[Education]:
    results = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in DEGREE_KEYWORDS):
            year_match = YEAR_REGEX.search(line)
            results.append(Education(
                degree=line.strip()[:120],
                institution=None,
                year=year_match.group(0) if year_match else None,
            ))
    return results[:5]


def estimate_years_of_experience(text: str) -> Optional[float]:
    years_found = [int(match) for match in re.findall(r"\b((?:19|20)\d{2})\b", text)]
    if len(years_found) < 2:
        return None
    span = max(years_found) - min(years_found)
    current_year = datetime.now().year
    if max(years_found) > current_year:
        return None
    return round(min(span, 25), 1)


def extract_candidate_profile(resume_id: str, text: str) -> CandidateProfile:
    return CandidateProfile(
        resume_id=resume_id,
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=extract_skills(text),
        education=extract_education(text),
        years_of_experience=estimate_years_of_experience(text),
        raw_text_length=len(text),
    )
