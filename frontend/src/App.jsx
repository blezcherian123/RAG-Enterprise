import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AuthLayout from "./components/AuthLayout";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import Dashboard from "./Dashboard";
import "./App.css";
import { useState } from "react";

function App() {
  const [isAuthenticated] = useState(() => Boolean(localStorage.getItem("token")));

  if (!isAuthenticated) {
    return (
      <BrowserRouter>
        <Routes>
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    );
  }

  // User is authenticated, show dashboard
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/hr" element={<Dashboard />} />
        <Route path="/employee" element={<Dashboard />} />
        <Route path="/finance-employee" element={<Dashboard />} />
        <Route path="/c-level" element={<Dashboard />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
