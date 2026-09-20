import re
import uuid
from typing import List, Optional

from app.models.job import JobRequirements
from app.services.candidate_extractor import ALL_SKILLS
from app.services.phrase_extractor import extract_key_phrases

PREFERRED_MARKERS = ["preferred", "nice to have", "bonus", "plus", "good to have"]
REQUIRED_MARKERS = ["required", "must have", "must-have", "requirements", "responsibilities", "who can apply", "qualifications"]

DEGREE_KEYWORDS = [
    "bachelor", "b.tech", "btech", "master", "m.tech", "mtech",
    "phd", "ph.d", "mba", "b.sc", "m.sc",
]

EXPERIENCE_REGEX = re.compile(
    r"(\d+)\+?\s*(?:to\s*\d+\s*)?years?\s*(?:of)?\s*experience", re.IGNORECASE
)


def split_into_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {"preferred": [], "required": [], "general": []}
    current = "general"
    for line in lines:
        line_lower = line.lower().strip()
        if any(marker in line_lower for marker in PREFERRED_MARKERS):
            current = "preferred"
            continue
        if any(marker in line_lower for marker in REQUIRED_MARKERS):
            current = "required"
            continue
        if line.strip():
            sections[current].append(line)
    return sections


def extract_taxonomy_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def extract_min_experience(text: str) -> Optional[float]:
    matches = EXPERIENCE_REGEX.findall(text)
    if not matches:
        return None
    years = [int(m) for m in matches]
    return float(min(years))


def extract_education_requirement(text: str) -> Optional[str]:
    text_lower = text.lower()
    for keyword in DEGREE_KEYWORDS:
        if keyword in text_lower:
            idx = text_lower.find(keyword)
            snippet = text[max(0, idx - 20):idx + 60].strip()
            return snippet
    return None


def extract_title(text: str) -> Optional[str]:
    first_line = text.strip().split("\n")[0].strip()
    if 3 < len(first_line) < 100:
        return first_line
    return None


def parse_job_description(text: str) -> JobRequirements:
    job_id = str(uuid.uuid4())
    sections = split_into_sections(text)

    required_text = " ".join(sections["required"]) or text
    preferred_text = " ".join(sections["preferred"])

    required_phrases = extract_key_phrases(required_text, max_phrases=30)
    preferred_phrases = extract_key_phrases(preferred_text, max_phrases=15) if preferred_text.strip() else []

    taxonomy_required = extract_taxonomy_skills(required_text)
    for skill in taxonomy_required:
        if skill not in required_phrases:
            required_phrases.append(skill)

    preferred_phrases = [p for p in preferred_phrases if p not in required_phrases]

    return JobRequirements(
        job_id=job_id,
        title=extract_title(text),
        required_skills=required_phrases,
        preferred_skills=preferred_phrases,
        min_years_experience=extract_min_experience(text),
        education_requirement=extract_education_requirement(text),
        raw_text_length=len(text),
    )
