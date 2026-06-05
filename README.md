# 🔍 Mini Search Engine — Semantic PDF Search

A Google-like semantic search application built with **Streamlit**, **SentenceTransformers**, and **Pinecone**.  
Upload PDFs, ask natural-language questions, and get the most relevant passages back — ranked by similarity.

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| 📤 Multi-PDF upload | Upload 5 or more PDFs at once |
| ✂️ Text chunking | Overlapping 500-word chunks for better recall |
| 🧠 Local embeddings | `all-MiniLM-L6-v2` via SentenceTransformers — **no OpenAI key needed** |
| 🗄️ Pinecone storage | Cosine-similarity vector search at scale |
| 🔎 Semantic search | Top-K results with similarity scores |
| 📊 Live index stats | Total vectors & dimension shown in sidebar |

---

## 🗂️ Project Structure

```
mini_search_engine/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── generate_sample_pdfs.py     # Script to regenerate sample PDFs
├── README.md                   # This file
├── sample_pdfs/                # 5 ready-to-use demo PDFs
│   ├── 01_Artificial_Intelligence.pdf
│   ├── 02_Climate_Change.pdf
│   ├── 03_Space_Exploration.pdf
│   ├── 04_Cybersecurity.pdf
│   └── 05_Blockchain_Technology.pdf
└── utils/
    ├── __init__.py
    ├── pdf_processor.py        # PDF extraction & chunking
    ├── embeddings.py           # SentenceTransformer wrapper
    └── pinecone_client.py      # Pinecone init, upsert, search
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone <your-repo-url>
cd mini_search_engine
pip install -r requirements.txt
```

> First run downloads the `all-MiniLM-L6-v2` model (~90 MB). Subsequent runs use the cache.

### 2. Get a free Pinecone API key

1. Sign up at [app.pinecone.io](https://app.pinecone.io)  
2. Create a project → copy the **API key** from the dashboard  
3. The app will automatically create the index on first use (free Starter plan supports 1 serverless index)

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Use the app

1. **Sidebar** → paste your Pinecone API key  
2. **Upload PDFs tab** → upload the 5 PDFs from `sample_pdfs/` (or your own)  
3. Click **Process & Index** — progress is shown per file  
4. **Search tab** → type a natural-language query and click **Search**

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.32 | Web UI |
| pypdf | ≥4.1 | PDF text extraction |
| sentence-transformers | ≥2.7 | Local embeddings |
| pinecone | ≥3.2 | Vector database |
| torch | ≥2.2 | SentenceTransformer backend |
| transformers | ≥4.40 | Tokenizers |

---

## 🔧 Configuration (Sidebar)

| Setting | Default | Description |
|---------|---------|-------------|
| Pinecone API Key | — | Your Pinecone secret key |
| Index Name | `mini-search-engine` | Created automatically if absent |
| Top-K Results | 5 | Number of results to return |
| Min Similarity Score | 0.0 | Filter results below this threshold |

---

## 🧪 Sample Queries to Try

After uploading the 5 demo PDFs, try these queries:

- *"What are the main challenges of artificial intelligence?"*
- *"How does the Paris Agreement address climate change?"*
- *"Tell me about the Apollo Moon landing"*
- *"What is Zero Trust security?"*
- *"How do smart contracts work on Ethereum?"*

---

## 📐 Architecture

```
User uploads PDF
      │
      ▼
 pypdf extracts text
      │
      ▼
 Split into 500-word overlapping chunks
      │
      ▼
 SentenceTransformer encodes each chunk → 384-dim vector
      │
      ▼
 Pinecone upserts vectors + metadata (text, doc_name, chunk_idx)
      │
      ▼
 User types a query
      │
      ▼
 Query embedded → cosine similarity search in Pinecone
      │
      ▼
 Top-K results displayed with doc name, score, and text
```

---

## 🌐 Deployment on Streamlit Cloud

1. Push this repo to GitHub  
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**  
3. Select your repo, set **Main file**: `app.py`  
4. Add `PINECONE_API_KEY` as a **Secret** (optional — users can also enter it in the sidebar)  
5. Click **Deploy**

---

## 📄 License

MIT — free for personal and commercial use.
