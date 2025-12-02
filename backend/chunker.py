# chunker.py

from typing import List, Dict

def chunk_pages(pages: List[Dict], chunk_size: int = 250) -> List[Dict]:
    """
    Split each page's text into chunks of ~chunk_size words.
    Returns list of { 'text': str, 'page': int }
    """
    chunks = []
    for page in pages:
        words = page["text"].split()
        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i:i + chunk_size])
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "page": page["page"]
                })
    return chunks
