import pandas as pd
import os
from typing import List, Dict

def extract_csv_text(file_path: str) -> List[Dict]:
    df = pd.read_csv(file_path)
    filename = os.path.basename(file_path)

    columns = ", ".join(df.columns.astype(str))
    preview = df.head(5).astype(str).to_string(index=False)

    text = f"""
CSV File: {filename}
Columns: {columns}
Row count: {len(df)}

Sample rows:
{preview}
""".strip()

    return [{
        "text": text,
        "page": "csv",
        "source": filename
    }]
