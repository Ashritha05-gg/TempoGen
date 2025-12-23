


# vector_store.py

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import uuid # ⬅️ New import for generating unique IDs

# Sentence-transformers embedding model
# Note: all-MiniLM-L6-v2 is fast, but consider a higher quality model like all-mpnet-base-v2 for better results.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ CRITICAL UPDATE: Switch to PersistentClient
# This will save your indexed data to a local folder named "./chroma_db".
client = chromadb.PersistentClient(path="./chroma_db")

# Single collection for the current uploaded documents
collection = client.get_or_create_collection(name="pdf_collection")


def clear_collection():
    
    """
    Clears the current collection (used when new files are uploaded).
    """
    global collection
    # NOTE: Deleting and recreating the collection is necessary for PersistentClient
    # to ensure a clean slate, as client.reset() might affect the entire database.
    client.delete_collection(name="pdf_collection")
    collection = client.get_or_create_collection(name="pdf_collection")


def store_chunks(chunks: List[Dict]):
    """
    Store list of chunks in Chroma.
    chunks: [{ "text": str, "page": int }, ...]
    """
    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        texts.append(chunk["text"])
        metadatas.append({"page": chunk["page"]})
        
        # ✅ IMPROVEMENT: Use UUID for robust, unique IDs for each chunk.
        # This prevents ID collisions if you were to index files separately later.
        ids.append(str(uuid.uuid4()))

    embeddings = embedding_model.encode(texts).tolist()

    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids,
    )


def query_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve top_k chunks relevant to the query using vector search.
    """
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    chunks = []
    for doc, meta in zip(documents, metadatas):
        chunks.append(
            {
                "text": doc,
                "page": meta["page"],
            }
        )

    return chunks