import React from "react";

const candidates = ["A", "B", "C", "D", "E"];
const skills = ["Python", "SQL", "Docker", "AWS"];

const grid: Record<string, ("strong" | "partial" | "missing")[]> = {
  Python: ["strong", "strong", "partial", "strong", "missing"],
  SQL: ["strong", "partial", "strong", "missing", "partial"],
  Docker: ["partial", "missing", "partial", "strong", "missing"],
  AWS: ["missing", "partial", "missing", "missing", "missing"],
};

const colorMap = {
  strong: "bg-mint",
  partial: "bg-mintDeep",
  missing: "bg-rose/20",
};

export function SkillHeatmap() {
  return (
    <div className="glass-panel p-4 mt-3.5">
      <div className="font-heading font-bold text-xs text-textPrimary mb-3">
        skill coverage heatmap &mdash; top 5 candidates
      </div>
      <div className="grid" style={{ gridTemplateColumns: "70px repeat(5, 1fr)", gap: "3px" }}>
        <div></div>
        {candidates.map((c) => (
          <div key={c} className="text-center text-[10px] text-textMuted">{c}</div>
        ))}
        {skills.map((skill) => (
          <React.Fragment key={skill}>
            <div className="text-[10px] text-textMuted flex items-center">{skill}</div>
            {grid[skill].map((level, i) => (
              <div key={i} className={`h-[22px] rounded ${colorMap[level]}`}></div>
            ))}
          </React.Fragment>
        ))}
      </div>
      <div className="flex items-center gap-1.5 mt-2.5 text-[10px] text-textMuted">
        <span className="w-2.5 h-2.5 bg-mint rounded-sm"></span> strong
        <span className="w-2.5 h-2.5 bg-mintDeep rounded-sm ml-2"></span> partial
        <span className="w-2.5 h-2.5 bg-rose/20 rounded-sm ml-2"></span> missing
      </div>
    </div>
  );
}
