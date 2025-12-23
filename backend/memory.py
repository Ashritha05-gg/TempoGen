


# memory.py

# Stores message history per session ID
chat_memory = {}  
MAX_HISTORY = 10  # Keep last 10 messages per session


def get_history(session_id: str):
    """Return message history for a session."""
    return chat_memory.get(session_id, [])


def add_message(session_id: str, role: str, content: str):
    """Store a new message and truncate old memory."""
    if session_id not in chat_memory:
        chat_memory[session_id] = []

    chat_memory[session_id].append({
        "role": role,
        "content": content
    })

    # Limit stored memory (avoid infinite growth)
    if len(chat_memory[session_id]) > MAX_HISTORY:
        chat_memory[session_id] = chat_memory[session_id][-MAX_HISTORY:]


def clear_session(session_id: str):
    """Clear conversation for new chat session."""
    if session_id in chat_memory:
        del chat_memory[session_id]
