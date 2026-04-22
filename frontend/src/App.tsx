import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./contexts/AuthContext";
import CombinedResultPage from "./pages/CombinedResultPage";
import DashboardPage from "./pages/DashboardPage";
import HistoryPage from "./pages/HistoryPage";
import LoginPage from "./pages/LoginPage";
import RelationshipPage from "./pages/RelationshipPage";
import SignupPage from "./pages/SignupPage";
import SummaryPage from "./pages/SummaryPage";
import UploadPage from "./pages/UploadPage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/upload/:companyType" element={<UploadPage />} />
            <Route path="/summary/:companyId" element={<SummaryPage />} />
            <Route path="/relationship" element={<RelationshipPage />} />
            <Route path="/combined" element={<CombinedResultPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
