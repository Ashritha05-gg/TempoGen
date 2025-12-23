// src/components/Landing.jsx
import React from "react";

export default function Landing({ onNewChat }) {
  return (
    <div className="landing-container">
      <div className="landing-inner">
        <h1 className="landing-title">What can I help you generate today?</h1>
        <p className="landing-subtitle">
          Start a new document, upload your PDFs, PPTs, Excels, or DOCX files,
          and describe how you want the final report to look.
        </p>

        <button className="primary-btn landing-btn" onClick={onNewChat}>
          + New document
        </button>
      </div>
    </div>
  );
}
