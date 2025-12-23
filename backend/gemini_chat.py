




# gemini_chat.py

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

from rag_engine import build_context
from memory import get_history, add_message

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# ✅ Correct model name (without "models/")
model = genai.GenerativeModel("gemini-2.5-flash")


def chat_with_rag(session_id: str, user_prompt: str) -> str:
    """
    RAG + Chat memory document assistant.
    Takes user prompt, retrieves document context, applies rules,
    and generates structured sections for the frontend.
    Fully conversational RAG-based chat. 
      - Uses document context for facts. 
      - Remembers previous turns via session_id. 
      - Supports ANY natural prompts. 
      - If the user asks for multiple sections (Executive Summary, Abstract, Results, etc.), 
        it formats the output as a mini-report with bold headings.
    """

    # 1️⃣ Retrieve relevant chunks using RAG
    context = build_context(user_prompt, top_k=10)
    if not context.strip():
        context = "No relevant information was found in the document."

    # 2️⃣ Create system instructions
    system_prompt = f"""
You are an AI document-writing assistant.

Your role is to help the user build, expand, or rewrite sections of a document
based on BOTH:
1. Retrieved document context
2. Conversation history

RULES:
- If the user asks to add/create a section → WRITE ONLY that section.
- If user asks to rewrite/shorten/expand → MODIFY ONLY that section.
- Do NOT rewrite the whole document unless asked explicitly.
- For high-level sections (Abstract, Introduction, Summary, Conclusion), 
  you may synthesize from document meaning.

- For specific factual questions, use the retrieved context and cite using [1], [2].
- Format every section like:
- If the user asks for one or more report sections (for example: 
  Executive Summary, Abstract, Introduction, Methodology, Results, Discussion, 
  Conclusion, Dataset, Future Work, Summary), then format the answer as a mini-report: * Use bold markdown headings for each requested section, e.g.:  
  **Executive Summary**  
    <content here>  
  **Abstract**  
    <content here> 
   **Results** 
    <content here>

  **Section Title**
  Your content...

Document Context:
{context}
""".strip()

    # 3️⃣ Build messages in Gemini format
    messages: List[Dict[str, Any]] = []

    # System prompt (Gemini-style = user role)
    messages.append({
        "role": "user",
        "parts": [system_prompt]
    })

    # Add memory history
    history = get_history(session_id)
    for msg in history:
        messages.append({
            "role": msg["role"],
            "parts": [msg["content"]]
        })

    # Current user query
    messages.append({
        "role": "user",
        "parts": [user_prompt]
    })

    # 4️⃣ Generate completion using Gemini
    response = model.generate_content(messages)
    answer = response.text.strip()

    # 5️⃣ Save memory
    add_message(session_id, "user", user_prompt)
    add_message(session_id, "model", answer)

    return answer

