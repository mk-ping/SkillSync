import React from "react";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell } from "recharts";

const data = [
  { stage: "Applied", count: 482 },
  { stage: "Screened", count: 210 },
  { stage: "Interviewed", count: 64 },
  { stage: "Offered", count: 12 },
];

const colors = ["#A78BFA", "#8B7CF6", "#5EEAD4", "#2DD4BF"];

export function FunnelChart() {
  return (
    <div className="glass-panel p-4 flex-1">
      <div className="font-heading font-bold text-xs text-textPrimary mb-2.5">
        hiring funnel
      </div>
      <ResponsiveContainer width="100%" height={190}>
        <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
          <XAxis type="number" tick={{ fill: "#8A8A93", fontSize: 10 }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="stage" tick={{ fill: "#D4D4D8", fontSize: 11 }} axisLine={false} tickLine={false} width={80} />
          <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={22}>
            {data.map((_, i) => (
              <Cell key={i} fill={colors[i]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
