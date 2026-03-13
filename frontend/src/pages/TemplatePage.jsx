import "./TemplatePage.css";
import academic from "../templates/academic";
import business from "../templates/business";
import minimal from "../templates/minimal";

const templates = [academic, business, minimal];

export default function TemplatePage() {

  const downloadWithTemplate = async (tpl) => {

    const html = localStorage.getItem("tg_download_html");

    if (!html) {
      alert("No document found");
      return;
    }

    const res = await fetch("http://localhost:8000/export_pdf_template", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        html,
        template: tpl,
      }),
    });

    if (!res.ok) {
      alert("Download failed");
      return;
    }

    const blob = await res.blob();
    window.open(URL.createObjectURL(blob));
  };

  return (
    <div className="template-page">
      <h1>Select a Template</h1>

      <div className="template-grid">
        {templates.map((tpl) => (
          <div
            key={tpl.id}
            className="template-card"
            onClick={() => downloadWithTemplate(tpl)}
          >
            <div className="template-preview">
              <h3>{tpl.name}</h3>

              <p style={{ fontFamily: tpl.font }}>
                Sample heading
              </p>

              <p style={{ lineHeight: tpl.lineHeight }}>
                Sample paragraph preview text...
              </p>
            </div>

            <div className="template-meta">
              <span>{tpl.font}</span>
              <span>Spacing {tpl.lineHeight}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
