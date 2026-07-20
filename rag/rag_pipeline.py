import sys
from pathlib import Path



#to run this file we need to set system path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from retriever import reterive
from llm.config import provider

def answer_question(query):

    results = reterive(query=query,top_k=3)

    context_parts = []

    for result in results:

        context_parts.append(
            f""" 

                Source: {result['metadata']['source']}
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

    return response


how much accuracy can be increased by research findings reveal that including irrelevant documents