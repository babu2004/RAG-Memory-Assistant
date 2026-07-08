#  RAG Memory Assistant

A production-style **Retrieval-Augmented Generation (RAG)** system built from scratch to understand how modern AI assistants retrieve knowledge before generating answers.

Unlike many RAG tutorials that immediately rely on frameworks, this project first implements semantic search manually using embeddings and cosine similarity, then evolves into a production-ready architecture using **ChromaDB**.

---

##  Features

-  Semantic Search using Sentence Transformers
-  Retrieval-Augmented Generation (RAG)
-  DataTalks.Club FAQ Knowledge Base
-  ChromaDB Vector Database
-  Local LLM Support (Ollama)
-  Cloud LLM Support (Groq)
-  Provider Abstraction Layer
-  Top-K Document Retrieval
-  Modular Software Architecture
-  Persistent Vector Storage

---

##  System Architecture

```
                    User
                      │
                      ▼
               RAG Pipeline
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Retriever              Prompt Builder
          │
          ▼
      ChromaDB
          │
          ▼
SentenceTransformer
          │
          ▼
      FAQ Dataset
```

---

##  Project Evolution

###  Version 2.0 — JSON-Based RAG

To understand the fundamentals of Retrieval-Augmented Generation, the entire retrieval system was implemented manually.

Features:

- Generated embeddings using Sentence Transformers
- Stored embeddings in `embeddings.json`
- Implemented cosine similarity manually
- Built a custom Top-K semantic retriever
- Constructed context manually for the LLM

Architecture:

```
faq.json
    │
    ▼
embedder.py
    │
    ▼
embeddings.json
    │
    ▼
retriever.py
    │
    ▼
rag_pipeline.py
    │
    ▼
LLM
```

---

###  Version 2.1 — ChromaDB Migration

After understanding the underlying concepts, the custom vector storage was replaced with **ChromaDB** while keeping the overall RAG pipeline unchanged.

Improvements:

- Replaced JSON embedding storage
- Replaced manual cosine similarity
- Persistent vector database
- Cleaner retrieval layer
- Production-style architecture

Architecture:

```
faq.json
    │
    ▼
SentenceTransformer
    │
    ▼
ChromaDB
    │
    ▼
retriever.py
    │
    ▼
rag_pipeline.py
    │
    ▼
LLM
```

This migration demonstrates how a custom prototype can evolve into a production-ready retrieval system.

---

##  Tech Stack

- Python
- Sentence Transformers
- ChromaDB
- Ollama
- Groq API
- UV
- Git
- JSON

---

##  Project Structure

```
rag-memory-assistant/
│
├── app.py
├── config.py
│
├── data/
│   └── faq.json
│
├── llm/
│   ├── provider.py
│   ├── ollama_provider.py
│   └── groq_provider.py
│
├── rag/
│   ├── chroma_manager.py
│   ├── retriever.py
│   └── rag_pipeline.py
│
├── chroma_db/
│
├── pyproject.toml
├── uv.lock
└── README.md
```

---

##  Installation

```bash
git clone <repository-url>

cd rag-memory-assistant

uv sync
```

---

##  Run

```bash
uv run app.py
```

---

##  Example Questions

```
When does the course start?

Can I join after the course starts?

How do I register?

What Python version should I install?
```

---

##  What I Learned

This project helped me understand the complete Retrieval-Augmented Generation workflow:

- Embedding Models
- Semantic Search
- Cosine Similarity
- Vector Similarity
- Top-K Retrieval
- Vector Databases
- ChromaDB
- Software Architecture
- Provider Abstraction
- Production-style RAG Systems

---

##  Roadmap

###  Completed

- Semantic Search
- JSON-based Vector Store
- Custom Retriever
- RAG Pipeline
- ChromaDB Migration

###  Coming Next

- PDF Ingestion
- DOCX Support
- Markdown Support
- Website Loader
- Conversation Memory
- Hybrid Search
- Reranking
- Agentic RAG

---

##  Why This Project?

The goal of this project was not simply to use existing RAG frameworks, but to understand **how Retrieval-Augmented Generation works internally**.

Instead of starting with libraries such as LangChain or LlamaIndex, this project first builds the core components manually and then gradually replaces them with production-grade tools like ChromaDB.

This approach provides a much deeper understanding of modern AI systems and the engineering principles behind them.