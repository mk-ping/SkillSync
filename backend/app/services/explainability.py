from typing import Dict, List

from app.models.candidate import CandidateProfile
from app.models.job import JobRequirements


def generate_explanation(job: JobRequirements, candidate: CandidateProfile, score_result: Dict) -> Dict:
    breakdown = score_result["breakdown"]
    matched_required = score_result["matched_required_skills"]
    missing_required = score_result["missing_required_skills"]
    matched_preferred = score_result["matched_preferred_skills"]

    strengths = []
    if breakdown["skill_match"] >= 70:
        strengths.append(f"Strong overlap on required skills ({len(matched_required)} matched)")
    if breakdown["semantic_similarity"] >= 70:
        strengths.append("Resume content closely aligns with the job description")
    if breakdown["experience_match"] >= 90:
        strengths.append("Meets or exceeds the experience requirement")
    if matched_preferred:
        strengths.append(f"Also covers {len(matched_preferred)} preferred/nice-to-have skills")

    concerns = []
    if missing_required:
        concerns.append(f"Missing {len(missing_required)} required skill(s): {', '.join(missing_required[:5])}")
    if breakdown["experience_match"] < 70:
        concerns.append("Experience appears below the stated requirement")
    if candidate.years_of_experience is None:
        concerns.append("Could not confidently estimate years of experience from resume")

    if not strengths:
        strengths.append("Some alignment with job requirements, but no standout strengths detected")
    if not concerns:
        concerns.append("No major gaps detected")

    summary = (
        f"{candidate.name or 'This candidate'} scored {score_result['final_score']}% overall. "
        f"Skill match contributed {breakdown['skill_match']}%, semantic alignment "
        f"{breakdown['semantic_similarity']}%, and experience match {breakdown['experience_match']}%."
    )

    return {
        "summary": summary,
        "strengths": strengths,
        "concerns": concerns,
    }


def build_skill_gap_chart(job: JobRequirements, candidate: CandidateProfile) -> List[Dict]:
    candidate_set = set(s.lower() for s in candidate.skills)
    all_relevant_skills = list(dict.fromkeys(job.required_skills + job.preferred_skills))

    chart_data = []
    for skill in all_relevant_skills:
        coverage = 100 if skill.lower() in candidate_set else 0
        chart_data.append({
            "skill": skill,
            "coverage": coverage,
            "required": skill in job.required_skills,
        })
    return chart_data
