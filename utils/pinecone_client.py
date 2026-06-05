"""
Pinecone vector database client.

Compatible with pinecone >= 3.x (the new `pinecone` package, formerly `pinecone-client`).
"""

from __future__ import annotations
from typing import Any, Dict, List

from utils.embeddings import EMBEDDING_DIMENSION


# ── Initialise / connect ──────────────────────────────────────────────────────

def init_pinecone(api_key: str, index_name: str):
    """
    Initialise Pinecone and return (or create) the requested index.

    Parameters
    ----------
    api_key : str
        Pinecone API key.
    index_name : str
        Name of the index to use.

    Returns
    -------
    pinecone.Index
        A connected Pinecone index object.
    """
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key=api_key)

    existing_indexes = [idx.name for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        # Wait until index is ready
        import time
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(index_name)


# ── Upsert ────────────────────────────────────────────────────────────────────

def upsert_chunks(index, chunks: List[Dict[str, Any]], batch_size: int = 100) -> None:
    """
    Upsert a list of chunk dicts into the Pinecone index.

    Each dict must contain:
      - id        : str  (unique vector id)
      - embedding : List[float]
      - text      : str
      - doc_name  : str
      - chunk_idx : int

    Parameters
    ----------
    index : pinecone.Index
    chunks : list of chunk dicts
    batch_size : int
        Number of vectors per upsert call.
    """
    vectors = []
    for chunk in chunks:
        vectors.append(
            {
                "id": chunk["id"],
                "values": chunk["embedding"],
                "metadata": {
                    "text":      chunk["text"],
                    "doc_name":  chunk["doc_name"],
                    "chunk_idx": chunk["chunk_idx"],
                },
            }
        )

    # Upsert in batches to respect Pinecone's request size limits
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        index.upsert(vectors=batch)


# ── Query ─────────────────────────────────────────────────────────────────────

def search_query(
    index,
    query_embedding: List[float],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search the Pinecone index and return the top-K results.

    Parameters
    ----------
    index : pinecone.Index
    query_embedding : List[float]
    top_k : int

    Returns
    -------
    List[dict]
        Each dict contains: id, score, doc_name, text, chunk_idx.
    """
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    results = []
    for match in response.get("matches", []):
        meta = match.get("metadata", {})
        results.append(
            {
                "id":        match["id"],
                "score":     match["score"],
                "doc_name":  meta.get("doc_name", "Unknown"),
                "text":      meta.get("text", ""),
                "chunk_idx": meta.get("chunk_idx", -1),
            }
        )
    return results


# ── Stats ─────────────────────────────────────────────────────────────────────

def get_index_stats(index) -> Dict[str, Any]:
    """Return basic stats about the Pinecone index."""
    stats = index.describe_index_stats()
    return {
        "total_vector_count": stats.get("total_vector_count", 0),
        "dimension":          stats.get("dimension", EMBEDDING_DIMENSION),
        "namespaces":         stats.get("namespaces", {}),
    }
