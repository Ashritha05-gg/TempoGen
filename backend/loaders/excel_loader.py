# loaders/excel_loader.py

import pandas as pd
import os
from typing import List, Dict

def extract_excel_text(file_path: str) -> List[Dict]:
    sheets = pd.read_excel(file_path, sheet_name=None)
    output = []
    filename = os.path.basename(file_path)

    for sheet_name, df in sheets.items():
        text = df.astype(str).to_string(index=False)
        output.append({
            "text": text,
            "page": f"sheet-{sheet_name}",
            "source": filename
        })

    return output
