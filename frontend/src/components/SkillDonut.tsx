import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const data = [
  { name: "Python", value: 30, color: "#5EEAD4" },
  { name: "ML", value: 25, color: "#2DD4BF" },
  { name: "Docker", value: 25, color: "#A78BFA" },
  { name: "AWS gap", value: 20, color: "#FB7185" },
];

export function SkillDonut() {
  return (
    <div className="glass-panel p-4 flex-1">
      <div className="font-heading font-bold text-xs text-textPrimary mb-2.5">
        skill coverage &mdash; candidate a
      </div>
      <ResponsiveContainer width="100%" height={190}>
        <PieChart>
          <Pie data={data} dataKey="value" innerRadius={55} outerRadius={80} stroke="#0A0A0C" strokeWidth={3}>
            {data.map((d, i) => (
              <Cell key={i} fill={d.color} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
