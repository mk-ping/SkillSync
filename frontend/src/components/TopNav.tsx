import React from "react";

interface StatCardProps {
  label: string;
  value: string;
  accent: "mint" | "violet" | "rose";
}

const accentMap = {
  mint: { bg: "bg-mint/10", border: "border-mint/25", text: "text-mint" },
  violet: { bg: "bg-violet/10", border: "border-violet/25", text: "text-violet" },
  rose: { bg: "bg-rose/10", border: "border-rose/25", text: "text-rose" },
};

export function StatCard({ label, value, accent }: StatCardProps) {
  const a = accentMap[accent];
  return (
    <div className={`${a.bg} ${a.border} border rounded-lg px-4 py-2 text-center`}>
      <div className={`font-mono font-medium text-lg ${a.text}`}>{value}</div>
      <div className="text-[10px] text-textMuted mt-0.5">{label}</div>
    </div>
  );
}

export function TopNav() {
  return (
    <div className="flex justify-between items-start mb-5">
      <div>
        <div className="font-heading font-bold text-xl text-textPrimary tracking-tight">
          SkillSync
        </div>
        <div className="text-xs text-textMuted mt-1">
          Senior ML Engineer &mdash; 482 candidates ranked
        </div>
      </div>
      <div className="flex gap-2.5">
        <StatCard label="strong match" value="73" accent="mint" />
        <StatCard label="avg match" value="68%" accent="violet" />
        <StatCard label="top gap" value="AWS" accent="rose" />
      </div>
    </div>
  );
}
