
import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <div className="navbar">
      <div style={{ fontWeight: 700 }}>TempOGen</div>

      <div style={{ marginLeft: "auto", display: "flex", gap: 16 }}>
        <Link to="/" style={{ textDecoration: "none", color: "#111" }}>
          Home
        </Link>
        <Link to="/about" style={{ textDecoration: "none", color: "#111" }}>
          About Us
        </Link>
        <Link to="/resume" style={{ textDecoration: "none", color: "#111" }}>Resume</Link>
        <Link to="/templates" style={{ textDecoration: "none", color: "#111" }}>
          Templates
        </Link>
      </div>
    </div>
  );
}
