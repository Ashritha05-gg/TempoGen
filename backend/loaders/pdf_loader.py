# loaders/pdf_loader.py

import fitz  # PyMuPDF
import os
from typing import List, Dict

def extract_pdf_text(pdf_path: str) -> List[Dict]:
    doc = fitz.open(pdf_path)
    pages = []
    filename = os.path.basename(pdf_path)

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "text": text,
                "page": page_num + 1,
                "source": filename
            })

    return pages
