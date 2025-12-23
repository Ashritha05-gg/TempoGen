



import os
from io import BytesIO
from typing import List

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from loaders.pdf_loader import extract_pdf_text
from loaders.docx_loader import extract_docx_text
from loaders.ppt_loader import extract_ppt_text
from loaders.excel_loader import extract_excel_text
from loaders.csv_loader import extract_csv_text
from loaders.audio_loader import extract_audio_text



from chunker import chunk_pages
from vector_store import clear_collection, store_chunks
from gemini_chat import chat_with_rag

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap

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
    """
    Route to the correct loader based on file extension.
    Returns: list of { 'text': str, 'page': int }
    """
    file_path_lower = file_path.lower()
    print(f"[INFO] Extracting from file: {file_path}")

    if file_path_lower.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif file_path_lower.endswith(".docx"):
        return extract_docx_text(file_path)

    elif file_path_lower.endswith((".ppt", ".pptx")):
        return extract_ppt_text(file_path)

    elif file_path_lower.endswith((".xls", ".xlsx")):
        return extract_excel_text(file_path)
    elif file_path_lower.endswith(".csv"):
        return extract_csv_text(file_path)
    elif file_path_lower.endswith((".mp3", ".wav", ".m4a")):
        return extract_audio_text(file_path)



    elif file_path_lower.endswith((".png", ".jpg", ".jpeg")):
        # Image support (no OCR yet)
        print("[INFO] Image uploaded — skipping text extraction")
        return [
            {
                "text": "Image uploaded. Use it as visual reference if required.",
                "page": 1,
            }
        ]

    else:
        raise ValueError(f"Unsupported file type: {file_path}")

# -------------------- ENDPOINTS --------------------

@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload and index multiple files.
    Can be called ANY time (even mid-conversation).
    """
    all_chunks = []
    files_to_delete = []

    try:
        if not files:
            return JSONResponse(
                status_code=400,
                content={"error": "No files received"},
            )

        print("[INFO] Files received:", [f.filename for f in files])

        # Process each file
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            files_to_delete.append(file_path)

            print(f"[INFO] Saving file: {file.filename}")
            with open(file_path, "wb") as f:
                f.write(await file.read())

            extracted_pages = extract_text_from_file(file_path)

            if not extracted_pages:
                raise ValueError(f"No text extracted from {file.filename}")

            chunks = chunk_pages(extracted_pages)
            if not chunks:
                raise ValueError(f"Chunking failed for {file.filename}")

            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError("No chunks generated")

        # Replace old knowledge with new uploads
        clear_collection()
        store_chunks(all_chunks)

        print(f"[INFO] Total chunks stored: {len(all_chunks)}")

        return {
            "message": "Files uploaded and indexed successfully",
            "files_indexed": [f.filename for f in files],
            "total_chunks": len(all_chunks),
        }

    except Exception as e:
        print("[ERROR] Upload failed:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        # Cleanup uploaded files
        for path in files_to_delete:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"[WARN] Cleanup failed for {path}: {e}")

# -------------------- CHAT --------------------

# @app.post("/chat")
# async def chat(payload: dict = Body(...)):
#     """
#     Conversational RAG chat endpoint.
#     payload = { "session_id": str, "prompt": str }
#     """
#     try:
#         session_id = payload.get("session_id")
#         prompt = payload.get("prompt")

#         if not session_id or not prompt:
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "session_id and prompt are required"},
#             )

#         response = chat_with_rag(session_id, prompt)
#         return {"response": response}

#     except Exception as e:
#         print("[ERROR] Chat failed:", str(e))
#         return JSONResponse(status_code=500, content={"error": str(e)})
@app.post("/chat")
async def chat(payload: dict = Body(...)):
    try:
        session_id = payload.get("session_id")
        prompt = payload.get("prompt")

        if not session_id or not prompt:
            return JSONResponse(
                status_code=400,
                content={"error": "session_id and prompt are required"},
            )

        response = chat_with_rag(session_id, prompt)

        return {"response": response}

    except Exception as e:
        print("[ERROR] Chat failed:", e)
        return JSONResponse(
            status_code=500,
            content={"error": "Chat generation failed"},
        )







# @app.post("/export_pdf")
# async def export_pdf(payload: dict = Body(...)):
#     try:
#         sections = payload.get("sections", [])

#         if not sections:
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "No sections to export"}
#             )

#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer, pagesize=A4)

#         width, height = A4
#         x_margin = 50
#         y = height - 60

#         for sec in sections:
#             title = sec.get("section", "")
#             content = sec.get("content", "")

#             # ---- Title ----
#             if title:
#                 pdf.setFont("Helvetica-Bold", 16)
#                 pdf.drawString(x_margin, y, title)
#                 y -= 28

#             # ---- Body ----
#             pdf.setFont("Helvetica", 11)

#             wrapped_lines = textwrap.wrap(content, width=90)

#             for line in wrapped_lines:
#                 if y < 80:
#                     pdf.showPage()
#                     pdf.setFont("Helvetica", 11)
#                     y = height - 60

#                 pdf.drawString(x_margin, y, line)
#                 y -= 16

#             y -= 24

#             if y < 80:
#                 pdf.showPage()
#                 y = height - 60

#         pdf.save()
#         buffer.seek(0)

#         return StreamingResponse(
#             buffer,
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": 'inline; filename="document.pdf"'
#             }
#         )

#     except Exception as e:
#         print("[PDF ERROR]", e)
#         return JSONResponse(status_code=500, content={"error": "PDF export failed"})



@app.post("/export_pdf")
async def export_pdf(payload: dict = Body(...)):
    try:
        sections = payload.get("sections", [])

        if not sections:
            return JSONResponse(status_code=400, content={"error": "No sections"})

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        x_margin = 50
        y = height - 60

        for sec in sections:
            title = sec.get("section", "")
            content = sec.get("content", "")
            images = sec.get("images", [])

            # ---- Title ----
            if title:
                p.setFont("Helvetica-Bold", 16)
                p.drawString(x_margin, y, title)
                y -= 24

            # ---- Text ----
            p.setFont("Helvetica", 12)
            if content:
                wrapped = textwrap.wrap(content, 90)
                for line in wrapped:
                    if y < 100:
                        p.showPage()
                        p.setFont("Helvetica", 12)
                        y = height - 60
                    p.drawString(x_margin, y, line)
                    y -= 16

            # ---- Images ----
            for img in images:
                try:
                    img_url = img.get("url")
                    if img_url and img_url.startswith("blob:"):
                        continue  # browser-only images cannot be drawn

                    image = ImageReader(img_url)
                    img_width = width - 100
                    img_height = img_width * 0.6

                    if y < img_height + 40:
                        p.showPage()
                        y = height - 60

                    p.drawImage(
                        image,
                        x_margin,
                        y - img_height,
                        width=img_width,
                        height=img_height,
                        preserveAspectRatio=True,
                    )
                    y -= img_height + 20
                except Exception as e:
                    print("Image skipped:", e)

            y -= 20

        p.save()
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=document.pdf"},
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
