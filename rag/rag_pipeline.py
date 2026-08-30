import sys
from pathlib import Path
import chromadb



from rag.retriever import (
    semantic_search,
    extract_sources,
    refresh_collection
)
from rag.bm25_manager import BM25Manager
from llm.config import provider
from rag.reranker import Reranker

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

def refresh_rag_components():

    global collection, bm25

    collection = client.get_collection("general")

    bm25 = BM25Manager(collection)

    refresh_collection()

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
 You are a helpful, accurate, and grounded AI assistant.

Your task is to answer the user's question using the provided retrieved context as the primary and authoritative source.

[CONTEXT]
{context}
[END OF CONTEXT]

[USER QUESTION]
{query}
[END OF USER QUESTION]

## Instructions

### 1. Use the context as your source of truth

Base your answer on the information contained in the provided context.

You may:

* combine information from multiple retrieved passages,
* summarize information,
* explain concepts in clearer language,
* organize information logically,
* rewrite information into the format requested by the user,
* adapt the level of detail to the user's request.

Do NOT introduce facts that are not supported by the context.

### 2. Follow the user's intent

Do not simply copy sentences from the retrieved context.

Understand what the user is asking for and construct an appropriate response.

For example:

* If the user asks "What is X?" → provide a clear definition and relevant explanation.
* If the user asks "Explain X" → explain the concept using the relevant information from the context.
* If the user asks "Describe X" → provide a structured description.
* If the user asks for a "2-mark answer" → provide a concise exam-style answer.
* If the user asks for a "5-mark answer" → provide a moderately detailed, structured answer.
* If the user asks for a "10-mark answer" → provide a detailed answer with relevant points and explanation.
* If the user asks for bullet points → use bullet points.
* If the user asks for a comparison → present the relevant differences clearly.
* If the user asks for steps or a procedure → present the supported steps in logical order.
* If the user asks for an example → provide an example only if the context contains enough information to support one.
* If the user asks for a summary → summarize the relevant context without unnecessary details.

### 3. Synthesize, don't copy

The retrieved context may contain fragmented chunks.

Combine relevant chunks when necessary to form a coherent answer.

Do not simply return the retrieved chunks verbatim.

Rewrite and synthesize the information into a natural response while preserving the meaning of the source.

### 4. Stay grounded

Do not use outside knowledge to fill missing information.

Do not speculate.

Do not make assumptions.

Do not invent examples, definitions, numbers, dates, or explanations that are not supported by the context.

If the context only partially answers the question, answer only the supported portion and clearly state what information is missing.

### 5. When the answer is not available

If the provided context does not contain enough relevant information to answer the question, respond exactly:

"I am sorry, but the provided documentation does not contain enough information to answer your question."

Do not attempt to answer from general knowledge.

### 6. Prefer useful answers over source repetition

The goal is to transform the retrieved information into the answer the user actually requested.

For example:

Context:
"RAG consists of retrieval and generation..."

Question:
"Write a 2-mark answer for RAG."

Return a concise exam-style explanation, not the original sentence from the context.

### 7. Preserve technical accuracy

Keep important technical terminology, names, formulas, terminology, and relationships from the context accurate.

Do not change the meaning of technical statements while simplifying the explanation.

### 8. Answer directly

Do not begin with phrases such as:

"According to the context..."

"Based on the provided context..."

"The context states..."

Unless the user specifically asks for source analysis.

Simply answer the user's question.

## Final requirement

The final answer must be:

* grounded in the retrieved context,
* responsive to the user's intent,
* appropriately detailed for the requested format,
* naturally written,
* and free from unsupported information.

    """
    messages_array = [
{"role": "user", "content": prompt}
]
    response = provider.generate(messages_array)

    final_response=f"{response}\n\nSources used: {', '.join(unique_sources)}"

     #final_response
    return {
    "answer": response,
    "sources": unique_sources
}


