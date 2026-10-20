import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";
import { apiUrl } from "./api";

const roleOptions = [
  { id: "hr", name: "People & HR", description: "Policies, hiring, benefits and people operations", icon: "✳", tone: "violet" },
  { id: "employee", name: "Employee", description: "Your workplace, tools and everyday questions", icon: "◉", tone: "blue" },
  { id: "finance", name: "Finance", description: "Expenses, budgets and financial guidance", icon: "◈", tone: "amber" },
  { id: "c_level", name: "Executive", description: "Company insights for leadership", icon: "⌁", tone: "mint" },
];

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [profileOpen, setProfileOpen] = useState(false);
  const signOutStarted = useRef(false);
  const profileRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login", { replace: true });
      return undefined;
    }
    let active = true;
    const headers = { Authorization: `Bearer ${token}` };
    fetch(apiUrl("/api/v1/users/me"), { headers }).then(async (profileResponse) => {
      if (profileResponse.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        navigate("/login", { replace: true });
        return;
      }
      if (!profileResponse.ok) throw new Error("We couldn’t load your workspace profile.");
      const profile = await profileResponse.json();
      if (active) {
        setUser(profile);
        localStorage.setItem("user", JSON.stringify(profile));
      }
    }).catch((error) => {
      if (active) setLoadError(error.message || "We couldn’t load your workspace.");
    });
    return () => { active = false; };
  }, [navigate]);

  useEffect(() => {
    if (!profileOpen) return undefined;
    const closeOnOutsideClick = (event) => {
      if (!profileRef.current?.contains(event.target)) setProfileOpen(false);
    };
    const closeOnEscape = (event) => { if (event.key === "Escape") setProfileOpen(false); };
    document.addEventListener("pointerdown", closeOnOutsideClick);
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("pointerdown", closeOnOutsideClick);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [profileOpen]);

  const signOut = (event) => {
    event?.preventDefault();
    event?.stopPropagation();
    if (signOutStarted.current) return;
    signOutStarted.current = true;
    const token = localStorage.getItem("token");
    setProfileOpen(false);
    if (token) {
      void fetch(apiUrl("/api/v1/auth/logout"), {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        keepalive: true,
      }).catch(() => {});
    }
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login", { replace: true });
  };

  if (!user) return <div className="dashboard-loading" role={loadError ? "alert" : "status"}><p>{loadError || "Loading your secure workspace…"}</p>{loadError && <><button onClick={() => window.location.reload()}>Try again</button><button onClick={signOut}>Sign out</button></>}</div>;

  const email = user.email || "your workspace";
  const displayName = user.full_name || email.split("@")[0];
  const displayRole = user.role === "c_level" ? "Executive" : user.role === "finance" ? "Finance" : user.role === "hr" ? "People & HR" : user.role === "admin" ? "Workspace admin" : "Employee";

  return (
    <div className="dashboard-shell">
      <header className="dashboard-topbar">
        <a className="brand-mark" href="/dashboard" aria-label="Homeegram home"><span className="brand-orbit">h</span><span>Homeegram</span></a>
        <div className="topbar-right">
          <span className="secure-label"><span /> Secure workspace</span>
          <div className="profile-menu-wrap" ref={profileRef}>
            <button className={`profile-button ${profileOpen ? "profile-button-open" : ""}`} onClick={() => setProfileOpen((open) => !open)} aria-expanded={profileOpen} aria-haspopup="menu" aria-label="Open profile menu"><span>{displayName.charAt(0).toUpperCase()}</span><i>⌄</i></button>
            {profileOpen && <div className="profile-menu" role="menu">
              <div className="profile-menu-heading"><span className="profile-avatar-large">{displayName.charAt(0).toUpperCase()}</span><span><strong>{displayName}</strong><small>{email}</small></span></div>
              <div className="profile-menu-meta"><span>Workspace role</span><strong>{displayRole}</strong></div>
              <button type="button" className="signout-button" role="menuitem" onClick={signOut}><span>↪</span> Sign out</button>
            </div>}
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <section className="welcome-block">
          <div className="eyebrow"><span className="eyebrow-line" /> YOUR WORKSPACE ASSISTANTS</div>
          <h1>Good to have you<br className="mobile-break" /> ❤<span className="title-period"></span></h1>
        </section>

        <section className="role-section" aria-labelledby="role-heading">
          <div className="section-heading"><div><h2 id="role-heading">Your assistants</h2><p>Choose a role to start a conversation</p></div><span className="access-pill"><span className="access-dot" /> 4 assistants available</span></div>
          <div className="role-grid">
            {roleOptions.map((option, index) => {
              return <button key={option.id} className={`role-card ${option.tone}`} style={{ "--card-index": index }} onClick={() => navigate(`/chat/${option.id}`)} aria-label={`Open ${option.name} assistant`}>
                <span className="role-card-top"><span className="role-icon">{option.icon}</span><span className="card-arrow">↗</span></span>
                <span className="role-card-copy"><strong>{option.name}</strong><span>{option.description}</span></span>
                <span className="role-card-bottom"><span>Start a conversation</span><span className="arrow-long">→</span></span>
              </button>;
            })}
          </div>
        </section>
        <footer className="dashboard-footer"><span>Explore all four role assistants</span><span className="footer-spark">✦</span><span>Company chat service coming soon</span></footer>
      </main>

    </div>
  );
}

export default Dashboard;
