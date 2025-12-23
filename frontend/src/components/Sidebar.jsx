// src/components/Sidebar.jsx
import React from "react";

export default function Sidebar({
  open,
  onToggle,
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
}) {
  return (
    <aside className={`sidebar ${open ? "sidebar-open" : "sidebar-collapsed"}`}>
      <div className="sidebar-top">
        <button className="sidebar-toggle" onClick={onToggle}>
          {/* simple double-rectangle toggle icon like ChatGPT */}
          <span className="sidebar-toggle-icon" />
        </button>
        {open && <span className="sidebar-title">Chats</span>}
      </div>

      <button className="sidebar-newchat" onClick={onNewChat}>
        {open ? "+ New document" : "+"}
      </button>

      <div className="sidebar-list">
        {sessions.length === 0 && open && (
          <div className="sidebar-empty">No documents yet.</div>
        )}

        {sessions.map((s) => (
          <button
            key={s.id}
            className={
              "sidebar-item" +
              (s.id === activeSessionId ? " sidebar-item-active" : "")
            }
            onClick={() => onSelectSession(s.id)}
          >
            {open ? s.title : s.title.charAt(0).toUpperCase()}
          </button>
        ))}
      </div>
    </aside>
  );
}
