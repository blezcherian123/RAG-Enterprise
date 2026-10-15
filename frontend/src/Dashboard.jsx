import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Dashboard.css";

import NavBar from "./components/NavBar";
import ChatBot from "./components/ChatBot";

/**
 * Dashboard Page - Appears after user sign-in
 * Shows 4 role-based navigation buttons:
 * - HR
 * - Employee
 * - Finance Employee
 * - C level employees
 *
 * The buttons are color-coded and styled based on typical role associations,
 * and each navigates to a relevant section/page.
 */
function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // Parse JWT token from localStorage to determine user role
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      setError("No authentication token found");
      navigate("/login");
      return;
    }

    try {
      // Decode the JWT token payload without verification for role detection
      // In production, verify the token signature for security
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser(payload);
      setError(""); // Clear any previous error
    } catch (error) {
      console.error("Failed to decode authentication token", error);
      setUser(null);
      setError("Invalid or expired authentication token. Please log in again.");
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  // Determine user role from token payload
  const getUserRole = () => {
    if (!user) return "guest";

    const role = (user.role || user.role_name || user.type || "").toLowerCase();
    if (role.includes("hr") || role.includes("human resources")) return "hr";
    if (role.includes("c-level") || role.includes("ceo") || role.includes("cfo") || role.includes("cto") || role.includes("executive")) return "c_level";
    if (role.includes("finance")) return "finance";
    return "employee";
  };

  const role = getUserRole();

  const [showChat, setShowChat] = useState(false);
  const [chatRole, setChatRole] = useState("");

  // Navigate based on button clicked (optional)
  const handleButtonClick = (targetRole) => {
    // Open chatbot for the selected role
    setChatRole(targetRole);
    setShowChat(true);
    // If you still want navigation, uncomment the line below
    // navigate(`/${targetRole.toLowerCase()}`);
  };

  if (loading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  // Show error state if token decoding failed
  if (error && !user) {
    return (
      <div className="error-state">
        <h3>Authentication Error</h3>
        <p>{error}</p>
        <button
          className="btn btn-hr"
          onClick={() => navigate("/login")}
          style={{ marginTop: "1rem" }}
        >
          Go to Login
        </button>
      </div>
    );
  }

  // If no user, redirect to login
  if (!user) {
    navigate("/login");
    return null;
  }

  return (
    <div className="dashboard-container glass-card">
  <NavBar />
      <header className="dashboard-header">
        <h1>Welcome back!</h1>
        <p>Homeegram - Intelligent enterprise knowledge management</p>
      </header>

      <main className="dashboard-content">
        <p className="user-role">Role: {role.toUpperCase()}</p>

        <div className="button-vertical">
          {/* HR Button - Green for HR/People operations */}
          <button
            className="btn btn-hr"
            onClick={() => handleButtonClick("HR")}
            aria-label="HR Dashboard"
            title="HR Department"
          >
            <span>HR</span>
          </button>

          {/* Employee Button - Blue for general employees */}
          <button
            className="btn btn-employee"
            onClick={() => handleButtonClick("Employee")}
            aria-label="Employee Dashboard"
            title="Employee Self-Service"
          >
            <span>Employee</span>
          </button>

          {/* Finance Employee Button - Orange/Teal for finance */}
          <button
            className="btn btn-finance"
            onClick={() => handleButtonClick("Finance Employee")}
            aria-label="Finance Employee Dashboard"
            title="Finance Department"
          >
            <span>Finance<br/>Employee</span>
          </button>

          {/* C Level Button - Purple for executives */}
          <button
            className="btn btn-c-level"
            onClick={() => handleButtonClick("C Level")}
            aria-label="C-Level Executive Dashboard"
            title="Executive Leadership"
          >
            <span>C Level<br/>Employees</span>
          </button>
        </div>
        {showChat && (
          <ChatBot role={chatRole} onClose={() => setShowChat(false)} />
        )}
      </main>
    </div>
  );
}

export default Dashboard;