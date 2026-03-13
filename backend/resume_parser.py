# resume_parser.py
def parse_resume(text: str) -> dict:
    sections = {}
    current = None

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Normalize headings
        upper = line.upper()

        if upper in [
            "NAME",
            "CONTACT",
            "SUMMARY",
            "SKILLS",
            "PROJECTS",
            "EXPERIENCE",
            "EDUCATION",
            "CERTIFICATIONS",
        ]:
            current = upper
            sections[current] = []
            continue

        # Detect name heuristically (first non-empty line)
        if current is None and "@" not in line and len(line.split()) <= 4:
            sections.setdefault("NAME", []).append(line)
            continue

        # Detect contact line
        if "@" in line or "linkedin" in line.lower():
            sections.setdefault("CONTACT", []).append(line)
            continue

        if current:
            sections[current].append(line)

    return sections