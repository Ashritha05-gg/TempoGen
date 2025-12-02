# loaders/ppt_loader.py

from pptx import Presentation
import os
from typing import List, Dict

def extract_ppt_text(file_path: str) -> List[Dict]:
    prs = Presentation(file_path)
    output = []
    filename = os.path.basename(file_path)

    for i, slide in enumerate(prs.slides):
        slide_text = []

        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text.append(shape.text)

        if slide_text:
            output.append({
                "text": "\n".join(slide_text),
                "page": f"slide-{i+1}",
                "source": filename
            })

    return output
