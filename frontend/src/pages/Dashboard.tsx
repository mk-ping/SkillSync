import React, { useEffect, useState } from "react";
import { ThumbsUp, ThumbsDown, Check } from "lucide-react";
import { rankCandidates, submitFeedback } from "../lib/skillsync";
import type { RankingResponse } from "../types/api";

interface DashboardProps {
  jobId: string;
  candidateIds: string[];
}

export default function Dashboard({ jobId, candidateIds }: DashboardProps) {
  const [data, setData] = useState<RankingResponse | null>(null);
  const [error, setError] = useState("");
  const [labeled, setLabeled] = useState<Record<string, 0 | 1>>({});
  const [labelCount, setLabelCount] = useState<number | null>(null);

  useEffect(() => {
    rankCandidates(jobId, candidateIds)
      .then(setData)
      .catch((err) => {
        console.error(err);
        setError("Failed to fetch rankings. Is the backend running?");
      });
  }, [jobId, candidateIds]);

  async function handleFeedback(candidateId: string, label: 0 | 1) {
    try {
      const result = await submitFeedback(jobId, candidateId, label);
      setLabeled((prev) => ({ ...prev, [candidateId]: label }));
      setLabelCount(result.total_labels_collected);
    } catch (err) {
      console.error(err);
    }
  }

  if (error) {
    return <div className="min-h-screen bg-bg text-rose flex items-center justify-center">{error}</div>;
  }

  if (!data) {
    return <div className="min-h-screen bg-bg text-textMuted flex items-center justify-center">Loading rankings...</div>;
  }

  return (
    <div className="min-h-screen bg-bg p-6">
      <div className="max-w-5xl mx-auto">
        <div className="font-heading font-bold text-xl text-textPrimary mb-1">SkillSync</div>
        <div className="text-xs text-textMuted mb-1">
          {data.job_title || "Untitled role"} &mdash; {data.total_candidates} candidates ranked
        </div>
        {labelCount !== null && (
          <div className="text-xs text-mint mb-4">
            {labelCount} labels collected {labelCount < 15 && `(need ~15-20 with a mix of good/bad to train)`}
          </div>
        )}

        <div className="glass-panel p-4">
          <div className="flex justify-between items-center mb-3">
            <div className="font-heading font-bold text-xs text-textPrimary">
              ranked candidates
            </div>
            <div className="text-[10px] text-textMuted">
              Rate each match to help train the ranking model
            </div>
          </div>
          <div className="flex flex-col gap-3">
            {data.ranked_candidates.map((c) => (
              <div key={c.candidate_id} className="flex items-center gap-3">
                <span className="w-32 text-xs text-textPrimary truncate">
                  {c.candidate_name || c.candidate_id.slice(0, 8)}
                </span>
                <div className="flex-1 h-6 bg-white/5 rounded-md overflow-hidden">
                  <div
                    className="h-full bg-mint flex items-center justify-end px-2"
                    style={{ width: `${c.final_score}%` }}
                  >
                    <span className="font-mono font-bold text-[11px] text-bg">
                      {c.final_score}%
                    </span>
                  </div>
                </div>
                <div className="flex gap-1.5 items-center w-20 justify-end">
                  {labeled[c.candidate_id] !== undefined ? (
                    <div className="flex items-center gap-1 text-[10px] text-mint">
                      <Check size={12} />
                      {labeled[c.candidate_id] === 1 ? "Good fit" : "Not a fit"}
                    </div>
                  ) : (
                    <>
                      <button
                        onClick={() => handleFeedback(c.candidate_id, 1)}
                        className="w-7 h-7 rounded-md bg-mint/10 hover:bg-mint/20 flex items-center justify-center text-mint"
                        title="Good match"
                      >
                        <ThumbsUp size={13} />
                      </button>
                      <button
                        onClick={() => handleFeedback(c.candidate_id, 0)}
                        className="w-7 h-7 rounded-md bg-rose/10 hover:bg-rose/20 flex items-center justify-center text-rose"
                        title="Not a good match"
                      >
                        <ThumbsDown size={13} />
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
