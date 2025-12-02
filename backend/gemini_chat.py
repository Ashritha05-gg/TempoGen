# # gemini_chat.py

# import os
# from typing import List, Dict, Any
# from dotenv import load_dotenv
# import google.generativeai as genai

# from rag_engine import build_context
# from memory import get_history, add_message, get_last_model_message

# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # ✅ Verified working model from your list
# model = genai.GenerativeModel("models/gemini-pro-latest")


# def chat_with_rag(session_id: str, user_prompt: str) -> str:
#     """
#     Fully conversational RAG-based chat.
#     Supports ANY natural language prompt.
#     """

#     # 1️⃣ Retrieve document context relevant to the current prompt
#     context = build_context(user_prompt)

#     if not context:
#         context = "No relevant information was found in the document."

#     # 2️⃣ System instruction (VERY important)
#     system_prompt = (
#         "You are an AI assistant that answers questions strictly using the document context "
#         "and the ongoing conversation.\n\n"
#         "Rules:\n"
#         "- Use ONLY the document context for factual information\n"
#         "- If something is not present, say: 'Not found in the document.'\n"
#         "- The user may refine or modify previous answers naturally\n"
#         "- Mention reference labels like [1], [2] when using document content\n\n"
#         f"Document Context:\n{context}"
#     )

#     # 3️⃣ Build conversation messages
#     messages: List[Dict[str, Any]] = []

#     # Gemini doesn't support a real system role → pass as first user message
#     messages.append({
#         "role": "user",
#         "parts": [system_prompt]
#     })

#     # Add previous conversation
#     history = get_history(session_id)
#     for msg in history:
#         messages.append({
#             "role": msg["role"],
#             "parts": [msg["content"]]
#         })

#     # Add current prompt
#     messages.append({
#         "role": "user",
#         "parts": [user_prompt]
#     })

#     # 4️⃣ Generate response
#     response = model.generate_content(messages)
#     answer = response.text.strip()

#     # 5️⃣ Save conversation
#     add_message(session_id, "user", user_prompt)
#     add_message(session_id, "model", answer)

#     return answer


# gemini_chat.py

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

from rag_engine import build_context
from memory import get_history, add_message

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=API_KEY)

# ✅ Use the model that worked from your check_models.py
model = genai.GenerativeModel("models/gemini-2.5-flash")


def chat_with_rag(session_id: str, user_prompt: str) -> str:
    """
    Fully conversational RAG-based chat.
    - Uses document context for facts.
    - Remembers previous turns via session_id.
    - Supports ANY natural prompts.
    - If the user asks for multiple sections (Executive Summary, Abstract, Results, etc.),
      it formats the output as a mini-report with bold headings.
    """

    # 1️⃣ Get relevant document context for this prompt
    context = build_context(user_prompt, top_k=5)
    if not context.strip():
        context = "No relevant information was found in the document."

    # 2️⃣ System prompt: rules + formatting instructions
    system_prompt = f"""
You are an AI assistant that answers questions strictly using the document context
and the ongoing conversation.

Rules:
- Use ONLY the document context for factual information.
- If the requested information is not present in the context, reply exactly:
  "Not found in the document."
- The document context chunks are labeled like [1], [2], etc., each with a page number.
- When you use information from a chunk, include the label(s) in your answer,
  for example: [1], [2].

Formatting:
- For normal questions, respond in clear, well-structured paragraphs.
- If the user asks for one or more report sections (for example:
  Executive Summary, Abstract, Introduction, Methodology, Results, Discussion,
  Conclusion, Dataset, Future Work, Summary), then format the answer as a mini-report:
  * Use bold markdown headings for each requested section, e.g.:

    **Executive Summary**
    <content here>

    **Abstract**
    <content here>

    **Results**
    <content here>

  * Put the content for each section directly under its heading.
  * You may include references like [1], [2] inside each section when using
    specific evidence from the document context.

Document context:
{context}
""".strip()

    # 3️⃣ Build message list for Gemini (system-style prompt + history + current user)
    messages: List[Dict[str, Any]] = []

    # First message: system-style instructions as a user message
    messages.append({
        "role": "user",
        "parts": [system_prompt]
    })

    # Add previous conversation from memory
    history = get_history(session_id)
    for msg in history:
        messages.append({
            "role": msg["role"],  # 'user' or 'model'
            "parts": [msg["content"]]
        })

    # Add current user prompt
    messages.append({
        "role": "user",
        "parts": [user_prompt]
    })

    # 4️⃣ Call Gemini
    response = model.generate_content(messages)
    answer = response.text.strip()

    # 5️⃣ Save this turn in memory
    add_message(session_id, "user", user_prompt)
    add_message(session_id, "model", answer)

    return answer
