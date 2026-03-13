// src/App.jsx

import { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";

import Navbar from "./components/Navbar";
import ChatPanel from "./components/ChatPanel";
import Preview from "./components/Preview";
import Sidebar from "./components/Sidebar";
import Landing from "./components/Landing";
import AboutUs from "./pages/AboutUs";
import TemplatePage from "./pages/TemplatePage";

/* ⭐ Resume Feature Imports (ADDED) */
import Resume_gen from "./components/Resume_gen";
import Reusme_Template from "./components/Resume_Templates";
import Minimal_Resume from "./pages/Minimal_Resume";

import "./App.css";

/* ================= MAIN APP CONTENT ================= */

function AppContent() {
  const navigate = useNavigate();

  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [documentsBySession, setDocumentsBySession] = useState({});
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTemplate, setActiveTemplate] = useState("academic");

  const [showDownloadPopup, setShowDownloadPopup] = useState(false);

  /* ---------------- RESTORE ---------------- */
  useEffect(() => {
    try {
      const s = JSON.parse(localStorage.getItem("tg_sessions"));
      const d = JSON.parse(localStorage.getItem("tg_documents"));
      const a = localStorage.getItem("tg_active_session");
      const t = localStorage.getItem("tg_template");

      if (Array.isArray(s)) setSessions(s);
      if (d) setDocumentsBySession(d);
      if (a) setActiveSessionId(a);
      if (t) setActiveTemplate(t);
    } catch {}
  }, []);

  /* ---------------- PERSIST ---------------- */
  useEffect(() => {
    localStorage.setItem("tg_sessions", JSON.stringify(sessions));
    localStorage.setItem("tg_documents", JSON.stringify(documentsBySession));

    if (activeSessionId)
      localStorage.setItem("tg_active_session", activeSessionId);

    if (activeTemplate)
      localStorage.setItem("tg_template", activeTemplate);
  }, [sessions, documentsBySession, activeSessionId, activeTemplate]);

  /* ---------------- NEW DOCUMENT ---------------- */
  const handleNewChat = () => {
    const id = String(Date.now());
    const title = `Document ${sessions.length + 1}`;

    setSessions((p) => [...p, { id, title }]);
    setActiveSessionId(id);
    setDocumentsBySession((p) => ({ ...p, [id]: [] }));
  };

  /* ---------------- UPDATE SINGLE SECTION ---------------- */
  const handleUpdateSection = (index, newHtml) => {
    setDocumentsBySession((prev) => ({
      ...prev,
      [activeSessionId]: prev[activeSessionId].map((sec, i) =>
        i === index ? { ...sec, content: newHtml } : sec
      ),
    }));
  };

  const activeSections =
    activeSessionId && documentsBySession[activeSessionId]
      ? documentsBySession[activeSessionId]
      : [];

  /* ================= BUILD FULL HTML ================= */
  const getFullHtml = () =>
    activeSections
      .map(
        (sec) =>
          `<h2>${sec.section || ""}</h2>${sec.content || ""}`
      )
      .join("");

  /* ================= DEFAULT DOWNLOAD ================= */
  const downloadDefault = async () => {
    const fullHtml = getFullHtml();

    const res = await fetch("http://localhost:8000/export_pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ html: fullHtml }),
    });

    const blob = await res.blob();
    window.open(URL.createObjectURL(blob));

    setShowDownloadPopup(false);
  };

  /* ================= GO TO TEMPLATE PAGE ================= */
  const goToTemplates = () => {
    localStorage.setItem("tg_download_html", getFullHtml());
    navigate("/templates");
    setShowDownloadPopup(false);
  };

  /* ================= UI ================= */
  return (
    <div className="app-shell">
      {activeSessionId && (
        <Sidebar
          open={sidebarOpen}
          onToggle={() => setSidebarOpen((o) => !o)}
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={setActiveSessionId}
          onNewChat={handleNewChat}
        />
      )}

      <main className="app-main">
        {sessions.length === 0 ? (
          <div className="landing-only">
            <Landing onNewChat={handleNewChat} />
          </div>
        ) : (
          <div className="workspace">

            {/* ---------- LEFT: PREVIEW ---------- */}
            <section className="workspace-left">
              <div className="workspace-left-header">
                <h2>Live Document Preview</h2>

                <button
                  className="download-btn"
                  onClick={() => setShowDownloadPopup(true)}
                >
                  ⬇ Download / Print
                </button>
              </div>

              <Preview
                sections={activeSections}
                template={activeTemplate}
                onUpdateSection={handleUpdateSection}
              />
            </section>

            {/* ---------- RIGHT: CHAT ---------- */}
            <section className="workspace-right">
              <ChatPanel
                sessionId={activeSessionId}
                onUpdateDocument={(updater) =>
                  setDocumentsBySession((prev) => ({
                    ...prev,
                    [activeSessionId]:
                      typeof updater === "function"
                        ? updater(prev[activeSessionId] || [])
                        : updater,
                  }))
                }
              />
            </section>
          </div>
        )}
      </main>

      {/* ================= DOWNLOAD POPUP ================= */}
      {showDownloadPopup && (
        <div className="download-modal-overlay">
          <div className="download-modal">

            <h3>Download Options</h3>

            <button onClick={downloadDefault}>
              Download Current Version
            </button>

            <button onClick={goToTemplates}>
              Choose Template
            </button>

            <button onClick={() => setShowDownloadPopup(false)}>
              Cancel
            </button>

          </div>
        </div>
      )}
    </div>
  );
}

/* ================= ROUTER WRAPPER ================= */

export default function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route path="/" element={<AppContent />} />
        <Route path="/templates" element={<TemplatePage />} />

        {/* ⭐ Resume Feature Routes (ADDED) */}
        <Route path="/resume" element={<Resume_gen />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/resumeTemplate" element={<Reusme_Template />} />
        <Route path="/minimal" element={<Minimal_Resume />} />

      </Routes>
    </Router>
  );
}