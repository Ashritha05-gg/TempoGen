/* Resume_gen.jsx*/
import React, { useState, useRef } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

export default function Resume() {
  const [resumeText, setResumeText] = useState("");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  /* ---------------- FILE UPLOAD ---------------- */
  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));

    try {
      await axios.post(`${API_BASE}/upload_files`, formData);
      alert("Files uploaded successfully. Now ask what to generate.");
    } catch (err) {
      alert("File upload failed");
      console.error(err);
    } finally {
      e.target.value = "";
    }
  };

  /* ---------------- SEND PROMPT ---------------- */
  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/resume/chat`, {
        prompt,
      });

      setResumeText(res.data.text);
      setPrompt("");
    } catch (err) {
      alert("Resume generation failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- DOWNLOAD PDF ---------------- */
  const downloadResume = async () => {
    if (!resumeText) {
      alert("No resume to download");
      return;
    }

    try {
      const res = await axios.post(
        `${API_BASE}/resume/pdf`,
        { text: resumeText },
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "resume.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("PDF download failed");
      console.error(err);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        height: "calc(100vh - 64px)",
        background: "#f5f6f8",
      }}
    >
      {/* ================= LEFT : EDITABLE PREVIEW ================= */}
      <div
        style={{
          flex: 1,
          padding: "24px",
          overflowY: "auto",
        }}
      >
        <div
          style={{
            background: "#f8fafc",
            borderRadius: "12px",
            padding: "24px",
            minHeight: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* HEADER */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "12px",
            }}
          >
            <h2>Editable Resume Preview</h2>

            <button
              onClick={downloadResume}
              disabled={!resumeText}
              style={{
                padding: "8px 14px",
                borderRadius: "8px",
                background: resumeText ? "#16a34a" : "#9ca3af",
                color: "#ffffff",
                border: "none",
                cursor: resumeText ? "pointer" : "not-allowed",
              }}
            >
              ⬇ Download PDF
            </button>
          </div>

          {/* EDITABLE TEXTAREA */}
          {resumeText ? (
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              style={{
                flex: 1,
                resize: "none",
                border: "1px solid #d1d5db",
                borderRadius: "8px",
                padding: "14px",
                fontSize: "15px",
                lineHeight: "1.6",
                fontFamily: "inherit",
              }}
            />
          ) : (
            <p style={{ color: "#6b7280" }}>
              Upload your resume files and ask the assistant what to generate.
            </p>
          )}
        </div>
      </div>

      {/* ================= RIGHT : CHAT / UPLOAD ================= */}
      <div
        style={{
          flex: 1,
          padding: "24px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            background: "#ffffff",
            borderRadius: "12px",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            height: "100%",
          }}
        >
          <h3 style={{ marginBottom: "12px" }}>Resume Assistant</h3>

          {/* Upload */}
          <div
            style={{
              background: "#e5e7eb",
              padding: "12px",
              borderRadius: "8px",
              marginBottom: "12px",
              cursor: "pointer",
            }}
            onClick={() => fileInputRef.current.click()}
          >
            📎 Upload resume files (PDF / DOCX)
          </div>

          <input
            ref={fileInputRef}
            type="file"
            multiple
            hidden
            accept=".pdf,.doc,.docx"
            onChange={handleFileUpload}
          />

          {/* Prompt */}
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Tell me what resume to generate..."
            style={{
              flex: 1,
              resize: "none",
              padding: "14px",
              borderRadius: "10px",
              border: "1px solid #d1d5db",
              fontSize: "14px",
              marginBottom: "12px",
            }}
          />

          <button
            onClick={sendPrompt}
            disabled={loading}
            style={{
              padding: "12px",
              borderRadius: "10px",
              background: "#2563eb",
              color: "#ffffff",
              border: "none",
              fontSize: "15px",
              cursor: "pointer",
            }}
          >
            {loading ? "Generating..." : "Generate Resume"}
          </button>
        </div>
      </div>
    </div>
  );
}