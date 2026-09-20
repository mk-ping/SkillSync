import React from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";

const data = [
  { week: "W1", applications: 40 },
  { week: "W2", applications: 65 },
  { week: "W3", applications: 58 },
  { week: "W4", applications: 90 },
  { week: "W5", applications: 112 },
  { week: "W6", applications: 148 },
];

export function TrendChart() {
  return (
    <div className="glass-panel p-4 mt-3.5">
      <div className="font-heading font-bold text-xs text-textPrimary mb-2.5">
        applications over time
      </div>
      <ResponsiveContainer width="100%" height={130}>
        <AreaChart data={data}>
          <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="week" tick={{ fill: "#8A8A93", fontSize: 10 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: "#8A8A93", fontSize: 10 }} axisLine={false} tickLine={false} />
          <Area type="monotone" dataKey="applications" stroke="#A78BFA" fill="#A78BFA" fillOpacity={0.1} strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
