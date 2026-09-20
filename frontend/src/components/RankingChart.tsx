import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell } from "recharts";

const data = [
  { name: "Candidate A", score: 94 },
  { name: "Candidate B", score: 89 },
  { name: "Candidate C", score: 82 },
  { name: "Candidate D", score: 61 },
];

export function RankingChart() {
  return (
    <div className="glass-panel p-4 flex-[1.3]">
      <div className="font-heading font-bold text-xs text-textPrimary mb-2.5">
        top ranked candidates
      </div>
      <ResponsiveContainer width="100%" height={190}>
        <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
          <CartesianGrid horizontal={false} stroke="rgba(255,255,255,0.06)" />
          <XAxis type="number" domain={[0, 100]} tick={{ fill: "#8A8A93", fontSize: 10 }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="name" tick={{ fill: "#D4D4D8", fontSize: 11 }} axisLine={false} tickLine={false} width={90} />
          <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={20}>
            {data.map((_, i) => (
              <Cell key={i} fill={i === 0 ? "#5EEAD4" : "#5EEAD4"} fillOpacity={i === 0 ? 1 : 0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
