from typing import List, Dict, Optional

from sentence_transformers import SentenceTransformer, util

from app.models.candidate import CandidateProfile
from app.models.job import JobRequirements
from app.services.phrase_extractor import extract_key_phrases

_model: Optional[SentenceTransformer] = None

MATCH_THRESHOLD = 0.5


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def semantic_similarity(job_text: str, resume_text: str) -> float:
    model = get_model()
    embeddings = model.encode([job_text, resume_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(max(0.0, min(1.0, score)), 4)


def dynamic_phrase_match(required_phrases: List[str], preferred_phrases: List[str], resume_text: str) -> Dict:
    model = get_model()

    resume_phrases = extract_key_phrases(resume_text, max_phrases=80)
    if not resume_phrases:
        resume_phrases = [resume_text[:500]]

    resume_embeddings = model.encode(resume_phrases, convert_to_tensor=True)

    def match_set(phrases: List[str]) -> Dict:
        matched, missing = [], []
        if not phrases:
            return {"matched": [], "missing": [], "score": 1.0}

        phrase_embeddings = model.encode(phrases, convert_to_tensor=True)
        sims = util.cos_sim(phrase_embeddings, resume_embeddings)

        for i, phrase in enumerate(phrases):
            best_sim = sims[i].max().item()
            if best_sim >= MATCH_THRESHOLD:
                matched.append(phrase)
            else:
                missing.append(phrase)

        score = len(matched) / len(phrases) if phrases else 1.0
        return {"matched": matched, "missing": missing, "score": round(score, 4)}

    required_result = match_set(required_phrases)
    preferred_result = match_set(preferred_phrases)

    combined_skill_score = (required_result["score"] * 0.8) + (preferred_result["score"] * 0.2)

    return {
        "matched_required": required_result["matched"],
        "matched_preferred": preferred_result["matched"],
        "missing_required": required_result["missing"],
        "missing_preferred": preferred_result["missing"],
        "required_score": required_result["score"],
        "preferred_score": preferred_result["score"],
        "combined_skill_score": round(combined_skill_score, 4),
    }


def experience_match_score(min_years_required: Optional[float], candidate_years: Optional[float]) -> float:
    if min_years_required is None:
        return 1.0
    if candidate_years is None:
        return 0.5
    if candidate_years >= min_years_required:
        return 1.0
    return round(max(0.0, candidate_years / min_years_required), 4)


def compute_hybrid_score(
    job: JobRequirements,
    job_text: str,
    candidate: CandidateProfile,
    resume_text: str,
) -> Dict:
    semantic_score = semantic_similarity(job_text, resume_text)

    required_phrases = job.required_skills if job.required_skills else extract_key_phrases(job_text, max_phrases=40)
    preferred_phrases = job.preferred_skills

    skill_result = dynamic_phrase_match(required_phrases, preferred_phrases, resume_text)
    exp_score = experience_match_score(job.min_years_experience, candidate.years_of_experience)

    final_score = (
        semantic_score * 0.35
        + skill_result["combined_skill_score"] * 0.45
        + exp_score * 0.20
    )

    return {
        "candidate_id": candidate.resume_id,
        "candidate_name": candidate.name,
        "final_score": round(final_score * 100, 1),
        "breakdown": {
            "semantic_similarity": round(semantic_score * 100, 1),
            "skill_match": round(skill_result["combined_skill_score"] * 100, 1),
            "experience_match": round(exp_score * 100, 1),
        },
        "matched_required_skills": skill_result["matched_required"],
        "matched_preferred_skills": skill_result["matched_preferred"],
        "missing_required_skills": skill_result["missing_required"],
        "missing_preferred_skills": skill_result["missing_preferred"],
    }
