# memory.py

chat_memory = {}  # session_id -> list of messages


def get_history(session_id: str):
    return chat_memory.get(session_id, [])


def add_message(session_id: str, role: str, content: str):
    if session_id not in chat_memory:
        chat_memory[session_id] = []
    chat_memory[session_id].append({
        "role": role,
        "content": content
    })


def get_last_model_message(session_id: str):
    history = chat_memory.get(session_id, [])
    for msg in reversed(history):
        if msg["role"] == "model":
            return msg["content"]
    return None
