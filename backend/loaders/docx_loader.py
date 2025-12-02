# loaders/docx_loader.py

from docx import Document
import os
from typing import List, Dict

def extract_docx_text(file_path: str) -> List[Dict]:
    doc = Document(file_path)
    output = []
    filename = os.path.basename(file_path)

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            output.append({
                "text": text,
                "page": f"paragraph-{i+1}",
                "source": filename
            })

    return output
