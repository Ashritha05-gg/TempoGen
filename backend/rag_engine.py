# # rag_engine.py

# from typing import List
# from vector_store import query_chunks

# def build_context(query: str, top_k: int = 5) -> str:
#     """
#     Use vector store to get relevant chunks and format them as context.
#     """
#     chunks = query_chunks(query, top_k=top_k)
#     context_lines: List[str] = []

#     for i, chunk in enumerate(chunks, start=1):
#         context_lines.append(f"[{i}] (Page {chunk['page']}): {chunk['text']}")

#     return "\n\n".join(context_lines)


# rag_engine.py

from vector_store import query_chunks


def build_context(query: str, top_k: int = 5) -> str:
    chunks = query_chunks(query, top_k)

    if not chunks:
        return ""

    context_lines = []
    for idx, chunk in enumerate(chunks, start=1):
        context_lines.append(
            f"[{idx}] (Page {chunk['page']}): {chunk['text']}"
        )

    return "\n\n".join(context_lines)
