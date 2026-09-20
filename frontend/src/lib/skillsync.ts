import { api } from "./api";
import type { JobRequirements, RankingResponse, ExplainResponse } from "../types/api";

export async function signup(email: string, password: string, fullName?: string) {
  const res = await api.post("/auth/signup", { email, password, full_name: fullName || null });
  return res.data;
}

export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);
  const res = await api.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
}

export async function parseJobDescription(text: string): Promise<JobRequirements> {
  const res = await api.post("/jobs/parse", { text });
  return res.data.job_requirements;
}

export async function uploadResume(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/resumes/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function rankCandidates(jobId: string, candidateIds: string[]): Promise<RankingResponse> {
  const res = await api.post(`/rank/${jobId}`, { candidate_ids: candidateIds });
  return res.data;
}

export async function explainCandidate(candidateId: string, jobId: string): Promise<ExplainResponse> {
  const res = await api.get(`/candidates/${candidateId}/explain/${jobId}`);
  return res.data;
}

export async function submitFeedback(jobId: string, candidateId: string, label: 0 | 1) {
  const res = await api.post("/feedback/", { job_id: jobId, candidate_id: candidateId, label });
  return res.data;
}
