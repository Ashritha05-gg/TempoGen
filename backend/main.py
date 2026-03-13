# import os
# import re
# from io import BytesIO
# from typing import List

# from fastapi import FastAPI, UploadFile, File, Body
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse, StreamingResponse

# # ----------- Loaders -----------
# from loaders.pdf_loader import extract_pdf_text
# from loaders.docx_loader import extract_docx_text
# from loaders.ppt_loader import extract_ppt_text
# from loaders.excel_loader import extract_excel_text
# from loaders.csv_loader import extract_csv_text
# from loaders.audio_loader import extract_audio_text

# # ----------- RAG -----------
# from chunker import chunk_pages
# from vector_store import clear_collection, store_chunks
# from gemini_chat import chat_with_rag

# # ----------- PDF Export (Rich) -----------
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import inch


# # ================= APP SETUP =================

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


# # ================= FILE TEXT EXTRACTION =================

# def extract_text_from_file(file_path: str):
#     file_path_lower = file_path.lower()
#     print(f"[INFO] Extracting from file: {file_path}")

#     if file_path_lower.endswith(".pdf"):
#         return extract_pdf_text(file_path)

#     elif file_path_lower.endswith(".docx"):
#         return extract_docx_text(file_path)

#     elif file_path_lower.endswith((".ppt", ".pptx")):
#         return extract_ppt_text(file_path)

#     elif file_path_lower.endswith((".xls", ".xlsx")):
#         return extract_excel_text(file_path)

#     elif file_path_lower.endswith(".csv"):
#         return extract_csv_text(file_path)

#     elif file_path_lower.endswith((".mp3", ".wav", ".m4a")):
#         return extract_audio_text(file_path)

#     elif file_path_lower.endswith((".png", ".jpg", ".jpeg")):
#         return [{
#             "text": "Image uploaded. Use as reference.",
#             "page": 1
#         }]

#     else:
#         raise ValueError(f"Unsupported file type: {file_path}")


# # ================= UPLOAD FILES =================

# @app.post("/upload_files")
# async def upload_files(files: List[UploadFile] = File(...)):
#     all_chunks = []
#     files_to_delete = []

#     try:
#         if not files:
#             return JSONResponse(400, {"error": "No files received"})

#         print("[INFO] Files received:", [f.filename for f in files])

#         for file in files:
#             file_path = os.path.join(UPLOAD_DIR, file.filename)
#             files_to_delete.append(file_path)

#             with open(file_path, "wb") as f:
#                 f.write(await file.read())

#             pages = extract_text_from_file(file_path)

#             if not pages:
#                 raise ValueError(f"No text extracted from {file.filename}")

#             chunks = chunk_pages(pages)
#             if not chunks:
#                 raise ValueError(f"Chunking failed for {file.filename}")

#             all_chunks.extend(chunks)

#         if not all_chunks:
#             raise ValueError("No chunks generated")

#         clear_collection()
#         store_chunks(all_chunks)

#         print(f"[INFO] Total chunks stored: {len(all_chunks)}")

#         return {
#             "message": "Files uploaded and indexed successfully",
#             "files_indexed": [f.filename for f in files],
#             "total_chunks": len(all_chunks),
#         }

#     except Exception as e:
#         print("[ERROR] Upload failed:", str(e))
#         return JSONResponse(500, {"error": str(e)})

#     finally:
#         for path in files_to_delete:
#             if os.path.exists(path):
#                 os.remove(path)


# # ================= CHAT =================

# @app.post("/chat")
# async def chat(payload: dict = Body(...)):
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
#         print("[ERROR] Chat failed:", e)
#         return JSONResponse(500, {"error": "Chat generation failed"})


# # ================= ⭐ NEW PDF EXPORT =================
# @app.post("/export_pdf")
# async def export_pdf(payload: dict = Body(...)):
#     try:
#         import re

#         html = payload.get("html", "")

#         if not html:
#             return JSONResponse(400, {"error": "No content provided"})

#         buffer = BytesIO()

#         doc = SimpleDocTemplate(
#             buffer,
#             pagesize=A4,
#             rightMargin=40,
#             leftMargin=40,
#             topMargin=40,
#             bottomMargin=40,
#         )

#         styles = getSampleStyleSheet()
#         story = []

#         # -------- Detect images --------
#         img_tags = re.findall(r'<img[^>]+src="([^">]+)"', html)

#         # -------- Text blocks --------
#         paragraphs = html.split("</p>")

#         for p in paragraphs:
#             clean = re.sub("<[^>]+>", "", p).strip()

#             if clean:
#                 story.append(Paragraph(clean, styles["Normal"]))
#                 story.append(Spacer(1, 12))

#         # -------- Insert Images --------
#         for img_src in img_tags:
#             if img_src.startswith("blob:"):
#                 continue

#             try:
#                 img = Image(img_src, width=5 * inch, height=3 * inch)
#                 story.append(img)
#                 story.append(Spacer(1, 12))
#             except:
#                 print("Image skipped:", img_src)

#         doc.build(story)

#         buffer.seek(0)

#         return StreamingResponse(
#             buffer,
#             media_type="application/pdf",
#             headers={"Content-Disposition": "inline; filename=document.pdf"},
#         )

#     except Exception as e:
#         return JSONResponse(500, {"error": str(e)})

# @app.post("/export_pdf_template")
# async def export_pdf_template(payload: dict = Body(...)):
#     import re
#     from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
#     from reportlab.lib.styles import getSampleStyleSheet
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib.units import inch

#     html = payload.get("html", "")
#     tpl = payload.get("template", {})

#     buffer = BytesIO()

#     margin = tpl.get("margin", 50)

#     doc = SimpleDocTemplate(
#         buffer,
#         pagesize=A4,
#         leftMargin=margin,
#         rightMargin=margin,
#         topMargin=margin,
#         bottomMargin=margin,
#     )

#     styles = getSampleStyleSheet()
#     story = []

#     # -------- Extract Images --------
#     img_tags = re.findall(r'<img[^>]+src="([^">]+)"', html)

#     # -------- TEXT --------
#     paragraphs = html.split("</p>")

#     for p in paragraphs:
#         clean = re.sub("<[^>]+>", "", p).strip()

#         if clean:
#             style = styles["Normal"]
#             style.fontName = tpl.get("font", "Helvetica")
#             style.fontSize = tpl.get("bodySize", 12)
#             style.leading = tpl.get("bodySize", 12) * tpl.get("lineHeight", 1.4)

#             story.append(Paragraph(clean, style))
#             story.append(Spacer(1, 12))

#     # -------- INSERT IMAGES --------
#     for img_src in img_tags:
#         # skip browser blob URLs
#         if img_src.startswith("blob:"):
#             continue

#         try:
#             img = Image(img_src, width=5 * inch, height=3 * inch)
#             story.append(img)
#             story.append(Spacer(1, 12))
#         except Exception as e:
#             print("Image skipped:", e)

#     # -------- PAGE BORDER FUNCTION --------
#     def draw_border(canvas, doc):
#         if tpl.get("border"):
#             width, height = A4

#             canvas.setLineWidth(2)
#             canvas.rect(
#                 20,
#                 20,
#                 width - 40,
#                 height - 40
#             )

#     doc.build(story, onFirstPage=draw_border, onLaterPages=draw_border)

#     buffer.seek(0)

#     return StreamingResponse(
#         buffer,
#         media_type="application/pdf",
#         headers={"Content-Disposition": "inline; filename=document.pdf"},
#     )




import os
import re
from io import BytesIO
from typing import List

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

# ----------- Loaders -----------
from loaders.pdf_loader import extract_pdf_text
from loaders.docx_loader import extract_docx_text
from loaders.ppt_loader import extract_ppt_text
from loaders.excel_loader import extract_excel_text
from loaders.csv_loader import extract_csv_text
from loaders.audio_loader import extract_audio_text

# ----------- RAG -----------
from chunker import chunk_pages
from vector_store import clear_collection, store_chunks
from gemini_chat import chat_with_rag

# ----------- Resume Feature (ADDED) -----------
from resume_chat import generate_resume
from resume_parser import parse_resume
from resume_pdf_template import build_resume_pdf

# ----------- PDF Export (Rich) -----------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


# ================= APP SETUP =================

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


# ================= FILE TEXT EXTRACTION =================

def extract_text_from_file(file_path: str):
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
        return [{
            "text": "Image uploaded. Use as reference.",
            "page": 1
        }]

    else:
        raise ValueError(f"Unsupported file type: {file_path}")


# ================= UPLOAD FILES =================

@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    all_chunks = []
    files_to_delete = []

    try:
        if not files:
            return JSONResponse(400, {"error": "No files received"})

        print("[INFO] Files received:", [f.filename for f in files])

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            files_to_delete.append(file_path)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            pages = extract_text_from_file(file_path)

            if not pages:
                raise ValueError(f"No text extracted from {file.filename}")

            chunks = chunk_pages(pages)
            if not chunks:
                raise ValueError(f"Chunking failed for {file.filename}")

            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError("No chunks generated")

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
        return JSONResponse(500, {"error": str(e)})

    finally:
        for path in files_to_delete:
            if os.path.exists(path):
                os.remove(path)


# ================= CHAT =================

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
        return JSONResponse(500, {"error": "Chat generation failed"})


# ================= RESUME CHAT (ADDED) =================

@app.post("/resume/chat")
async def resume_chat(payload: dict = Body(...)):
    try:
        prompt = payload.get("prompt")

        if not prompt:
            return JSONResponse(
                status_code=400,
                content={"error": "prompt is required"},
            )

        resume_text = generate_resume(prompt)

        return {"text": resume_text}

    except Exception as e:
        print("[RESUME ERROR]", e)
        return JSONResponse(
            status_code=500,
            content={"error": "Resume generation failed"},
        )


# ================= RESUME PDF EXPORT (ADDED) =================

@app.post("/resume/pdf")
async def export_resume_pdf(payload: dict = Body(...)):
    try:
        text = payload.get("text")

        if not text:
            return JSONResponse(
                status_code=400,
                content={"error": "Resume text is required"},
            )

        sections = parse_resume(text)

        buffer = BytesIO()
        build_resume_pdf(sections, buffer)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=resume.pdf"},
        )

    except Exception as e:
        print("[RESUME PDF ERROR]", e)
        return JSONResponse(
            status_code=500,
            content={"error": "Resume PDF generation failed"},
        )


# ================= DOCUMENT PDF EXPORT =================

@app.post("/export_pdf")
async def export_pdf(payload: dict = Body(...)):
    try:
        html = payload.get("html", "")

        if not html:
            return JSONResponse(400, {"error": "No content provided"})

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        story = []

        img_tags = re.findall(r'<img[^>]+src="([^">]+)"', html)

        paragraphs = html.split("</p>")

        for p in paragraphs:
            clean = re.sub("<[^>]+>", "", p).strip()

            if clean:
                story.append(Paragraph(clean, styles["Normal"]))
                story.append(Spacer(1, 12))

        for img_src in img_tags:
            if img_src.startswith("blob:"):
                continue

            try:
                img = Image(img_src, width=5 * inch, height=3 * inch)
                story.append(img)
                story.append(Spacer(1, 12))
            except:
                print("Image skipped:", img_src)

        doc.build(story)

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=document.pdf"},
        )

    except Exception as e:
        return JSONResponse(500, {"error": str(e)})


# ================= TEMPLATE PDF EXPORT =================

@app.post("/export_pdf_template")
async def export_pdf_template(payload: dict = Body(...)):
    html = payload.get("html", "")
    tpl = payload.get("template", {})

    buffer = BytesIO()

    margin = tpl.get("margin", 50)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
    )

    styles = getSampleStyleSheet()
    story = []

    img_tags = re.findall(r'<img[^>]+src="([^">]+)"', html)

    paragraphs = html.split("</p>")

    for p in paragraphs:
        clean = re.sub("<[^>]+>", "", p).strip()

        if clean:
            style = styles["Normal"]
            style.fontName = tpl.get("font", "Helvetica")
            style.fontSize = tpl.get("bodySize", 12)
            style.leading = tpl.get("bodySize", 12) * tpl.get("lineHeight", 1.4)

            story.append(Paragraph(clean, style))
            story.append(Spacer(1, 12))

    for img_src in img_tags:
        if img_src.startswith("blob:"):
            continue

        try:
            img = Image(img_src, width=5 * inch, height=3 * inch)
            story.append(img)
            story.append(Spacer(1, 12))
        except Exception as e:
            print("Image skipped:", e)

    def draw_border(canvas, doc):
        if tpl.get("border"):
            width, height = A4

            canvas.setLineWidth(2)
            canvas.rect(
                20,
                20,
                width - 40,
                height - 40
            )

    doc.build(story, onFirstPage=draw_border, onLaterPages=draw_border)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=document.pdf"},
    )