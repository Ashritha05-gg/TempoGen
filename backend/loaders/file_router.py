from loaders.pdf_loader import extract_pdf_text
from loaders.docx_loader import extract_docx_text
from loaders.ppt_loader import extract_ppt_text
from loaders.excel_loader import extract_excel_text


def extract_text_from_file(file_path: str):
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)
    elif file_path.endswith(".ppt") or file_path.endswith(".pptx"):
        return extract_ppt_text(file_path)
    elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
        return extract_excel_text(file_path)
    else:
        raise ValueError("Unsupported file format")
