import React from "react";
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from "recharts";

const data = [
  { dimension: "Skills", value: 96 },
  { dimension: "Experience", value: 82 },
  { dimension: "Projects", value: 90 },
  { dimension: "Education", value: 75 },
  { dimension: "Communication", value: 70 },
];

export function RadarProfile() {
  return (
    <div className="glass-panel p-4 flex-1">
      <div className="font-heading font-bold text-xs text-textPrimary mb-2.5">
        candidate profile radar
      </div>
      <ResponsiveContainer width="100%" height={190}>
        <RadarChart data={data}>
          <PolarGrid stroke="rgba(255,255,255,0.08)" />
          <PolarAngleAxis dataKey="dimension" tick={{ fill: "#D4D4D8", fontSize: 10 }} />
          <Radar dataKey="value" stroke="#5EEAD4" fill="#5EEAD4" fillOpacity={0.12} strokeWidth={2} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
