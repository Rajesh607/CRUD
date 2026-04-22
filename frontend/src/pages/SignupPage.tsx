import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import client from "../api/client";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("analyst");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await client.post("/auth/signup", { email, password, role });
      navigate("/login");
    } catch {
      setError("Signup failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={onSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm space-y-4">
        <h1 className="text-2xl font-bold">Sign up</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input className="w-full border p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full border p-2" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <select className="w-full border p-2" value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="analyst">Analyst</option>
          <option value="admin">Admin</option>
        </select>
        <button className="w-full bg-slate-900 text-white p-2 rounded">Create Account</button>
        <p className="text-sm">Already have account? <Link to="/login" className="text-blue-600">Login</Link></p>
      </form>
    </div>
  );
}
