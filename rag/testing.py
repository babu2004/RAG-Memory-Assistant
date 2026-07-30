import chromadb
from rag.bm25_manager import BM25Manager
from pathlib import Path
from rag.reranker import Reranker
from rag.retriever import semantic_search

current_dir = Path(__file__).resolve().parent
db_path = (current_dir.parent / "chroma_db").resolve()
client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection(
    "general"
)

# # -------------------------------
# # testing bm25

# bm25 = BM25Manager(collection)

# results = bm25.search(
#     "ROUGE metrics are also commonly used to evaluate answer quality ",
#     top_k = 3
# )

# for r in results:
#     print(r["scores"])
#     print(r["metadatas"])
#     print(r["documents"][:100])
#     print("-"*50)

# --------------------------------------
# testing reranker.py

reranker = Reranker()
query = "What is Query Transformation"
retrieved_chunks = semantic_search(query,top_k=6)

results = reranker.rerank(
    query = query,
    chunks = retrieved_chunks,
    top_k = 3
)


for chunk in results:
    print(chunk["rerank_score"])
    print(chunk["metadata"])
    print(chunk["document"][:120])
    print("-" * 50)
