# vector_store.py

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ NEW Chroma client initialization (NO Settings)
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="pdf_collection")


def clear_collection():
    global collection
    client.delete_collection(name="pdf_collection")
    collection = client.get_or_create_collection(name="pdf_collection")


def store_chunks(chunks: List[Dict]):
    texts = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        texts.append(chunk["text"])
        metadatas.append({"page": chunk["page"]})
        ids.append(str(i))

    embeddings = embedding_model.encode(texts).tolist()

    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )


def query_chunks(query: str, top_k: int = 5) -> List[Dict]:
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    chunks = []
    for doc, meta in zip(documents, metadatas):
        chunks.append({
            "text": doc,
            "page": meta["page"]
        })

    return chunks
