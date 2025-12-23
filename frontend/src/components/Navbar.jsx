
// import "./Navbar.css";

// export default function Navbar() {
//   return (
//     <nav className="tg-navbar">
//       <div className="tg-nav-left">
//         <span className="tg-logo">🧪</span>
//         <b>TempOGen</b>
//       </div>

//       <div className="tg-nav-right">
//         <a className="tg-nav-item" href="#">Dashboard</a>
//         <a className="tg-nav-item" href="#">Templates</a>

//         <div className="tg-avatar">U</div>
//       </div>
//     </nav>
//   );
// }

// src/components/Navbar.jsx
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
        <Link to="/" style={{ textDecoration: "none", color: "#111" }}>
          About Us
        </Link>
        <Link to="/templates" style={{ textDecoration: "none", color: "#111" }}>
          Templates
        </Link>
      </div>
    </div>
  );
}
