# resume_chat.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=API_KEY)

# Simple, fast model (safe)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_resume(user_prompt: str) -> str:
    """
    Generate a professional resume from user instructions.
    Returns PLAIN TEXT only.
    """

    prompt = f"""
You are a professional resume writer.

Generate a clean, ATS-friendly resume based on the user's request.

Rules:
- Do NOT return JSON
- Do NOT use markdown (** or ##)
- Use clear section headings
- Plain readable text only

Recommended format:
NAME
CONTACT
SUMMARY
SKILLS
PROJECTS
EXPERIENCE
EDUCATION
CERTIFICATIONS (if any)

User request:
{user_prompt}
"""

    response = model.generate_content(prompt)
    return response.text.strip()