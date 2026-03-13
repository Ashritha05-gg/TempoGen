# resume_pdf_template.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4


def clean_text(text: str) -> str:
    return text.replace("[", "").replace("]", "").strip()


def build_resume_pdf(sections: dict, buffer):
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    # ---------- STYLES (MATCH IMAGE) ----------

    name_style = ParagraphStyle(
        "NameStyle",
        fontName="Times-Bold",
        fontSize=18,
        alignment=1,      # CENTER
        spaceAfter=12,    # ⬅ more space after name
    )

    contact_style = ParagraphStyle(
        "ContactStyle",
        fontName="Times-Roman",
        fontSize=10,
        alignment=1,      # CENTER
        spaceAfter=22,    # ⬅ strong separation before SUMMARY
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        fontName="Times-Bold",
        fontSize=11,
        spaceBefore=12,
        spaceAfter=4,
        leading=14,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        fontName="Times-Roman",
        fontSize=11,
        leading=14,
        spaceAfter=3,
    )

    content = []

    # ---------- HEADER ----------
    if "NAME" in sections and sections["NAME"]:
        content.append(
            Paragraph(clean_text(sections["NAME"][0]), name_style)
        )

    # explicit spacer to avoid congestion
    content.append(Spacer(1, 6))

    if "CONTACT" in sections:
        cleaned_contact = " | ".join(
            clean_text(c) for c in sections["CONTACT"]
        )
        content.append(
            Paragraph(cleaned_contact, contact_style)
        )

    # ---------- SECTIONS ----------
    for section, lines in sections.items():
        if section in ["NAME", "CONTACT"]:
            continue

        # Section heading
        content.append(
            Paragraph(section.title(), section_style)
        )

        # Thin divider line (as in reference)
        content.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color="#000000",
                spaceBefore=2,
                spaceAfter=6,
            )
        )

        for line in lines:
            content.append(
                Paragraph(clean_text(line), body_style)
            )

    doc.build(content)