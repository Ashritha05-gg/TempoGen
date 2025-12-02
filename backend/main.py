# import os
# from typing import List

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse

# from loaders.pdf_loader import extract_pdf_text
# from loaders.docx_loader import extract_docx_text
# from loaders.ppt_loader import extract_ppt_text
# from loaders.excel_loader import extract_excel_text

# from chunker import chunk_pages
# from vector_store import clear_collection, store_chunks
# from gemini_chat import chat_with_rag

# # -------------------- APP SETUP --------------------

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # -------------------- HELPERS --------------------

# def extract_text_from_file(file_path: str):
#     file_path_lower = file_path.lower()
#     print(f"[INFO] Extracting from file: {file_path}")

#     if file_path_lower.endswith(".pdf"):
#         return extract_pdf_text(file_path)

#     elif file_path_lower.endswith(".docx"):
#         return extract_docx_text(file_path)

#     elif file_path_lower.endswith(".ppt") or file_path_lower.endswith(".pptx"):
#         return extract_ppt_text(file_path)

#     elif file_path_lower.endswith(".xls") or file_path_lower.endswith(".xlsx"):
#         return extract_excel_text(file_path)

#     else:
#         raise ValueError(f"Unsupported file type: {file_path}")

# # -------------------- ENDPOINTS --------------------

# @app.post("/upload_files")
# async def upload_files(files: List[UploadFile] = File(...)):
#     """
#     Upload and index multiple files (PDF, DOCX, PPT, Excel).
#     """
#     try:
#         if not files:
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "No files received"}
#             )

#         print("[INFO] Files received:", [f.filename for f in files])

#         clear_collection()
#         all_chunks = []

#         for file in files:
#             file_path = os.path.join(UPLOAD_DIR, file.filename)
#             print(f"[INFO] Saving file: {file.filename}")

#             with open(file_path, "wb") as f:
#                 f.write(await file.read())

#             extracted_pages = extract_text_from_file(file_path)

#             if not extracted_pages:
#                 raise ValueError(f"No text could be extracted from {file.filename}")

#             print(f"[INFO] Extracted {len(extracted_pages)} items from {file.filename}")

#             chunks = chunk_pages(extracted_pages)

#             if not chunks:
#                 raise ValueError(f"Chunking failed for {file.filename}")

#             print(f"[INFO] Created {len(chunks)} chunks from {file.filename}")

#             all_chunks.extend(chunks)

#         if not all_chunks:
#             raise ValueError("No chunks generated from uploaded files")

#         store_chunks(all_chunks)
#         print(f"[INFO] Stored total chunks: {len(all_chunks)}")

#         return {
#             "message": "All files uploaded and indexed successfully",
#             "files_indexed": [file.filename for file in files],
#             "total_chunks": len(all_chunks)
#         }

#     except Exception as e:
#         print("[ERROR] Upload failed:", str(e))
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e)}
#         )


# @app.post("/chat")
# async def chat(
#     session_id: str = Form(...),
#     prompt: str = Form(...)
# ):
#     """
#     Conversational RAG chat endpoint.
#     """
#     try:
#         response = chat_with_rag(session_id, prompt)
#         return {"response": response}

#     except Exception as e:
#         print("[ERROR] Chat failed:", str(e))
#         return JSONResponse(
#             status_code=500,
#             content={"error": str(e)}
#         )





import os
from typing import List

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from loaders.pdf_loader import extract_pdf_text
from loaders.docx_loader import extract_docx_text
from loaders.ppt_loader import extract_ppt_text
from loaders.excel_loader import extract_excel_text

from chunker import chunk_pages
from vector_store import clear_collection, store_chunks
from gemini_chat import chat_with_rag

# -------------------- APP SETUP --------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- HELPERS --------------------

def extract_text_from_file(file_path: str):
    file_path_lower = file_path.lower()
    print(f"[INFO] Extracting from file: {file_path}")

    if file_path_lower.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif file_path_lower.endswith(".docx"):
        return extract_docx_text(file_path)

    elif file_path_lower.endswith(".ppt") or file_path_lower.endswith(".pptx"):
        return extract_ppt_text(file_path)

    elif file_path_lower.endswith(".xls") or file_path_lower.endswith(".xlsx"):
        return extract_excel_text(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path}")

# -------------------- ENDPOINTS --------------------

@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload and index multiple files (PDF, DOCX, PPT, Excel).
    Also returns extracted content for live preview.
    """
    try:
        if not files:
            return JSONResponse(
                status_code=400,
                content={"error": "No files received"}
            )

        print("[INFO] Files received:", [f.filename for f in files])

        clear_collection()
        all_chunks = []
        preview_text_parts = []   # ✅ FOR FRONTEND PREVIEW

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            print(f"[INFO] Saving file: {file.filename}")

            with open(file_path, "wb") as f:
                f.write(await file.read())

            extracted_pages = extract_text_from_file(file_path)

            if not extracted_pages:
                raise ValueError(f"No text could be extracted from {file.filename}")

            print(f"[INFO] Extracted {len(extracted_pages)} pages from {file.filename}")

            # ✅ Collect raw text (for left preview)
            for page in extracted_pages:
                preview_text_parts.append(page["text"])

            chunks = chunk_pages(extracted_pages)

            if not chunks:
                raise ValueError(f"Chunking failed for {file.filename}")

            print(f"[INFO] Created {len(chunks)} chunks from {file.filename}")

            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError("No chunks generated from uploaded files")

        store_chunks(all_chunks)
        print(f"[INFO] Stored total chunks: {len(all_chunks)}")

        # ✅ MERGE PREVIEW TEXT
        full_preview_text = "\n\n".join(preview_text_parts)

        return {
            "message": "All files uploaded and indexed successfully",
            "files_indexed": [file.filename for file in files],
            "total_chunks": len(all_chunks),
            "content": full_preview_text   # ✅ THIS FIXES PREVIEW
        }

    except Exception as e:
        print("[ERROR] Upload failed:", str(e))
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    prompt: str = Form(...)
):
    """
    Conversational RAG chat endpoint.
    """
    try:
        response = chat_with_rag(session_id, prompt)
        return {"response": response}

    except Exception as e:
        print("[ERROR] Chat failed:", str(e))
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
