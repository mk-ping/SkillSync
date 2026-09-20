import React, { useState } from "react";
import { SetupPanel } from "../components/SetupPanel";
import Dashboard from "./Dashboard";
import { useAuth } from "../lib/auth";

export default function AppShell() {
  const [session, setSession] = useState<{ jobId: string; candidateIds: string[] } | null>(null);
  const { user, logout } = useAuth();

  return (
    <div>
      <div className="flex justify-end items-center gap-3 px-6 py-3 text-xs text-textMuted">
        <span>{user?.email}</span>
        <button onClick={logout} className="text-rose hover:underline">Log out</button>
      </div>
      {!session ? (
        <SetupPanel onReady={(jobId, candidateIds) => setSession({ jobId, candidateIds })} />
      ) : (
        <Dashboard jobId={session.jobId} candidateIds={session.candidateIds} />
      )}
    </div>
  );
}
