



from vector_store import query_chunks


HIGH_LEVEL_QUERIES = [
    "abstract", "introduction", "summary", "overview",
    "executive summary", "conclusion", "future work"
]


def build_context(query: str, top_k: int = 5) -> str:
    """
    Build document context for Gemini using vector search.
    Automatically expands context for high-level prompts.
    """

    query_lower = query.lower()

    # ✅ If user asks high-level section, broaden context
    if any(key in query_lower for key in HIGH_LEVEL_QUERIES):
        chunks = query_chunks("overall document", top_k=12)
    else:
        chunks = query_chunks(query, top_k)

    if not chunks:
        return ""

    context_lines = []
    for idx, chunk in enumerate(chunks, start=1):
        context_lines.append(
            f"[{idx}] (Page {chunk['page']}): {chunk['text']}"
        )

    return "\n\n".join(context_lines)
