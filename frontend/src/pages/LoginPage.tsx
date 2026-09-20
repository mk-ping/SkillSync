import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login as loginApi } from "../lib/skillsync";
import { useAuth } from "../lib/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await loginApi(email, password);
      login(data.access_token, {
        user_id: data.user_id,
        email: data.email,
        full_name: data.full_name,
      });
      navigate("/app");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center p-6">
      <form onSubmit={handleSubmit} className="glass-panel p-8 max-w-sm w-full">
        <div className="font-heading font-bold text-xl text-textPrimary mb-1">Log in</div>
        <div className="text-xs text-textMuted mb-6">Welcome back to SkillSync</div>

        <label className="text-xs text-textMuted mb-1 block">Email</label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full bg-white/5 border border-border rounded-lg p-2.5 text-sm text-textPrimary mb-4 outline-none focus:border-mint/50"
        />

        <label className="text-xs text-textMuted mb-1 block">Password</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-white/5 border border-border rounded-lg p-2.5 text-sm text-textPrimary mb-5 outline-none focus:border-mint/50"
        />

        {error && <div className="text-rose text-xs mb-4">{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-mint text-bg font-heading font-bold text-sm rounded-lg py-2.5 disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Log in"}
        </button>

        <div className="text-xs text-textMuted mt-4 text-center">
          Don't have an account? <Link to="/signup" className="text-mint">Sign up</Link>
        </div>
      </form>
    </div>
  );
}
