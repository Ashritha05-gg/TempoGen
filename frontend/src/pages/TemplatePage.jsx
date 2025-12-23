


import "./TemplatePage.css";
import academic from "../templates/academic";
import business from "../templates/business";
import resume from "../templates/resume";
import minimal from "../templates/minimal";

const templates = [
  academic,
  business,
  resume,
  minimal,
];

export default function TemplatePage({ onSelectTemplate }) {
  return (
    <div className="template-page">
      <h1>Select a Template</h1>
      <p className="template-subtitle">
        Choose a layout style for your generated document
      </p>

      <div className="template-grid">
        {templates.map((tpl) => (
          <div
            key={tpl.id}
            className="template-card"
            onClick={() => onSelectTemplate(tpl)}
          >
            <div className="template-preview">
              <h3>{tpl.name}</h3>
              <p style={{ fontFamily: tpl.font }}>
                Sample heading
              </p>
              <p
                style={{
                  fontFamily: tpl.font,
                  lineHeight: tpl.lineHeight,
                  fontSize: 13,
                }}
              >
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


