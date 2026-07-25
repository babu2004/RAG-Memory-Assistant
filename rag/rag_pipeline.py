import sys
from pathlib import Path
import chromadb


#to run this file we need to set system path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from retriever import  semantic_search,extract_sources
from bm25_manager import BM25Manager
from llm.config import provider
from reranker import Reranker

current_dir = Path(__file__).resolve().parent
db_path = (current_dir.parent / "chroma_db").resolve()
client = chromadb.PersistentClient(
    path = str(db_path)
)

collection = client.get_collection(
    "general"
)

bm25 = BM25Manager(collection)
reranker = Reranker()


def merge_results(semantic_results,bm25_results):

   # Merge semantic and BM25 retrieval results.
   # Duplicate chunks are removed using their chunk IDs.
    merged = {}

    for chunk in semantic_results:
        merged[chunk["id"]] = chunk

    for chunk in bm25_results:
        if chunk["id"] not in merged:
            merged[chunk["id"]] = chunk
    
    return list(merged.values())
    


def answer_question(query):

    semantic_results =  semantic_search(query=query,top_k=3)
    bm25_results = bm25.search(query=query,top_k=3)

    merged_chunks = merge_results(semantic_results,bm25_results)

    ranked_chunks = reranker.rerank(query,merged_chunks)


    unique_sources = extract_sources(ranked_chunks)

    context_parts = []

    for result in ranked_chunks:

        context_parts.append(
            f""" 

                Source: {result['metadata']}
            {result['document']}
            """
        )

    context = "\n --- \n".join(context_parts)

    prompt = f"""
 You are a helpful, secure, and accurate assistant. Your task is to answer the user's question using ONLY the provided context blocks below.

[CONTEXT]
{context}
[END OF CONTEXT]

Strict Guidelines:
1. Grounding: Rely strictly on the clear facts directly mentioned in the context. Do not assume, extrapolate, or bring in outside knowledge.
2. Unanswerable Questions: If the context does not contain the exact answer to the question, state clearly: "I am sorry, but the provided documentation does not contain enough information to answer your question."
3. No Speculation: Never say things like "Based on my knowledge..." or "The text implies...". If it is not explicitly written, it does not exist.

User Question: 
{query}

    """
    messages_array = [
{"role": "user", "content": prompt}
]
    response = provider.generate(messages_array)

    final_response=f"{response}\n\nSources used: {', '.join(unique_sources)}"

    return final_response


