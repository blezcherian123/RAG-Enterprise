import { NavLink } from "react-router-dom";
import "./NavBar.css";

function NavBar() {
  return (
    <nav className="navbar">
      <ul className="nav-list">
        <li><NavLink to="/hr" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>HR</NavLink></li>
        <li><NavLink to="/employee" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Employee</NavLink></li>
        <li><NavLink to="/finance-employee" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>Finance</NavLink></li>
        <li><NavLink to="/c-level" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>C‑Level</NavLink></li>
      </ul>
    </nav>
  );
}

export default NavBar;
