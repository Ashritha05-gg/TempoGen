import React from "react";
import RichEditor from "./RichEditor";

export default function Preview({ sections, onUpdateSection }) {
  if (!Array.isArray(sections)) return null;

  if (sections.length === 0) {
    return (
      <div className="doc-page doc-page-empty">
        <p>Start by uploading files and generating content.</p>
      </div>
    );
  }

  return (
    <div className="doc-scroll">
      <div className="doc-page">
        {sections.map((sec, i) => (
          <div key={i} style={{ marginBottom: 32 }}>

            {/* Section Heading */}
            <h2 className="doc-heading">{sec.section}</h2>

            {/* Editable content */}
            <RichEditor
              content={sec.content || ""}
              onChange={(html) => onUpdateSection(i, html)}
            />

            {/* IMAGE RENDERING (ADD THIS) */}
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





