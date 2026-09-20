import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  MessageSquareText,
  Target,
  FileText,
  Upload,
  ListOrdered,
  ArrowRight,
} from "lucide-react";

const faqs = [
  {
    q: "What happens if a candidate's resume uses different words than my job description?",
    a: "SkillSync compares meaning, not just exact text. A resume that says \"reduced churn using predictive models\" will still register against a JD asking for \"experience with predictive modeling,\" even though the wording doesn't match.",
  },
  {
    q: "What goes into the final score?",
    a: "Three things, combined: how closely the resume's content aligns with the job description overall, how many required and preferred skills were found, and how the candidate's experience compares to what the role asks for. You can see all three separately, not just the final number.",
  },
  {
    q: "Which file types can I upload?",
    a: "PDF and DOCX resumes.",
  },
  {
    q: "Will this make hiring decisions for me?",
    a: "No. It orders your candidate pool and tells you why, so you know where to start. Who gets an interview or an offer is still your call.",
  },
  {
    q: "Can I see why one candidate ranked above another?",
    a: "Yes. Every candidate's page shows matched skills, missing skills, and an experience comparison against the role.",
  },
];

function Logo({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
      <rect width="32" height="32" rx="9" fill="#5EEAD4" />
      <path d="M11 20c0 2.2 2.2 4 5 4s5-1.8 5-4-2.2-3-5-3.6c-2.8-.6-5-1.4-5-3.4 0-2.2 2.2-4 5-4s5 1.8 5 4"
        stroke="#0A0A0C" strokeWidth="2.2" strokeLinecap="round" fill="none" />
    </svg>
  );
}

export default function LandingPage() {
  const navigate = useNavigate();
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-bg text-textPrimary">
      <nav className="flex justify-between items-center px-8 py-5 max-w-6xl mx-auto">
        <div className="flex items-center gap-2.5">
          <Logo />
          <div className="font-heading font-bold text-lg">SkillSync</div>
        </div>
        <div className="flex gap-3">
          <button onClick={() => navigate("/login")} className="text-sm text-textMuted hover:text-textPrimary px-4 py-2">
            Log in
          </button>
          <button onClick={() => navigate("/signup")} className="text-sm bg-mint text-bg font-semibold rounded-lg px-4 py-2">
            Try for free
          </button>
        </div>
      </nav>

      <section className="max-w-3xl mx-auto text-center pt-20 pb-10 px-6">
        <h1 className="font-heading font-bold text-5xl leading-tight mb-5">
          From resume pile to<br />ranked shortlist. In minutes.
        </h1>
        <p className="text-textMuted text-lg max-w-xl mx-auto mb-8">
          SkillSync reads every resume against your job description and hands
          back a scored, explained shortlist &mdash; no manual screening required.
        </p>
        <div className="flex justify-center gap-3">
          <button onClick={() => navigate("/signup")} className="flex items-center gap-2 bg-mint text-bg font-heading font-bold rounded-lg px-7 py-3 text-sm">
            Try for free <ArrowRight size={16} />
          </button>
          <button onClick={() => navigate("/signup")} className="border border-border text-textPrimary font-heading font-bold rounded-lg px-7 py-3 text-sm">
            See how it works
          </button>
        </div>
      </section>

      <section className="max-w-2xl mx-auto px-6 pb-14">
        <div className="flex items-center justify-center gap-3 text-textMuted text-xs">
          <div className="flex flex-col items-center gap-1.5">
            <div className="glass-panel w-11 h-11 flex items-center justify-center"><FileText size={18} className="text-mint" /></div>
            Job description
          </div>
          <ArrowRight size={16} className="text-textMuted/40" />
          <div className="flex flex-col items-center gap-1.5">
            <div className="glass-panel w-11 h-11 flex items-center justify-center"><Upload size={18} className="text-violet" /></div>
            Resumes
          </div>
          <ArrowRight size={16} className="text-textMuted/40" />
          <div className="flex flex-col items-center gap-1.5">
            <div className="glass-panel w-11 h-11 flex items-center justify-center"><Search size={18} className="text-mint" /></div>
            Match
          </div>
          <ArrowRight size={16} className="text-textMuted/40" />
          <div className="flex flex-col items-center gap-1.5">
            <div className="glass-panel w-11 h-11 flex items-center justify-center"><ListOrdered size={18} className="text-violet" /></div>
            Ranked list
          </div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-6 pb-20">
        <div className="glass-panel p-5">
          <div className="flex justify-between items-center mb-4">
            <div className="font-heading font-bold text-xs text-textMuted">SENIOR ML ENGINEER</div>
            <div className="text-xs text-textMuted">3 candidates</div>
          </div>
          <div className="flex flex-col gap-2.5">
            {[
              { name: "Sarah Khan", score: 94 },
              { name: "Arjun Mehta", score: 89 },
              { name: "Riya Sharma", score: 82 },
            ].map((c) => (
              <div key={c.name} className="flex items-center gap-3">
                <span className="w-24 text-xs">{c.name}</span>
                <div className="flex-1 h-6 bg-white/5 rounded-md overflow-hidden">
                  <div className="h-full bg-mint flex items-center justify-end px-2" style={{ width: `${c.score}%` }}>
                    <span className="font-mono font-bold text-[11px] text-bg">{c.score}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-6 pb-20">
        <div className="font-heading font-bold text-2xl mb-3">What SkillSync actually does</div>
        <p className="text-textMuted text-sm mb-4 leading-relaxed">
          You give it a job description and a stack of resumes. It figures out
          what the role actually needs &mdash; the required skills, how much
          experience it calls for &mdash; and checks every resume against that,
          reading for meaning rather than matching exact phrases.
        </p>
        <p className="text-textMuted text-sm leading-relaxed">
          What comes back isn't just a ranked list. Every candidate has a
          breakdown: what matched, what's missing, and how their background
          stacks up against the role.
        </p>
      </section>

      <section className="max-w-5xl mx-auto px-6 pb-20">
        <div className="grid grid-cols-2 gap-4">
          <div className="glass-panel p-6">
            <div className="w-9 h-9 rounded-lg bg-mint/10 flex items-center justify-center mb-3">
              <Target size={16} className="text-mint" />
            </div>
            <div className="font-heading font-bold text-sm mb-2">The same bar for every candidate</div>
            <div className="text-xs text-textMuted">Resume 1 and resume 150 get measured against the exact same criteria &mdash; nothing depends on which one you happened to read first.</div>
          </div>
          <div className="glass-panel p-6">
            <div className="w-9 h-9 rounded-lg bg-violet/10 flex items-center justify-center mb-3">
              <ArrowRight size={16} className="text-violet" />
            </div>
            <div className="font-heading font-bold text-sm mb-2">Minutes, not an afternoon</div>
            <div className="text-xs text-textMuted">Upload the whole pool at once and get your ranking back immediately. Spend the saved time on actual conversations.</div>
          </div>
          <div className="glass-panel p-6">
            <div className="w-9 h-9 rounded-lg bg-mint/10 flex items-center justify-center mb-3">
              <MessageSquareText size={16} className="text-mint" />
            </div>
            <div className="font-heading font-bold text-sm mb-2">A reason for every score</div>
            <div className="text-xs text-textMuted">No unexplained percentage. Every ranking comes with the matched skills, the gaps, and the experience comparison behind it.</div>
          </div>
          <div className="glass-panel p-6">
            <div className="w-9 h-9 rounded-lg bg-violet/10 flex items-center justify-center mb-3">
              <Search size={16} className="text-violet" />
            </div>
            <div className="font-heading font-bold text-sm mb-2">Walk into the interview already informed</div>
            <div className="text-xs text-textMuted">See a candidate's missing skills ahead of time, so the interview can actually probe them instead of discovering them.</div>
          </div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-6 pb-20">
        <div className="font-heading font-bold text-2xl mb-8 text-center">How it works</div>
        <div className="flex flex-col gap-6">
          {[
            { icon: FileText, title: "Paste the job description", desc: "SkillSync pulls out the required skills, preferred skills, and experience level on its own." },
            { icon: Upload, title: "Upload the resumes", desc: "PDF or DOCX, one or many at a time." },
            { icon: ListOrdered, title: "Read the ranking", desc: "Candidates sorted by fit, each with the reasoning behind their score." },
          ].map((step, i) => (
            <div key={i} className="flex gap-4 items-start">
              <div className="glass-panel w-11 h-11 flex items-center justify-center shrink-0">
                <step.icon size={18} className="text-mint" />
              </div>
              <div>
                <div className="font-heading font-bold text-sm mb-1">{step.title}</div>
                <div className="text-xs text-textMuted">{step.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="max-w-2xl mx-auto px-6 pb-24">
        <div className="font-heading font-bold text-2xl mb-6 text-center">Questions people actually ask</div>
        <div className="flex flex-col gap-2">
          {faqs.map((item, i) => (
            <div key={i} className="glass-panel px-5 py-4 cursor-pointer" onClick={() => setOpenFaq(openFaq === i ? null : i)}>
              <div className="flex justify-between items-center text-sm font-medium">
                {item.q}
                <span className="text-textMuted">{openFaq === i ? "\u2212" : "+"}</span>
              </div>
              {openFaq === i && <div className="text-xs text-textMuted mt-3 leading-relaxed">{item.a}</div>}
            </div>
          ))}
        </div>
      </section>

      <section className="max-w-2xl mx-auto px-6 pb-24 text-center">
        <div className="font-heading font-bold text-2xl mb-3">The right candidate is in there somewhere</div>
        <div className="text-textMuted text-sm mb-5">Let's find them faster than reading 200 resumes would.</div>
        <button onClick={() => navigate("/signup")} className="bg-mint text-bg font-heading font-bold rounded-lg px-8 py-3 text-sm">
          Try for free
        </button>
      </section>

      <footer className="border-t border-border py-8 text-center text-xs text-textMuted flex items-center justify-center gap-2">
        <Logo size={16} /> SkillSync
      </footer>
    </div>
  );
}
