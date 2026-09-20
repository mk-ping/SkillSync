from typing import Dict

from app.models.candidate import CandidateProfile
from app.models.job import JobRequirements
from app.services.matching_engine import semantic_similarity, dynamic_phrase_match, experience_match_score


def extract_features(
    job: JobRequirements,
    job_text: str,
    candidate: CandidateProfile,
    resume_text: str,
) -> Dict[str, float]:
    """
    Engineers the feature vector used for ranking.
    Each feature is a float in [0, 1]. This is the same feature set
    described in the resume: semantic similarity, skill-phrase overlap,
    and experience alignment.
    """
    semantic_score = semantic_similarity(job_text, resume_text)

    required_phrases = job.required_skills
    preferred_phrases = job.preferred_skills
    skill_result = dynamic_phrase_match(required_phrases, preferred_phrases, resume_text)

    exp_score = experience_match_score(job.min_years_experience, candidate.years_of_experience)

    return {
        "semantic_similarity": semantic_score,
        "skill_overlap": skill_result["combined_skill_score"],
        "experience_alignment": exp_score,
    }


FEATURE_ORDER = ["semantic_similarity", "skill_overlap", "experience_alignment"]


def features_to_vector(features: Dict[str, float]) -> list:
    return [features[f] for f in FEATURE_ORDER]
