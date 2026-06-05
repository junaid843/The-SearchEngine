"""
Embedding generation using SentenceTransformers.

Model: all-MiniLM-L6-v2
  - 384-dimensional embeddings
  - Fast and accurate for semantic search
  - No API key required
"""

from __future__ import annotations
from typing import List
import streamlit as st


# Cache the model so it is only downloaded / loaded once per session
@st.cache_resource(show_spinner="Loading embedding model …")
def _load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> List[float]:
    """
    Generate a 384-dimensional embedding for the given text.

    Parameters
    ----------
    text : str
        Text to embed (a chunk or a search query).

    Returns
    -------
    List[float]
        Embedding vector.
    """
    model  = _load_model()
    vector = model.encode(text, convert_to_numpy=True)
    return vector.tolist()


def get_embeddings_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for a list of texts in batches (faster for large corpora).

    Parameters
    ----------
    texts : List[str]
        Texts to embed.
    batch_size : int
        Number of texts per batch.

    Returns
    -------
    List[List[float]]
        List of embedding vectors.
    """
    model   = _load_model()
    vectors = model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
    return [v.tolist() for v in vectors]


# Expose the dimension so Pinecone index creation can use it
EMBEDDING_DIMENSION = 384
