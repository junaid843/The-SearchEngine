import streamlit as st
import os
import time
from utils.pdf_processor import extract_text_from_pdf, split_text_into_chunks
from utils.embeddings import get_embedding
from utils.pinecone_client import (
    init_pinecone,
    upsert_chunks,
    search_query,
    get_index_stats,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mini Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---- Global ---- */
    body { font-family: 'Segoe UI', sans-serif; }

    /* ---- Hero banner ---- */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .hero h1 { color: #e2e8f0; font-size: 2.8rem; margin: 0; }
    .hero p  { color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem; }

    /* ---- Search bar ---- */
    .search-container {
        background: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #334155;
    }

    /* ---- Result cards ---- */
    .result-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: border-color 0.2s;
    }
    .result-card:hover { border-color: #6366f1; }
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .doc-name  { color: #818cf8; font-weight: 600; font-size: 1rem; }
    .score-badge {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .result-text { color: #cbd5e1; line-height: 1.7; font-size: 0.95rem; }
    .chunk-meta  { color: #475569; font-size: 0.8rem; margin-top: 0.6rem; }

    /* ── Sidebar stat boxes ─ */
    .stat-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .stat-label { color: #94a3b8; font-size: 0.8rem; }
    .stat-value { color: #e2e8f0; font-size: 1.6rem; font-weight: 700; }

    /* ── Upload section ─ */
    .upload-section {
        background: #1e293b;
        border: 2px dashed #334155;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>🔍 Mini Search Engine</h1>
        <p>Semantic search across your PDF documents powered by vector embeddings &amp; Pinecone</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    pinecone_api_key = st.text_input(
        "Pinecone API Key",
        type="password",
        help="Get your key from app.pinecone.io",
        placeholder="pcsk_...",
    )
    pinecone_index_name = st.text_input(
        "Index Name",
        value="mini-search-engine",
        help="Pinecone index name (will be created if missing)",
    )

    st.markdown("---")
    st.markdown("## 📊 Index Stats")

    stats_placeholder = st.empty()

    st.markdown("---")
    st.markdown("## 🔧 Search Settings")
    top_k = st.slider("Top-K Results", min_value=1, max_value=10, value=5)
    score_threshold = st.slider(
        "Min Similarity Score", min_value=0.0, max_value=1.0, value=0.0, step=0.05
    )

    st.markdown("---")
    st.markdown(
        """
        <small style='color:#475569'>
        ℹ️ Uses SentenceTransformers for embeddings (no OpenAI key needed).<br><br>
        Pinecone free tier: 1 index, 100 k vectors.
        </small>
        """,
        unsafe_allow_html=True,
    )

# ── Helper: init Pinecone ─────────────────────────────────────────────────────

@st.cache_resource
def get_pinecone_index(api_key: str, index_name: str):
    return init_pinecone(api_key, index_name)


def refresh_stats(index):
    try:
        stats = get_index_stats(index)
        total = stats.get("total_vector_count", 0)
        dim   = stats.get("dimension", "—")
        stats_placeholder.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-label">Total Vectors</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Dimensions</div>
                <div class="stat-value">{dim}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        stats_placeholder.info("Connect to Pinecone to see stats.")


# ── Main Tabs ─────────────────────────────────────────────────────────────────
tab_upload, tab_search = st.tabs(["📤 Upload PDFs", "🔍 Search"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 – UPLOAD
# ════════════════════════════════════════════════════════════════════════════════
with tab_upload:
    st.markdown("### Upload PDF Documents")
    st.caption(
        "Upload **at least 5 PDFs**. Text will be extracted, chunked, embedded, and stored in Pinecone."
    )

    if not pinecone_api_key:
        st.warning("⚠️  Please enter your **Pinecone API Key** in the sidebar first.")
    else:
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select 5 or more PDF files",
        )

        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} file(s) selected**")
            for f in uploaded_files:
                st.markdown(f"- 📄 `{f.name}` ({f.size / 1024:.1f} KB)")

            col1, col2 = st.columns([1, 3])
            with col1:
                process_btn = st.button(
                    "🚀 Process & Index",
                    type="primary",
                    disabled=len(uploaded_files) < 1,
                )

            if process_btn:
                try:
                    index = get_pinecone_index(pinecone_api_key, pinecone_index_name)
                except Exception as e:
                    st.error(f"❌ Pinecone connection failed: {e}")
                    st.stop()

                progress_bar = st.progress(0)
                status_text  = st.empty()
                log_container = st.container()

                total_chunks = 0

                for file_idx, pdf_file in enumerate(uploaded_files):
                    doc_name = pdf_file.name
                    status_text.markdown(f"**Processing:** `{doc_name}` …")

                    with log_container:
                        with st.expander(f"📄 {doc_name}", expanded=True):
                            # 1. Extract
                            step_col1, step_col2 = st.columns([1, 6])
                            with step_col1:
                                st.markdown("📝")
                            with step_col2:
                                with st.spinner("Extracting text …"):
                                    try:
                                        text = extract_text_from_pdf(pdf_file)
                                        st.success(
                                            f"Extracted **{len(text):,}** characters"
                                        )
                                    except Exception as e:
                                        st.error(f"Extraction failed: {e}")
                                        continue

                            # 2. Chunk
                            with step_col2:
                                with st.spinner("Splitting into chunks …"):
                                    chunks = split_text_into_chunks(text)
                                    st.success(
                                        f"Created **{len(chunks)}** chunks"
                                    )

                            # 3. Embed + upsert
                            with step_col2:
                                with st.spinner(
                                    f"Embedding & indexing {len(chunks)} chunks …"
                                ):
                                    chunk_dicts = []
                                    for i, chunk_text in enumerate(chunks):
                                        embedding = get_embedding(chunk_text)
                                        chunk_dicts.append(
                                            {
                                                "id": f"{doc_name}__chunk_{i}",
                                                "embedding": embedding,
                                                "text": chunk_text,
                                                "doc_name": doc_name,
                                                "chunk_idx": i,
                                            }
                                        )
                                    upsert_chunks(index, chunk_dicts)
                                    total_chunks += len(chunk_dicts)
                                    st.success("✅ Indexed in Pinecone!")

                    progress_bar.progress((file_idx + 1) / len(uploaded_files))

                status_text.markdown(
                    f"✅ **Done!** Indexed **{total_chunks}** chunks from **{len(uploaded_files)}** PDFs."
                )
                refresh_stats(index)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 – SEARCH
# ════════════════════════════════════════════════════════════════════════════════
with tab_search:
    st.markdown("### Semantic Search")
    st.caption("Ask anything — the engine finds the most relevant passages from your PDFs.")

    if not pinecone_api_key:
        st.warning("⚠️  Please enter your **Pinecone API Key** in the sidebar first.")
    else:
        # Search box
        query = st.text_input(
            "Search query",
            placeholder="e.g. What are the main conclusions about climate change?",
            label_visibility="collapsed",
        )

        col_btn, col_clear = st.columns([1, 6])
        with col_btn:
            search_btn = st.button("🔍 Search", type="primary")

        if search_btn and query.strip():
            try:
                index = get_pinecone_index(pinecone_api_key, pinecone_index_name)
            except Exception as e:
                st.error(f"❌ Pinecone connection failed: {e}")
                st.stop()

            with st.spinner("Searching …"):
                query_embedding = get_embedding(query)
                results = search_query(index, query_embedding, top_k=top_k)

            # Filter by threshold
            results = [r for r in results if r["score"] >= score_threshold]

            if not results:
                st.info(
                    f"No results found above similarity score **{score_threshold}**. "
                    "Try lowering the threshold or uploading more documents."
                )
            else:
                st.markdown(
                    f"**{len(results)} result(s)** for: *\"{query}\"*"
                )
                st.markdown("---")

                for rank, result in enumerate(results, 1):
                    score    = result["score"]
                    doc_name = result.get("doc_name", "Unknown")
                    text     = result.get("text", "")
                    chunk_idx = result.get("chunk_idx", "?")

                    # Colour the score badge
                    if score >= 0.80:
                        badge_color = "background: linear-gradient(90deg,#10b981,#059669)"
                    elif score >= 0.60:
                        badge_color = "background: linear-gradient(90deg,#f59e0b,#d97706)"
                    else:
                        badge_color = "background: linear-gradient(90deg,#6366f1,#8b5cf6)"

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-header">
                                <span class="doc-name">#{rank} &nbsp;📄 {doc_name}</span>
                                <span class="score-badge" style="{badge_color}">
                                    Score: {score:.4f}
                                </span>
                            </div>
                            <div class="result-text">{text}</div>
                            <div class="chunk-meta">Chunk #{chunk_idx} &nbsp;·&nbsp; {len(text)} characters</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            refresh_stats(index)

        elif search_btn:
            st.warning("Please enter a search query.")

# ── Initial stat refresh if key provided ─────────────────────────────────────
if pinecone_api_key:
    try:
        idx = get_pinecone_index(pinecone_api_key, pinecone_index_name)
        refresh_stats(idx)
    except Exception:
        stats_placeholder.info("Could not load stats. Check your API key.")
