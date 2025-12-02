import { useState, useRef } from "react";
import axios from "axios";

export default function Chat({ setDocumentContent }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const sessionId = "test1";

  const fileInputRef = useRef(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Show user message
    setMessages(prev => [...prev, { role: "user", text: input }]);
    setInput("");

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("prompt", input);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", formData);

      // Update document preview
      setDocumentContent(prev => prev + "\n\n" + res.data.response);

      // Friendly AI response
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "✅ I’ve updated the document based on your request." }
      ]);

    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "⚠️ Something went wrong." }
      ]);
    }
  };

  const handleFileUpload = async (e) => {
    const files = e.target.files;
    if (!files.length) return;

    setUploading(true);

    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }

    try {
      await axios.post("http://127.0.0.1:8000/upload_files", formData);

      setMessages(prev => [
        ...prev,
        {
          role: "ai",
          text: `📎 ${files.length} file(s) uploaded successfully. You can now ask questions.`
        }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "⚠️ File upload failed." }
      ]);
    }

    setUploading(false);
    e.target.value = null;
  };

  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
      
      {/* Chat messages */}
      <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: "10px",
              textAlign: msg.role === "user" ? "right" : "left"
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "10px 14px",
                borderRadius: "12px",
                background: msg.role === "user" ? "#2563eb" : "#e5e7eb",
                color: msg.role === "user" ? "white" : "black",
                maxWidth: "75%"
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      {/* Input bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          padding: "15px",
          borderTop: "1px solid #ddd",
          gap: "10px"
        }}
      >
        {/* Attachment icon */}
        <span
          style={{
            fontSize: "20px",
            cursor: "pointer"
          }}
          onClick={() => fileInputRef.current.click()}
          title="Attach files"
        >
          📎
        </span>

        <input
          type="file"
          multiple
          ref={fileInputRef}
          onChange={handleFileUpload}
          style={{ display: "none" }}
          accept=".pdf,.docx,.ppt,.pptx,.xls,.xlsx"
        />

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={uploading ? "Uploading files..." : "Type a request..."}
          disabled={uploading}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc"
          }}
        />

        <button
          onClick={sendMessage}
          disabled={uploading}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            background: "#2563eb",
            color: "white",
            border: "none"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
