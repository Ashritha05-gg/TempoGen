
// import { useEffect, useState } from "react";
// import Navbar from "./components/Navbar";
// import ChatPanel from "./components/ChatPanel";
// import Preview from "./components/preview";
// import Sidebar from "./components/Sidebar";
// import Landing from "./components/Landing";

// import "./App.css";

// function App() {
//   const [sessions, setSessions] = useState([]);
//   const [activeSessionId, setActiveSessionId] = useState(null);
//   const [documentsBySession, setDocumentsBySession] = useState({});
//   const [sidebarOpen, setSidebarOpen] = useState(true);
//   const [activeTemplate,setActiveTemplate] =useState(null);

//   // --------------------------------------------------
//   // restore from localStorage (ONCE)
//   // --------------------------------------------------
//   useEffect(() => {
//     try {
//       const storedSessions = JSON.parse(localStorage.getItem("tg_sessions"));
//       const storedDocs = JSON.parse(localStorage.getItem("tg_documents"));
//       const storedActive = localStorage.getItem("tg_active_session");

//       if (Array.isArray(storedSessions)) setSessions(storedSessions);
//       if (storedDocs) setDocumentsBySession(storedDocs);
//       if (storedActive) setActiveSessionId(storedActive);
//     } catch (err) {
//       console.warn("Failed to restore saved sessions");
//     }
//   }, []);

//   // --------------------------------------------------
//   // persist to localStorage
//   // --------------------------------------------------
//   useEffect(() => {
//     localStorage.setItem("tg_sessions", JSON.stringify(sessions));
//     localStorage.setItem("tg_documents", JSON.stringify(documentsBySession));

//     if (activeSessionId) {
//       localStorage.setItem("tg_active_session", activeSessionId);
//     } else {
//       localStorage.removeItem("tg_active_session");
//     }
//   }, [sessions, documentsBySession, activeSessionId]);

//   // --------------------------------------------------
//   // create new document / chat
//   // --------------------------------------------------
//   const handleNewChat = () => {
//     const id = String(Date.now());
//     const title = `Document ${sessions.length + 1}`;

//     setSessions((prev) => [...prev, { id, title }]);
//     setActiveSessionId(id);

//     setDocumentsBySession((prev) => ({
//       ...prev,
//       [id]: [],
//     }));
//   };

//   const handleSelectChat = (id) => {
//     setActiveSessionId(id);
//   };

//   // --------------------------------------------------
//   // update document for active session
//   // --------------------------------------------------
//   const handleUpdateDocumentForActive = (updater) => {
//     if (!activeSessionId) return;

//     setDocumentsBySession((prev) => {
//       const current = prev[activeSessionId] || [];
//       const next = typeof updater === "function" ? updater(current) : updater;

//       return {
//         ...prev,
//         [activeSessionId]: next,
//       };
//     });
//   };

//   const activeSections = activeSessionId
//     ? documentsBySession[activeSessionId] || []
//     : [];

//   // --------------------------------------------------
//   // download (unchanged for now)
//   // --------------------------------------------------
//   const handleDownload = async () => {
//   if (!activeSessionId) return;

//   const sections = documentsBySession[activeSessionId] || [];

//   const res = await fetch("http://localhost:8000/export_pdf", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ sections }),
//   });

//   const blob = await res.blob();
//   const url = window.URL.createObjectURL(blob);

//   window.open(url, "_blank");
// };


//   return (
//     <div className="app-root">
//       <Navbar />

//       <div className="app-shell">
//         {/* Sidebar ONLY when a document exists */}
//         {activeSessionId && (
//           <Sidebar
//             open={sidebarOpen}
//             onToggle={() => setSidebarOpen((o) => !o)}
//             sessions={sessions}
//             activeSessionId={activeSessionId}
//             onSelectSession={handleSelectChat}
//             onNewChat={handleNewChat}
//           />
//         )}

//         <main className="app-main">
//           {/* LANDING */}
          
//             {sessions.length === 0 ? (
//   <div className="landing-only">
//     <Landing onNewChat={handleNewChat} />
//   </div>
// ) : (
//   <div className="workspace">

//               {/* LEFT */}
//               <section className="workspace-left">
//                 <div className="workspace-left-header">
//                   <h2>Live Document Preview</h2>
//                   <button
//                     className="download-btn"
//                     onClick={handleDownload}
//                   >
//                     ⬇ Download / Print
//                   </button>
//                 </div>

//                 <div className="preview-wrapper">
//                   <Preview sections={activeSections} />
//                 </div>
//               </section>

//               {/* RIGHT */}
//               <section className="workspace-right">
//                 <ChatPanel
//                   sessionId={activeSessionId}
//                   onUpdateDocument={handleUpdateDocumentForActive}
//                 />
//               </section>
//             </div>
//           )}
//         </main>
//       </div>
//     </div>
//   );
// }

// export default App;


// src/App.js
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import ChatPanel from "./components/ChatPanel";
import Preview from "./components/preview";
import Sidebar from "./components/Sidebar";
import Landing from "./components/Landing";
import TemplatePage from "./pages/TemplatePage";

import "./App.css";

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [documentsBySession, setDocumentsBySession] = useState({});
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTemplate, setActiveTemplate] = useState("academic");

  /* -------------------- RESTORE -------------------- */
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

  /* -------------------- PERSIST -------------------- */
  useEffect(() => {
    localStorage.setItem("tg_sessions", JSON.stringify(sessions));
    localStorage.setItem("tg_documents", JSON.stringify(documentsBySession));

    if (activeSessionId)
      localStorage.setItem("tg_active_session", activeSessionId);

    if (activeTemplate)
      localStorage.setItem("tg_template", activeTemplate);
  }, [sessions, documentsBySession, activeSessionId, activeTemplate]);

  /* -------------------- NEW DOC -------------------- */
  const handleNewChat = () => {
    const id = String(Date.now());
    const title = `Document ${sessions.length + 1}`;

    setSessions((p) => [...p, { id, title }]);
    setActiveSessionId(id);
    setDocumentsBySession((p) => ({ ...p, [id]: [] }));
  };

  /* -------------------- UPDATE DOC -------------------- */
  const handleUpdateDocumentForActive = (updater) => {
    if (!activeSessionId) return;

    setDocumentsBySession((prev) => ({
      ...prev,
      [activeSessionId]:
        typeof updater === "function"
          ? updater(prev[activeSessionId] || [])
          : updater,
    }));
  };

  const activeSections = activeSessionId
    ? documentsBySession[activeSessionId] || []
    : [];

  /* -------------------- DOWNLOAD -------------------- */
  const handleDownload = async () => {
    if (!activeSessionId) return;

    const res = await fetch("http://localhost:8000/export_pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sections: activeSections,
        template: activeTemplate,
      }),
    });

    const blob = await res.blob();
    window.open(URL.createObjectURL(blob));
  };

  return (
    <Router>
      {/* NAVBAR – color comes ONLY from Navbar.css */}
      <Navbar />

      <Routes>
        {/* ================= MAIN APP ================= */}
        <Route
          path="/"
          element={
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
                    {/* LEFT */}
                    <section className="workspace-left">
                      <div className="workspace-left-header">
                        <h2>Live Document Preview</h2>
                        <button
                          className="download-btn"
                          onClick={handleDownload}
                        >
                          ⬇ Download / Print
                        </button>
                      </div>

                      <Preview
                        sections={activeSections}
                        template={activeTemplate}
                      />
                    </section>

                    {/* RIGHT */}
                    <section className="workspace-right">
                      <ChatPanel
                        sessionId={activeSessionId}
                        onUpdateDocument={handleUpdateDocumentForActive}
                      />
                    </section>
                  </div>
                )}
              </main>
            </div>
          }
        />

        {/* ================= TEMPLATES PAGE ================= */}
        <Route
          path="/templates"
          element={
            <TemplatePage
              activeTemplate={activeTemplate}
              onSelectTemplate={(tpl) => setActiveTemplate(tpl)}
            />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
