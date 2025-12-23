

import React, { useRef, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

export default function ChatPanel({ sessionId, onUpdateDocument }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Upload files or images and tell me what you want to generate." },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadedImages, setUploadedImages] = useState([]);

  const fileInputRef = useRef(null);
  const bottomRef = useRef(null);

  const scrollToBottom = () =>
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });

  const handleAttachClick = () => fileInputRef.current?.click();

  // ---------- FILE UPLOAD ----------
  const handleFilesSelected = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));

    const images = files.filter((f) => f.type.startsWith("image/"));
    const imageObjs = images.map((img) => ({
      name: img.name,
      url: URL.createObjectURL(img),
    }));
    setUploadedImages((prev) => [...prev, ...imageObjs]);

    setMessages((p) => [...p, { role: "ai", text: "⬆ Uploading files..." }]);

    try {
      await axios.post(`${API_BASE}/upload_files`, formData);
      setMessages((p) => [
        ...p,
        {
          role: "ai",
          text:
            images.length > 0
              ? "✅ Files uploaded. Images can now be used in sections."
              : "✅ Files uploaded. Tell me what to generate.",
        },
      ]);
    } catch {
      setMessages((p) => [...p, { role: "ai", text: "❌ Upload failed." }]);
    } finally {
      e.target.value = "";
      scrollToBottom();
    }
  };

  // ---------- SEND PROMPT ----------
  const sendPrompt = async () => {
    if (!input.trim()) return;

    const prompt = input.trim();
    setInput("");

    setMessages((p) => [...p, { role: "user", text: prompt }]);
    scrollToBottom();

    // 🖼 IMAGE COMMAND (frontend only)
    const isImageCmd =
      prompt.toLowerCase().includes("add this image") ||
      prompt.toLowerCase().includes("use the uploaded image");

    if (isImageCmd && uploadedImages.length > 0) {
      onUpdateDocument((prev) =>
        prev.map((sec) => ({
          ...sec,
          images: [...(sec.images || []), ...uploadedImages],
        }))
      );

      setMessages((p) => [...p, { role: "ai", text: "🖼 Image added to section." }]);
      return;
    }

    // ---------- TEXT GENERATION ----------
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        session_id: sessionId,
        prompt,
      });

      const rawText = res.data.response || "";

      /**
       * 🔥 SPLIT MARKDOWN INTO SECTIONS
       * Matches:
       * **Heading**
       * content...
       */
      const sectionRegex = /\*\*(.*?)\*\*\n([\s\S]*?)(?=\n\*\*|$)/g;
      const newSections = [];
      let match;

      while ((match = sectionRegex.exec(rawText)) !== null) {
        newSections.push({
          section: match[1].trim(),
          content: match[2].trim(),
        });
      }

      // Fallback if Gemini returned plain text
      if (newSections.length === 0) {
        newSections.push({
          section: "Generated Content",
          content: rawText.trim(),
        });
      }

      onUpdateDocument((prev) => [
        ...(Array.isArray(prev) ? prev : []),
        ...newSections,
      ]);

      setMessages((p) => [...p, { role: "ai", text: "✅ Document updated." }]);
    } catch (e) {
      setMessages((p) => [...p, { role: "ai", text: "❌ Generation failed." }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  return (
    <div className="card chat-card">
      <h3 className="chat-title">Template Assistant</h3>

      <div className="chat-body">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            {m.text}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <button className="chat-attach-btn" onClick={handleAttachClick}>📎</button>

        <input
          ref={fileInputRef}
          type="file"
          multiple
          hidden
          accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.png,.jpg,.jpeg,.csv,.mp3,.wav,.m4a"
          onChange={handleFilesSelected}
        />

        <textarea
          className="chat-input"
          placeholder="Tell me what to add..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendPrompt()}
          rows={1}
        />

        <button className="chat-send-btn" onClick={sendPrompt}>➤</button>
      </div>
    </div>
  );
}
