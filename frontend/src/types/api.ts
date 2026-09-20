export interface ScoreBreakdown {
  semantic_similarity: number;
  skill_match: number;
  experience_match: number;
}

export interface RankedCandidate {
  candidate_id: string;
  candidate_name: string | null;
  final_score: number;
  breakdown: ScoreBreakdown;
  matched_required_skills: string[];
  matched_preferred_skills: string[];
  missing_required_skills: string[];
  missing_preferred_skills: string[];
}

export interface RankingResponse {
  job_id: string;
  job_title: string | null;
  total_candidates: number;
  ranked_candidates: RankedCandidate[];
}

export interface JobRequirements {
  job_id: string;
  title: string | null;
  required_skills: string[];
  preferred_skills: string[];
  min_years_experience: number | null;
  education_requirement: string | null;
}

export interface SkillGapItem {
  skill: string;
  coverage: number;
  required: boolean;
}

export interface ExplainResponse {
  candidate_id: string;
  job_id: string;
  score_result: RankedCandidate;
  explanation: {
    summary: string;
    strengths: string[];
    concerns: string[];
  };
  skill_gap_chart: SkillGapItem[];
}
