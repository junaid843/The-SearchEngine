"""
PDF text extraction and chunking utilities.
Uses pypdf (no external binary needed).
"""

from __future__ import annotations
import io
import re
from typing import List

from pypdf import PdfReader


# ── Text extraction ───────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract all text from a PDF file-like object or file path.

    Parameters
    ----------
    pdf_file : file-like or str
        A Streamlit UploadedFile, a BytesIO, or a path string.

    Returns
    -------
    str
        All extracted text joined with newlines.
    """
    if isinstance(pdf_file, (str, bytes)):
        reader = PdfReader(pdf_file)
    else:
        # Streamlit UploadedFile or BytesIO
        content = pdf_file.read()
        reader  = PdfReader(io.BytesIO(content))

    pages_text: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages_text.append(page_text)

    full_text = "\n".join(pages_text)
    # Normalise whitespace (collapse multiple blank lines, strip leading/trailing)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text).strip()
    return full_text


# ── Text chunking ─────────────────────────────────────────────────────────────

def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    Split text into overlapping chunks of roughly `chunk_size` words.

    Parameters
    ----------
    text : str
        The full document text.
    chunk_size : int
        Target number of words per chunk.
    chunk_overlap : int
        Number of words to overlap between consecutive chunks.

    Returns
    -------
    List[str]
        Non-empty text chunks.
    """
    if not text.strip():
        return []

    words = text.split()
    if not words:
        return []

    chunks: List[str] = []
    start = 0

    while start < len(words):
        end        = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end]).strip()
        if chunk_text:
            chunks.append(chunk_text)
        if end >= len(words):
            break
        start = end - chunk_overlap  # slide back for overlap

    return chunks
