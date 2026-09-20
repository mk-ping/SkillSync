import React, { useState } from "react";
import { parseJobDescription, uploadResume } from "../lib/skillsync";

interface SetupPanelProps {
  onReady: (jobId: string, candidateIds: string[]) => void;
}

export function SetupPanel({ onReady }: SetupPanelProps) {
  const [jdText, setJdText] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  async function handleSubmit() {
    if (!jdText.trim() || !files || files.length === 0) {
      setStatus("Please provide a job description and at least one resume.");
      return;
    }
    setLoading(true);
    setStatus("Parsing job description...");
    try {
      const job = await parseJobDescription(jdText);

      setStatus(`Uploading ${files.length} resume(s)...`);
      const candidateIds: string[] = [];
      for (let i = 0; i < files.length; i++) {
        const result = await uploadResume(files[i]);
        candidateIds.push(result.resume_id);
      }

      setStatus("Ranking candidates...");
      onReady(job.job_id, candidateIds);
    } catch (err) {
      console.error(err);
      setStatus("Something went wrong. Check the console and make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center p-6">
      <div className="glass-panel p-8 max-w-lg w-full">
        <div className="font-heading font-bold text-xl text-textPrimary mb-1">
          SkillSync
        </div>
        <div className="text-xs text-textMuted mb-6">
          Paste a job description and upload resumes to get started
        </div>

        <label className="text-xs text-textMuted mb-1 block">Job description</label>
        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          rows={6}
          className="w-full bg-white/5 border border-border rounded-lg p-3 text-sm text-textPrimary mb-4 outline-none focus:border-mint/50"
          placeholder="Paste the job description here..."
        />

        <label className="text-xs text-textMuted mb-1 block">Resumes (PDF or DOCX)</label>
        <input
          type="file"
          multiple
          accept=".pdf,.docx"
          onChange={(e) => setFiles(e.target.files)}
          className="w-full text-xs text-textMuted mb-5 file:bg-mint/10 file:text-mint file:border-0 file:rounded-md file:px-3 file:py-1.5 file:mr-3 file:text-xs"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-mint text-bg font-heading font-bold text-sm rounded-lg py-2.5 disabled:opacity-50"
        >
          {loading ? "Working..." : "Rank Candidates"}
        </button>

        {status && <div className="text-xs text-textMuted mt-3">{status}</div>}
      </div>
    </div>
  );
}
