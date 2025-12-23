

// src/components/Preview.jsx
import React from "react";
import ReactMarkdown from "react-markdown";

export default function Preview({ sections }) {
  if (!Array.isArray(sections)) {
    return <p style={{ color: "red" }}>Invalid document structure</p>;
  }

  if (sections.length === 0) {
    return (
      <div className="doc-page doc-page-empty">
        <p>
          Start by uploading your files and telling the assistant what to
          generate.
        </p>
      </div>
    );
  }

  return (
    <div className="doc-scroll">
      <div className="doc-page">
        {sections.map((sec, i) => (
          <div key={i} style={{ marginBottom: 32 }}>
            {/* SECTION HEADING */}
            <h2 className="doc-heading">{sec.section}</h2>

            {/* MARKDOWN CONTENT (FIXED) */}
            {sec.content && (
              <div className="doc-paragraph">
                <ReactMarkdown>
                  {sec.content}
                </ReactMarkdown>
              </div>
            )}

            {/* IMAGES */}
            {Array.isArray(sec.images) &&
              sec.images.map((img, idx) => (
                <div key={idx} style={{ marginTop: 12 }}>
                  <img
                    src={img.url}
                    alt={img.name}
                    style={{
                      maxWidth: "100%",
                      borderRadius: 8,
                      border: "1px solid #e5e7eb",
                    }}
                  />
                  <p style={{ fontSize: 12, color: "#6b7280" }}>
                    {img.name}
                  </p>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}


