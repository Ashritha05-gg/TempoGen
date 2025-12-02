export default function Preview({ sections }) {
  // ✅ Safety guard
  if (!Array.isArray(sections)) {
    console.error("Preview received invalid sections:", sections);
    return (
      <p style={{ color: "#ef4444" }}>
        Internal error: document structure is invalid.
      </p>
    );
  }

  if (sections.length === 0) {
    return (
      <p style={{ color: "#64748b" }}>
        Start by giving instructions to generate the document.
      </p>
    );
  }

  return (
    <div style={{ overflowY: "auto", height: "100%" }}>
      {sections.map((sec, i) => (
        <div key={i} style={{ marginBottom: 24 }}>
          <h2>{sec.section}</h2>
          <p style={{ whiteSpace: "pre-wrap" }}>{sec.content}</p>
        </div>
      ))}
    </div>
  );
}
