import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Layout() {
  const { logout, user } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-slate-900 text-white px-6 py-4 flex justify-between">
        <div className="flex gap-4">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/upload/company-a">Upload A</Link>
          <Link to="/upload/target">Upload Target</Link>
          <Link to="/history">History</Link>
        </div>
        <div className="flex gap-3">
          <span>{user?.email}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </nav>
      <main className="max-w-6xl mx-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}
