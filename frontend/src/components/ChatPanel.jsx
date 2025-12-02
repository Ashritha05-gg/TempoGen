import { useState } from "react";
import axios from "axios";

export default function ChatPanel({ onUpdateDocument }) {
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "Hi! I'm your AI assistant. Upload your files and tell me how you'd like to structure your output."
    }
  ]);
  const [input, setInput] = useState("");

  const sendPrompt = async () => {
    if (!input.trim()) return;

    const prompt = input;
    setMessages(prev => [...prev, { role: "user", text: prompt }]);
    setInput("");

    const form = new FormData();
    form.append("session_id", "test1");
    form.append("prompt", prompt);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        form
      );

      const generatedText = res.data.response;

      // ✅ Decide section name from prompt
      let sectionName = "Generated Content";
      const p = prompt.toLowerCase();

      if (p.includes("introduction")) sectionName = "Introduction";
      else if (p.includes("summary")) sectionName = "Executive Summary";
      else if (p.includes("method")) sectionName = "Methodology";
      else if (p.includes("result")) sectionName = "Results";
      else if (p.includes("conclusion")) sectionName = "Conclusion";

      // ✅ Always send ARRAY to App state
      onUpdateDocument(prevSections => {
        const safeSections = Array.isArray(prevSections) ? prevSections : [];

        return [
          ...safeSections.filter(s => s.section !== sectionName),
          {
            section: sectionName,
            content: generatedText
          }
        ];
      });

      setMessages(prev => [
        ...prev,
        { role: "ai", text: "✅ Document updated." }
      ]);

    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "❌ Failed to generate content." }
      ]);
    }
  };

  return (
    <div className="card chat-card">
      <h3>Template Assistant</h3>

      <div className="chat-body">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Example: Give a brief introduction..."
        />
        <button onClick={sendPrompt}>➤</button>
      </div>
    </div>
  );
}
