# RAG-Memory-Assistant

A production-style, general-purpose Retrieval-Augmented Generation (RAG)
system built from scratch with Python.

The system allows users to upload PDF documents, index them into a
ChromaDB vector database, retrieve relevant information using hybrid
semantic + keyword search, rerank results using a cross-encoder, and
generate grounded answers through an LLM.

Built as part of my AI Engineering learning journey to understand how
modern RAG systems work internally rather than relying entirely on
high-level frameworks.

------------------------------------------------------------------------

## 🚀 Features

### Document Ingestion

-   Upload PDF documents through the browser
-   Extract text from documents
-   Recursive text chunking with configurable chunk size and overlap
-   Generate embeddings using Sentence Transformers
-   Store document chunks and embeddings in ChromaDB

### Hybrid Retrieval

Combines two complementary retrieval strategies:

-   Semantic search using vector embeddings
-   BM25 keyword-based retrieval
-   Merges results while removing duplicate chunks

This allows the system to handle both semantic questions and
keyword-specific queries.

### Cross-Encoder Reranking

Retrieved candidates are reranked using a cross-encoder before being
passed to the LLM.

``` text
Query
  ↓
Semantic Search ──┐
                  ├──→ Hybrid Results
BM25 Search ──────┘
                        ↓
                 Cross-Encoder
                        ↓
                  Top Results
```

### Grounded Generation

The LLM receives only the retrieved document context and is instructed
to avoid unsupported claims.

The system returns:

-   Generated answer
-   Source documents used for the answer

### FastAPI Backend

Provides REST API endpoints for:

-   Document upload
-   Question answering
-   Knowledge-base deletion

### Browser Interface

A lightweight HTML/CSS/JavaScript interface allows users to:

-   Upload PDFs
-   Ask questions
-   View generated answers
-   View source documents
-   Clear the current knowledge base

### Docker

The complete application can be containerized and run independently of
the local development environment.

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                         ┌──────────────────┐
                         │     Browser      │
                         │  HTML/CSS/JS     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                 Upload                       Query
                    │                           │
                    ▼                           ▼
             ┌─────────────┐             ┌─────────────┐
             │   FastAPI   │             │   FastAPI   │
             └──────┬──────┘             └──────┬──────┘
                    │                           │
                    ▼                           ▼
             Document Loader             RAG Pipeline
                    │                           │
                    ▼                           │
          Recursive Chunking                    │
                    │                           │
                    ▼                           │
             Embeddings                         │
                    │                           │
                    ▼                           │
              ChromaDB ◄────────────────────────┤
                    │                           │
                    │                    ┌──────┴──────┐
                    │                    │             │
                    │              Semantic Search   BM25
                    │                    │             │
                    │                    └──────┬──────┘
                    │                           │
                    │                    Hybrid Retrieval
                    │                           │
                    │                           ▼
                    │                    Cross-Encoder
                    │                       Reranking
                    │                           │
                    │                           ▼
                    │                         LLM
                    │                           │
                    │                           ▼
                    └──────────────────► Answer + Sources
```

------------------------------------------------------------------------

# 🔎 Retrieval Pipeline

The core retrieval pipeline is:

``` text
User Query
    ↓
Query Embedding
    ↓
┌─────────────────────┐
│ Semantic Retrieval  │
└──────────┬──────────┘
           │
           ├──────────────┐
           │              │
           ▼              ▼
      Vector Search      BM25
           │              │
           └──────┬───────┘
                  ▼
           Merge & Deduplicate
                  ↓
          Cross-Encoder Reranker
                  ↓
             Top Chunks
                  ↓
          Context Construction
                  ↓
                 LLM
                  ↓
          Grounded Answer
```

------------------------------------------------------------------------

# 📈 Project Evolution

One of the goals of this project was to understand how a RAG system
evolves from a simple implementation into a more capable retrieval
architecture.

## Version 2.0 --- JSON-Based Semantic Retrieval

The first implementation used manually persisted embeddings.

``` text
FAQ Documents
     ↓
Embedder
     ↓
embeddings.json
     ↓
Retriever
     ↓
LLM
```

This version helped establish the fundamentals of:

-   Embedding generation
-   Vector similarity
-   Semantic retrieval
-   Retrieval scoring
-   Context construction

------------------------------------------------------------------------

## Version 2.1 --- ChromaDB Migration

The embedding storage layer was migrated from JSON to ChromaDB.

``` text
Documents
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retriever
```

This removed the need to manually manage embedding files and introduced
a proper vector database.

The original JSON-based implementation was retained in the repository as
part of the project's learning and evolution history.

------------------------------------------------------------------------

## Version 3.0 --- General-Purpose RAG

The system was expanded from a fixed FAQ dataset into a general-purpose
document retrieval engine.

``` text
PDF
 ↓
Loader
 ↓
Recursive Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Hybrid Retrieval
 ↓
Cross-Encoder Reranking
 ↓
LLM
```

The system can now accept arbitrary PDF documents through the browser
and build a temporary knowledge base from the uploaded document.

------------------------------------------------------------------------

# 🧠 Why Hybrid Search?

Semantic search is good at understanding meaning.

BM25 is good at exact keyword matching.

For example:

``` text
Query:
"ROUGE metrics"
```

Semantic retrieval may find conceptually related passages, while BM25
can strongly prioritize passages containing the exact terms.

Combining both approaches provides complementary retrieval signals.

------------------------------------------------------------------------

# 🎯 Why Cross-Encoder Reranking?

Initial retrieval is optimized for finding candidate documents
efficiently.

However, the highest-scoring retrieved chunks are not always the most
relevant to the exact query.

The cross-encoder evaluates the query and candidate document together
and produces a more focused relevance score.

``` text
Initial Retrieval
      ↓
Candidate Chunks
      ↓
Cross-Encoder
      ↓
Reranked Chunks
      ↓
LLM Context
```

------------------------------------------------------------------------

# 📂 Project Structure

``` text
RAG-Memory-Assistant/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   └── templates/
│       └── index.html
│
├── ingestion/
│   ├── loaders.py
│   ├── chunker.py
│   └── ingest.py
│
├── rag/
│   ├── retriever.py
│   ├── bm25_manager.py
│   ├── reranker.py
│   ├── rag_pipeline.py
│   ├── source_detection.py
│   └── document_registry.py
│
├── llm/
│   ├── config.py
│   └── groq_provider.py
│
├── my_local_model/
│
├── Dockerfile
├── .dockerignore
├── pyproject.toml
├── uv.lock
└── README.md
```

------------------------------------------------------------------------

# 🛠️ Technologies Used

### Language

-   Python

### LLM / NLP

-   LLM APIs
-   Sentence Transformers
-   Embeddings
-   Cross-Encoder Reranking

### Retrieval

-   ChromaDB
-   BM25
-   Semantic Search
-   Hybrid Search

### Backend

-   FastAPI
-   REST APIs
-   Uvicorn

### Frontend

-   HTML
-   CSS
-   JavaScript

### Deployment

-   Docker

### Development

-   uv
-   Git
-   GitHub

------------------------------------------------------------------------

# 🚀 Running Locally

## 1. Clone the repository

``` bash
git clone https://github.com/babu2004/RAG-Memory-Assistant.git

cd RAG-Memory-Assistant
```

## 2. Install dependencies

This project uses `uv`.

``` bash
uv sync
```

## 3. Configure environment variables

Create a `.env` file containing the required LLM provider credentials.

``` text
XAI_API_KEY=your_api_key
```

Do not commit `.env` to Git.

## 4. Start the API

``` bash
uv run uvicorn app.main:app --reload
```

Open:

``` text
http://localhost:8000
```

------------------------------------------------------------------------

# 🐳 Running with Docker

Build the image:

``` bash
docker build -t rag-assistant .
```

Run the container:

``` bash
docker run --env-file .env -p 8000:8000 rag-assistant
```

Open:

``` text
http://localhost:8000
```

The application can then be used directly from the browser.

------------------------------------------------------------------------

# 🔌 API Endpoints

  Method     Endpoint        Description
  ---------- --------------- ----------------------------------
  `GET`      `/`             Web interface
  `POST`     `/upload`       Upload and ingest a PDF
  `POST`     `/query`        Ask a question
  `DELETE`   `/collection`   Clear the current knowledge base

FastAPI automatically provides interactive API documentation at:

``` text
/docs
```

------------------------------------------------------------------------

# 💡 Example Workflow

### 1. Upload a document

``` text
PDF
 ↓
POST /upload
 ↓
Load
 ↓
Chunk
 ↓
Embed
 ↓
ChromaDB
```

### 2. Ask a question

``` text
"What is Query Routing?"
```

### 3. Retrieval

``` text
Semantic Search
      +
BM25
      ↓
Hybrid Results
      ↓
Cross-Encoder
      ↓
Relevant Context
```

### 4. Generation

``` text
Context + Question
        ↓
       LLM
        ↓
Grounded Answer
```

### 5. Source attribution

``` text
Answer

Sources used:
- rag
```

------------------------------------------------------------------------

# 🧪 Engineering Concepts Demonstrated

This project was built to understand and demonstrate practical AI
engineering concepts including:

-   Document ingestion pipelines
-   Recursive text chunking
-   Embedding generation
-   Vector databases
-   Semantic retrieval
-   Keyword retrieval with BM25
-   Hybrid search
-   Cross-encoder reranking
-   Source-aware retrieval
-   Retrieval-Augmented Generation
-   Prompt grounding
-   LLM provider abstraction
-   REST API development
-   Dynamic document ingestion
-   ChromaDB collection lifecycle management
-   Docker containerization
-   Git-based project evolution

------------------------------------------------------------------------

# 🔬 Engineering Decisions

### JSON → ChromaDB

The project intentionally started with JSON-based embedding storage
before migrating to ChromaDB.

This made it possible to understand the underlying retrieval process
before introducing a vector database abstraction.

### Hybrid Retrieval

Semantic search and BM25 were combined because they provide
complementary retrieval behavior.

### Reranking

A cross-encoder was introduced after initial retrieval to improve the
relevance of the final context supplied to the LLM.

### Simple Document Lifecycle

The application maintains one temporary `general` ChromaDB collection.

Uploading a document creates a fresh knowledge base, while the delete
endpoint removes the current knowledge base.

This keeps the portfolio application simple without introducing
unnecessary multi-user or multi-tenant infrastructure.

------------------------------------------------------------------------

# 📌 Current Status

``` text
Document Loading             ✅
Recursive Chunking           ✅
Embeddings                   ✅
ChromaDB                     ✅
Semantic Search              ✅
BM25 Retrieval               ✅
Hybrid Search                ✅
Cross-Encoder Reranking      ✅
RAG Generation               ✅
Source Attribution           ✅
FastAPI                      ✅
PDF Upload                   ✅
Knowledge Base Deletion      ✅
Browser UI                   ✅
Docker                       ✅
```

------------------------------------------------------------------------

# 🔮 Future Improvements

Possible future improvements include:

-   Retrieval and generation evaluation pipelines
-   Retrieval metrics such as Hit Rate and MRR
-   Query expansion and rewriting
-   Streaming LLM responses
-   Authentication and multi-user document isolation
-   More document formats
-   Cloud deployment

These are intentionally kept outside the current implementation to keep
the project focused on the core RAG architecture.

------------------------------------------------------------------------

# 👨‍💻 Author

**R. Ganesh Babu**

Master of Data Science student focused on Machine Learning, AI
Engineering, LLM applications, and Retrieval-Augmented Generation.

-   GitHub: https://github.com/babu2004
-   LinkedIn: https://www.linkedin.com/in/ganesh-babu-333a7530a/

------------------------------------------------------------------------

## ⭐ Project Goal

The goal of this project is not simply to build a chatbot.

It is to understand how a practical RAG system is constructed, evolved,
evaluated, and deployed---from basic embedding retrieval to a complete
application with hybrid retrieval, reranking, APIs, document ingestion,
and containerization.
