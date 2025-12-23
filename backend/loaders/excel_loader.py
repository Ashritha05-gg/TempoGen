# import pandas as pd
# import os
# from typing import List, Dict

# def extract_excel_text(file_path: str) -> List[Dict]:
#     sheets = pd.read_excel(file_path, sheet_name=None)
#     output = []
#     filename = os.path.basename(file_path)

#     for sheet_name, df in sheets.items():
#         cols = list(df.columns)
#         rows = len(df)

#         sample = df.head(5).astype(str).to_dict(orient="records")

#         text = f"""
# Excel Sheet: {sheet_name}
# Columns: {', '.join(cols)}
# Total Rows: {rows}

# Sample Rows:
# {sample}
# """.strip()

#         output.append({
#             "text": text,
#             "page": f"sheet-{sheet_name}",
#             "source": filename
#         })

#     return output


import pandas as pd
import os
from typing import List, Dict

def extract_excel_text(file_path: str) -> List[Dict]:
    sheets = pd.read_excel(file_path, sheet_name=None)
    output = []
    filename = os.path.basename(file_path)

    for sheet_name, df in sheets.items():
        columns = ", ".join(df.columns.astype(str))
        preview = df.head(5).astype(str).to_string(index=False)

        text = f"""
Sheet name: {sheet_name}
Columns: {columns}
Row count: {len(df)}

Sample rows:
{preview}
""".strip()

        output.append({
            "text": text,
            "page": f"sheet-{sheet_name}",
            "source": filename
        })

    return output
