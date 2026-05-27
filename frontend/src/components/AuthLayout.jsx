import { Outlet, useLocation } from "react-router-dom";
import "../css/LoginPage.css";

function AuthLayout() {
  const { pathname } = useLocation();
  const mode = pathname.includes("/signup") ? "signup-mode" : "login-mode";

  return (
    <div className={`auth-container ${mode}`}>
      <div className="auth-branding">
        <h2>WELCOME TO</h2>
        <div className="logo">Company RAG</div>
        <p>Intelligent enterprise knowledge management system powered by RAG</p>
      </div>

      <div className="auth-form-container">
        <div className="auth-card">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default AuthLayout;
